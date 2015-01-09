import SocketServer
import os
import mimetypes
from time import ctime

http_res_codes = {
	'200': "OK"
	'404': "Not Found"
}

new_line = "\n"
connection_closed = "Connection: close"
accept_ranges = "Accept-Ranges: bytes"
server_type = "Server: python"
OK_response = "OK"

def is_subdirectory(path):
	cur_path = os.path.realpath(os.curdir)
	checked_path = os.path.realpath(cur_path + path)
	print ("data yo %s\n" % checked_path)
	return checked_path.startswith(os.curdir + os.sep)

def parse_path(str):
	str_list = str.split("\n") #split get call to extract the folder/file request
	get_str = str_list[0].split(" ")
	return get_str[1] if len(get_str) > 1 else " /../../.." #default the check to parent folder thus returning 404 error

def construct_response(code="404", path=None):
	#response follows the following format:
	# HTTP/1.1 200 OK
	# Date: Sun, 18 Oct 2009 08:56:53
	# Server: python
	# Last-Modified: Sat, 20 Nov 2004 07:16:26 GMT
	# Accept-Ranges: bytes
	# Content-Length: xxx
	# Connection: close
	# Content-Type: text/html

	status_line = "HTTP/1.1 " + code + " " + http_res_codes[code] + new_line
	general_header = "Date: " + ctime() + new_line + connection_closed + new_line
	response_header = accept_ranges + new_line + server_type + new_line
	response_str = status_line + general_header + response_header

	if (path != None):
		entity_header = "Content-Type: " + Content-Type + new_line + "Content-Length: " + len(Content-Length) + new_line
		response_str = response_str + entity_header + new_line + data

	return response_str


class MyWebServer(SocketServer.BaseRequestHandler):
	
	def serve_get(self):
		request_path = parse_path(self.data)
		if (is_subdirectory(request_path) == False):
			return construct_response()
		if (os.path.exists(request_path) == False):
			return construct_response()
		# need to throw above 404 data as error codes

		return construct_response(OK_response, request_path)
		# also need to return actual data

	def handle(self):
		self.data = self.request.recv(1024).strip()
		print ("Got a request of: %s\n" % self.data)
		test_data = self.serve_get()
		print ("Data sent: %s\n" % test_data)
		self.request.sendall(test_data)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
