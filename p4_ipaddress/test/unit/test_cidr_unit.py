import unittest
import ipaddress
from p4_ipaddress.src.cidr import *


class Test_cidr(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_is_cidr(self):
        assert extract_ipaddress(Test_cidr.get_ipv4_cidr()) == Test_cidr.get_ipv4()
        assert extract_ipaddress(Test_cidr.get_ipv6_cidr()) == Test_cidr.get_ipv6()
        with self.assertRaises(ValueError):
            extract_ipaddress(Test_cidr.get_ipv4())
            extract_ipaddress(Test_cidr.get_ipv6())

    def test_valid_address(self):
        assert validIPAddress(Test_cidr.get_ipv4() == "IPv4")
        assert validIPAddress(Test_cidr.get_ipv6() == "IPv6")

    def test_ipv4_range(self):
        """test with ipv4 corner cases compore the start,end and the length"""
        network = get_ipaddress(Test_cidr.get_ipv4_corner())
        expected_start_ip = ipaddress.ip_address("192.168.1.0")
        expected_end_ip = ipaddress.ip_address("192.168.1.255")
        expected_network_length = 256

        start_ip = network.network_address
        end_ip = network.broadcast_address

        assert expected_start_ip == start_ip
        assert expected_end_ip == end_ip
        assert expected_network_length == network.num_addresses

    def test_ipv6_range(self):
        """test with ipv6 corner cases compore the start,end and the length"""
        network = get_ipaddress(Test_cidr.get_ipv6_corner())
        expected_start_ip = ipaddress.ip_address("2001:0db8::")
        expected_end_ip = ipaddress.ip_address("2001:0db8::3")
        expected_network_length = 4

        start_ip = network.network_address
        end_ip = network.broadcast_address

        assert expected_start_ip == start_ip
        assert expected_end_ip == end_ip
        assert expected_network_length == network.num_addresses

    def get_ipv4():
        return "129.45.67.89"

    def get_ipv4_cidr():
        return "129.45.67.89/27"

    def get_ipv6_cidr():
        return "2001:0db8:85a3:0000:0000:8a2e:0370:7334/64"

    def get_ipv6():
        return "2001:0db8:85a3:0000:0000:8a2e:0370:7334"

    def get_ipv4_corner():
        return "192.168.1.0/24"

    def get_ipv6_corner():
        return "2001:0db8::/126"


if __name__ == "__main__":
    unittest.main()
