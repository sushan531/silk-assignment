import dataclasses
import datetime

from dataclasses import dataclass
from dataclasses import field


@dataclass
class DevicePolicy:
    """
    Dataclass representing Device Policy information.
    """
    policy_name: str
    policy_type: str
    policy_id: str
    applied: bool


@dataclass
class Hosts:
    """
    Dataclass representing normalized Hosts information.
    """
    source_name: str
    hostname: str
    ip_address: str
    external_ip: str = ""
    last_vuln_scan: datetime.datetime = ""
    latitude: float = 0.0
    longitude: float = 0.0
    platform: str = ""
    os: str = ""
    cloud_provider: str = ""
    service_provider: str = ""
    zone: str = ""
    tags: list = field(default_factory=list)
    mac_address: str = ""
    instance_id: str = ""
    device_policies: list[DevicePolicy] = field(default_factory=list)
    last_seen: datetime.datetime = ""

    # TODO based on requirement more can be added in future
    # For Demonstration purpose I have limited to to few selected fields.

    def merge_hosts(self, other: "Hosts") -> "Hosts":
        """
        Merges another Hosts dataclass with this instance, prioritizing values from the argument.

        Args:
            other: The Hosts dataclass to merge with (values take precedence).

        Returns:
            A new Hosts dataclass with merged information.
        """
        merged_data = {}
        for field in dataclasses.fields(Hosts):
            # Access the attribute value for each field
            value1 = getattr(self, field.name)
            value2 = getattr(other, field.name)

            # Use the value from the argument if not None
            merged_data[field.name] = value2 if value2 is not None else value1

        return Hosts(**merged_data)


@dataclass
class NormSource:
    source_name: str
    socket: str
    storage_socket: str

    def __repr__(self):
        """
        Return a string representation of the object.
        """
        return f"SourceName: {self.source_name}, socket: {self.socket}"
