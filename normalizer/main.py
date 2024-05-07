import asyncio
import dataclasses
import os
import sys
import zmq

from dotenv import load_dotenv
from normalizers.crowdstrike_norm import crowdstrike_norm
from normalizers.qualys_norm import qualys_norm
from pathlib import Path
from storage.store import MongoHostsManager

load_dotenv()

sys.path.append(Path(__file__).parent)

SOURCE_NORM_MAP = {
    "crowdstrike": crowdstrike_norm,
    "qualys": qualys_norm
}
store_queue = asyncio.Queue()  # Create a queue for storing normalized data


def get_normalizer(source_name: str):
    return SOURCE_NORM_MAP.get(source_name)


def _get_fetcher_socket():
    """
    Get the ZMQ PULL socket for fetching data.
    Returns:
        zmq.Socket: The ZMQ PULL socket object.
    """
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PULL)
    socket = os.getenv("PULL_SOCKET")  # or "tcp://fetcher:5555"
    zmq_socket.connect(socket)
    print("SOCKET", socket)
    return zmq_socket


async def normalize(fetch_socket):
    """
    Asynchronously normalizes incoming messages from fetch_socket.
    Retrieves a normalizer based on the message source name, normalizes the message,
    converts it to JSON, and puts it into a store queue. If no normalizer is found
    for the source name, it prints an error message.
    This function runs indefinitely, periodically checking for new messages.
    """
    while True:
        message = fetch_socket.recv_json()
        # print(message)
        if message:
            normalizer = get_normalizer(message["source_name"])
            if normalizer:
                generic_data = normalizer(message)
                json_data = dataclasses.asdict(generic_data)
                await store_queue.put(json_data)
            else:
                print(f"Unknown source: {message['source_name']}")
        await asyncio.sleep(0)


async def store():
    """
    Asynchronously stores data retrieved from a queue into a MongoDB instance.

    This function continuously reads data from a queue and stores it in a MongoDB
    database pointed to by the specified hostname.

    Parameters:
        None

    Returns:
        None
    """
    mongo = MongoHostsManager(host=os.getenv("MONGO_HOSTNAME"))
    while True:
        try:
            read_data = await store_queue.get()
            if read_data:  # Get data from queue with timeout
                mongo.store(read_data)
        except asyncio.QueueEmpty:
            # Handle empty queue case (optional: wait or continue)
            pass
        await asyncio.sleep(0)


async def main():
    """
    A function that retrieves a fetcher socket and then normalizes the data fetched
    from it while storing the normalized data.
    """
    fetch_socket = _get_fetcher_socket()
    await asyncio.gather(normalize(fetch_socket), store())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
