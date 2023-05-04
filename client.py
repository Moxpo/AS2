import socket
import sys
from common_utilities import download_file, upload_file, list_function, keyboard_to_socket, socket_to_screen

# Create the socket with which we will connect to the server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The server's address is a tuple, comprising the server's IP address or hostname, and port number
srv_addr = (sys.argv[1], int(sys.argv[2])) # sys.argv[x] is the x'th argument on the command line

# Convert to string, to be used shortly
srv_addr_str = str(srv_addr)

""" 
 Enclose the connect() call in a try-except block to catch
 exceptions related to invalid/missing command-line arguments, 
 port number out of range, etc. Ideally, these errors should 
 have been handled separately.
"""
try:
	print("Connecting to " + srv_addr_str + "... ")

	"""
	 Connect our socket to the server. This will actually bind our socket to
	 a port on our side; the port number will most probably be in the
	 ephemeral port number range and may or may not be chosen at random
	 (depends on the OS). The connect() call will initiate TCP's 3-way
	 handshake procedure. On successful return, said procedure will have
	 finished successfully, and a TCP connection to the server will have been
	 established.
	"""
	cli_sock.connect(srv_addr)
	
	print("Connected. Now chatting...")
except Exception as e:
	# Print the exception message
	print(e)
	# Exit with a non-zero value, to indicate an error condition
	exit(1)

"""
 Surround the following code in a try-except block to account for
 socket errors as well as errors related to user input. Ideally
 these error conditions should be handled separately.
"""
try:
	# Loop until either the server closes the connection or the user requests termination
	while True:
		userinput = input("What do you want? 1,2,3, 4?")
		castInput = int(userinput)
		if castInput == 1:
			download_file()
			break
		elif castInput == 2:
			upload_file()
			break
		elif castInput == 3:
			list_function()
			break
		elif castInput == 4:
			while True:
				# First, read data from keyboard and send to server
				bytes_sent = keyboard_to_socket(cli_sock)
				if bytes_sent == 0:
					print("User-requested exit.")
					break

				# Then, read data from server and print on screen
				bytes_read = socket_to_screen(cli_sock, srv_addr_str)
				if bytes_read == 0:
					print("Server closed connection.")
					break
		else:
			print("yolo")
			break
finally:
	cli_sock.close()

exit(0)
