import sys

import aiohttp
import asyncio

import zmq

from dotenv import load_dotenv
from models.models import FetcherSource
from pathlib import Path
from typing import List
from utils.utils import get_env
from utils.utils import get_sources

sys.path.append(Path(__file__).parent)

load_dotenv()


async def fetch_data(source: FetcherSource, headers: dict, zmq_socket: zmq.Socket):
    """
    Asynchronously fetches data from a given source using the provided headers and sends the data to a ZeroMQ socket.

    Args:
        source (FetcherSource): The source from which to fetch the data.
        headers (dict): The headers to include in the request.
        zmq_socket (zmq.Socket): The ZeroMQ socket to send the data to.

    Returns:
        None
    """
    async with aiohttp.ClientSession() as session:
        print(f"Fetching data from {source.source_name}...")
        while True:
            try:
                params = {
                    "skip": source.skip,
                    "limit": source.limit
                }
                async with session.post(source.url, headers=headers, params=params) as response:
                    response.raise_for_status()  # Raise exception for non-200 status codes
                    data = await response.json()
                    source.skip += source.limit
                    for item in data:
                        item["source_name"] = source.source_name
                        zmq_socket.send_json(item)
            except aiohttp.ClientError as e:
                print(f"Error: An error occurred during the request - {e}")
                # Handle the error more specifically (e.g., log the error, retry)
                break
            except Exception as e:  # Catch generic exceptions for unexpected issues
                print(f"Unexpected error: {e}")
                # Handle unexpected errors (e.g., log the error, exit gracefully)
                break


async def main(source_objects: List[FetcherSource], token: str, socket: str):
    """
    Asynchronously fetches data from multiple sources using the provided headers
    and sends the data to a ZeroMQ socket for processing.

    Args:
        source_objects (List[FetcherSource]): A list of FetcherSource objects representing the sources to fetch data from.
        token (str): The authentication token to be included in the headers.
        socket (str): The ZeroMQ socket address to push the fetched data to.

    Returns:
        None
    """
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind(socket)

    if source_objects is not None and token is not None:
        headers = {
            "accept": "application/json",
            "token": token
        }
        tasks = []
        for source in source_objects:
            tasks.append(fetch_data(source, headers.copy(), zmq_socket))  # Avoid modifying original dict
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    source_objects = get_sources()
    token, socket = get_env()
    asyncio.run(main(source_objects=source_objects, token=token, socket=socket))
