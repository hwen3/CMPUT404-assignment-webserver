import SocketServer
import os
import mimetypes
from time import ctime

# coding: utf-8
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright (c) 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py
# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

	HTTP_RES_CODES = {
	'200': "OK",
	'404': "Not Found"
	}

	STATUS_FORMAT = "HTTP/1.1 {} {} \r\n"
	GENERAL_HEADER_FORMAT = "Date: {} \r\nConnection: close \r\n"
	RESPONSE_HEADER_FORMAT = "Accept-Ranges: bytes \r\nServer: python \r\n"
	ENTITY_HEADER_FORMAT = "Content-Type: {} \r\nContent-Length: {} \r\n"
	CRLF = "\r\n"
	OK_RESPONSE = "200"
	SERVER_MAIN_PATH = os.path.realpath(os.curdir) + "/www"

	def is_subdirectory(self, path):
		checked_path = os.path.realpath(self.SERVER_MAIN_PATH + path)
		return checked_path.startswith(self.SERVER_MAIN_PATH)

	def parse_path(self, str):
		str_list = str.split("\n") #split get call to extract the folder/file request
		get_str = str_list[0].split(" ")
		return self.SERVER_MAIN_PATH + get_str[1] if len(get_str) > 1 else " /../../.." #default the check to parent folder thus returning 404 error

	def construct_response(self, code="404", path=None):
		#response follows the following format:
		# HTTP/1.1 200 OK
		# Date: Sun, 18 Oct 2009 08:56:53
		# Server: python
		# Last-Modified: Sat, 20 Nov 2004 07:16:26 GMT
		# Accept-Ranges: bytes
		# Content-Length: xxx
		# Connection: close
		# Content-Type: text/html

		response_str = self.STATUS_FORMAT.format(code, self.HTTP_RES_CODES[code]) + \
			self.GENERAL_HEADER_FORMAT.format(ctime()) + \
			self.RESPONSE_HEADER_FORMAT

		if (path != None):
			mimetypes.init()
			file_data = ""
			content_type = mimetypes.guess_type(path)[0]
			with open(path) as req_file:
				file_data += req_file.read()
			response_str += self.ENTITY_HEADER_FORMAT.format(content_type, len(file_data)) + self.CRLF + file_data
		else:
			response_str += self.CRLF


		return response_str

	
	def serve_get(self):
		request_path = self.parse_path(self.data)
		if (self.is_subdirectory(request_path) == False):
			return self.construct_response()
		if (os.path.exists(request_path) == False):
			return self.construct_response()
		if (os.path.isdir(request_path)):
			request_path += "index.html"

		return self.construct_response(self.OK_RESPONSE, request_path)

	def handle(self):
		self.data = self.request.recv(1024).strip()
		self.request.sendall(self.serve_get())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
