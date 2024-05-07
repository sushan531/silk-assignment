from dataclasses import dataclass


@dataclass
class FetcherSource:
    source_name: str
    url: str
    skip: int = 0
    limit: int = 2

    def __repr__(self):
        """
        Returns a string representation of the object with the source name and URL.
        """
        return f"SourceName: {self.source_name}, URL: {self.url}"
