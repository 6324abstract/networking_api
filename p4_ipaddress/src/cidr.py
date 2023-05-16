import ipaddress
import re


def get_ipaddress(cidr):
    ipaddress_without_cidr = extract_ipaddress(cidr)
    ip_version = validIPAddress(ipaddress_without_cidr)
    if ip_version == "IPv4":
        address_list = ipaddress.IPv4Network(cidr, strict=False)
    elif ip_version == "IPv6":
        address_list = ipaddress.IPv6Network(cidr, strict=False)
    else:
        raise ValueError("invalid ipaddress")
    return address_list


def extract_ipaddress(cidr):
    pattern = r"(.+?)/"
    match = re.search(pattern, cidr)
    if match:
        return match.group(1)
    else:
        raise ValueError("not a CIDR")


def validIPAddress(IP: str) -> str:
    try:
        return (
            "IPv4"
            if type(ipaddress.ip_address(IP)) is ipaddress.IPv4Address
            else "IPv6"
        )
    except ValueError:
        return "Invalid"
