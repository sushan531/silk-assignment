import os

import yaml

from dotenv import load_dotenv
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple

load_dotenv()

from models.models import FetcherSource


def get_sources() -> Optional[List[FetcherSource]]:
    """
    Retrieves fetcher sources from a YAML file and returns a list of FetcherSource objects.

    Returns:
        Optional[List[FetcherSource]]: A list of FetcherSource objects if successful, None otherwise.
    """
    current_file_path = Path(__file__)
    source_file = current_file_path.parent.parent.joinpath("sources.yaml")
    source_obj = []
    with open(source_file) as stream:
        try:
            sources = yaml.safe_load(stream)
            for source in sources:
                source_obj.append(FetcherSource(
                    source_name=source["source"]["name"],
                    url=source["source"]["url"],
                ))
            return source_obj
        except yaml.YAMLError as exc:
            print(exc)
            return None


def get_env() -> Optional[Tuple[List]]:
    """
    Return the environment variables 'TOKEN' and 'PUSH_SOCKET'.

    Returns:
        Optional[Tuple[List]]: A tuple containing the 'TOKEN' and 'PUSH_SOCKET' environment variables.
    """
    return os.getenv("TOKEN"), os.getenv("PUSH_SOCKET") # or "tcp://0.0.0.0:5555"
