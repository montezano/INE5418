from socket import AF_INET, SOCK_STREAM, socket, SHUT_RDWR, timeout
from concurrent.futures import ThreadPoolExecutor
from sys import argv
from time import sleep

leader = None
class Servidorzinho:
	def __init__(self, conn, threads):
		self.addr = (("172.78.0.2",1337),("172.78.0.3",1337),("172.78.0.4",1337),("172.78.0.5",1337),)
		self.conn = conn
		pool = ThreadPoolExecutor(threads)
		sig_sender = ThreadPoolExecutor(1)
		sock = socket(a
				AF_INET,
				SOCK_STREAM)
		sock.bind(conn)
		sock.listen(8)
		print("Server On.")
		sig_sender.submit(self._sender)
		while True:
			try:
				client_sock, client_addr = sock.accept()
				client_sock.settimeout(1+len(self.addr))
				print("Connection from {}.".format(client_addr))
				pool.submit(self._handle, client_sock, client_addr)
			except KeyboardInterrupt as err:
				exit(0)
			except Exception as err:
				print(err)

	def _handle(self, sock, client_addr):
		global leader
		data = sock.recv(1024)
		if leader:
			sock.sendall(leader[0].encode())
		else:
			sock.sendall(b"ok")
			try:
				if sock.recv(1024) == b'leader':
					leader = client_addr[0]
			except OSError:
				print("#NotMyLeader")
				pass


	def _sender(self):
		global leader
		while 1:
			print("Meu lider é: ",leader)
			sleep(4)
			if leader and leader != self.conn:
				with socket(AF_INET, SOCK_STREAM) as s:
					s.settimeout(1)
					try:
						s.connect(leader)
						s.sendall(b"alive")
						s.recv(1024)
					except OSError:
						#leader dead
						leader = None
			else:
				handshakes = []
				for node in self.addr:
					print("Ping {}".format(node))
					with socket(AF_INET, SOCK_STREAM) as s:
						s.settimeout(1)
						try:
							s.connect(node)
							s.sendall(b"vote")
							data = s.recv(1024)
							#print(data)
							if data == b"ok":
								handshakes.append(node)
								#adicionar em uma lista de handshakes
								continue
							else:
								leader = (data.decode('utf-8'),1337)
								break; # GAMBIARRA
								#print(leader)
						except OSError:
							#node dead
							print("DeadNode")
				else: #no breaks
					leader = (argv[1], int(argv[2]))
					for hand in handshakes:
						with socket(AF_INET, SOCK_STREAM) as s:
							s.settimeout(1)
							try:
								s.connect(node)
								s.sendall(b"leader")
							except OSError:
								print("RIP Node :(")

if __name__ == "__main__":
	print("Starting Servidorzinho")
	Servidorzinho(("0.0.0.0", 1337),10)