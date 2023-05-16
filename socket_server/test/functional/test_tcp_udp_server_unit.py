from socket_server.src.my_server import *
import socket
import threading
import unittest
import xmlrpc.client


class Test_tcp_udp_server(unittest.TestCase):
    def setUp(self) -> None:
        self.test_server = Server()
        self.host = "localhost"
        self.tcp_port, self.udp_port = 12000, 12001
        self.client_message = "test_message"
        self.server_thread_tcp = MyThread(
            target=self.test_server.start_tcp, args=(self.tcp_port,)
        )
        self.server_thread_udp = MyThread(
            target=self.test_server.start_udp, args=(self.udp_port,)
        )

    def tearDown(self) -> None:
        self.server_thread_tcp.stop()
        self.server_thread_udp.stop()

    def test_udp_server(self):
        self.server_thread_udp.start()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect((self.host, self.udp_port))
            sock.sendall(bytes(self.client_message + "\n", "utf-8"))
            received = str(sock.recv(1024), "utf-8")
            assert received == self.client_message.upper()

    def test_tcp_server(self):
        self.server_thread_tcp.start()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.tcp_port))
            sock.sendall(bytes(self.client_message + "\n", "utf-8"))
            received = str(sock.recv(1024), "utf-8")
            assert received == self.client_message.upper()

    # def test_invalid_message_to_tcp_server(self):
    #     self.server_thread_tcp.start()
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #         sock.connect((self.host, self.tcp_port))
    #         sock.sendall(self.client_message)
    #         received = str(sock.recv(1024), "utf-8")
    #         assert received == self.client_message.upper()


class Test_rpc_server(unittest.TestCase):
    def setUp(self) -> None:
        self.host = "localhost"
        self.rpc_port = 12002
        self.url = "http://" + self.host + ":" + str(self.rpc_port) + "/RPC2"
        print(self.url)
        self.test_server = Server()
        self.server_thread_rpc = MyThread(
            target=self.test_server.start_xmlrpc, args=(self.rpc_port,)
        )

    def test_correct_result(self):
        self.server_thread_rpc.start()
        with xmlrpc.client.ServerProxy(self.url) as proxy:
            assert proxy.add(1, 2) == 3

    def test_unknown_function(self):
        pass

    def tearDown(self) -> None:
        self.server_thread_rpc.stop()


class MyThread(threading.Thread):
    def __init__(self, target=None, args=()):
        super().__init__(target=target, args=args)
        self._stop_flag = threading.Event()

    def stop(self):
        self._stop_flag.set()


if __name__ == "__main__":
    unittest.main()
