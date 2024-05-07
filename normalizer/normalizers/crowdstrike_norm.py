from models.models import DevicePolicy
from models.models import Hosts
from typing import List


def _convert_to_policy_list(device_policies: dict) -> List[DevicePolicy]:
    """
    Convert a dictionary of device policies into a list of DevicePolicy objects.

    Args:
        device_policies (dict): A dictionary containing device policies.

    Returns:
        List[DevicePolicy]: A list of DevicePolicy objects.
    """
    policy_list = []
    for policy_name, policy_details in device_policies.items():
        policy_list.append(DevicePolicy(
            policy_name=policy_name,
            policy_type=policy_details.get("policy_type"),
            policy_id=policy_details.get("policy_id"),
            applied=policy_details.get("applied"),
        ))
    return policy_list


def crowdstrike_norm(host: dict) -> Hosts:
    """
    Generate a Hosts object from the provided host dictionary.

    Parameters:
    - host (dict): A dictionary containing information about a host.

    Returns:
    - Hosts: A Hosts object populated with the host information.
    """
    return Hosts(
        source_name=host.get("source_name", ""),
        hostname=host.get("hostname", ""),
        ip_address=host.get("local_ip", ),
        external_ip=host.get("external_ip", ""),
        platform=host.get("platform_name", ""),
        os=host.get("os_version", ""),
        service_provider=host.get("service_provider", ""),
        zone=host.get("zone_group", ""),
        tags=host.get("tags", []),
        mac_address=host.get("mac_address", "").replace("-", ":"),
        instance_id=host.get("instance_id", ""),
        device_policies=_convert_to_policy_list(host.get("device_policies", {})),
        last_seen=host.get("last_seen", ""),
    )
