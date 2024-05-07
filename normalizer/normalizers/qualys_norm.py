from models.models import Hosts

"""
Get the availability zone from the source info dictionary.

Args:
    source_info (dict): The source information dictionary.

Returns:
    str: The availability zone extracted from the source info.
"""
def _get_zone(source_info: dict) -> str:
    _list = source_info.get("list", [])
    for item in _list:
        if "Ec2AssetSourceSimple" in item:
            availability_zone = item["Ec2AssetSourceSimple"]["availabilityZone"]
            return availability_zone
    return ""



def _get_mac_address(source_info: dict) -> str:
    """
    Get the MAC address from the source information provided.

    Parameters:
    source_info (dict): A dictionary containing source information.

    Returns:
    str: The MAC address extracted from the source information.
    """
    _list = source_info.get("list", [])
    for item in _list:
        if "Ec2AssetSourceSimple" in item:
            mac_address = item["Ec2AssetSourceSimple"]["macAddress"]
            return mac_address
    return ""


def _get_tags(tags: dict) -> list:
    """
    Get a list of tag names from a dictionary of tags.

    :param tags: A dictionary containing tags
    :type tags: dict
    :return: A list of tag names
    :rtype: list
    """
    tags_list = []
    if not tags:
        return []
    for item in tags.get("list", []):
        tag_name = item["TagSimple"]["name"]
        tags_list.append(tag_name)
    return tags_list


def _get_instance_id(source_info: dict) -> str:
    """
    A function that retrieves the instance ID from a dictionary of source information.

    Parameters:
    source_info (dict): A dictionary containing source information.

    Returns:
    str: The instance ID extracted from the source information dictionary. Returns an empty string if not found.
    """
    _list = source_info.get("list", [])
    for item in _list:
        if "Ec2AssetSourceSimple" in item:
            instance_id = item["Ec2AssetSourceSimple"]["instanceId"]
            return instance_id
    return ""


def qualys_norm(host: dict) -> Hosts:
    """
    Generate a Hosts object from a dictionary representing a host.

    Args:
        host (dict): A dictionary containing the host information.

    Returns:
        Hosts: A Hosts object with the normalized host information.

    """
    return Hosts(
        source_name=host.get("source_name", ""),
        hostname=host.get("dnsHostName", ""),
        ip_address=host.get("address", ""),
        external_ip=host.get("agentInfo", {}).get("connectedFrom", ""),
        last_vuln_scan=host.get("lastVulnScan", {}).get("$date", ""),
        latitude=host.get("agentInfo", {}).get("locationGeoLatitude", ""),
        longitude=host.get("agentInfo", {}).get("locationGeoLongtitude", ""),
        platform=host.get("agentInfo", {}).get("platform", ""),
        os=host.get("os", ""),
        cloud_provider=host.get("cloudProvider", ""),
        zone=_get_zone(host.get("sourceInfo", {})),
        tags=_get_tags(host.get("tags", {})),
        mac_address=_get_mac_address(host.get("sourceInfo", {})),
        instance_id=_get_instance_id(host.get("sourceInfo", {})),
    )
