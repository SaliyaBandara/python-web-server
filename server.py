import socket
import os
import subprocess
import tempfile

# Define the host and port to listen on
HOST = 'localhost'
PORT = 2728

# Define the path to the htdocs folder
HTDOCS_PATH = 'htdocs'

def convert_to_php_array(input_string, array_name='array'):
    # Split the string by '&' to separate key-value pairs
    key_value_pairs = input_string.split('&')
    php_array = {}

    # Loop through each key-value pair and split the pair into key and value using '='
    for pair in key_value_pairs:
        key, value = pair.split('=')
        php_array[key] = value

    # Convert the dictionary to a PHP array string
    php_array_string = f"<?php ${array_name} = array("
    for key, value in php_array.items():
        php_array_string += f"'{key}' => '{value}', "
    php_array_string = php_array_string.rstrip(', ')
    php_array_string += "); ?>"

    return php_array_string

def serve_php_file(client_socket, file_path, query_params=None, post_data=None):
    try:
        # Prepare environment variables for PHP script
        env = os.environ.copy()

        # Create a temporary PHP file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.php') as temp_php_file:
            try:
                if post_data:
                    # Convert the POST data to a PHP array
                    post_data_str = convert_to_php_array(post_data, '_POST')
                    temp_php_file.write(post_data_str)

                if query_params:
                    # Convert the query parameters to a PHP array
                    query_params_str = convert_to_php_array(query_params, '_GET')
                    temp_php_file.write(query_params_str)

                # Write the content of the PHP script file to the temporary file
                with open(file_path, 'r') as php_file:
                    temp_php_file.write(php_file.read())

            except Exception as e:
                client_socket.send(f"Error while preparing PHP script: {str(e)}".encode())
                return

        # Execute the temporary PHP script using the system's PHP interpreter
        result = subprocess.check_output(['php', temp_php_file.name], stderr=subprocess.STDOUT, env=env)

        # Delete the temporary PHP file
        os.remove(temp_php_file.name)

        client_socket.send(result)
        client_socket.close()

    except subprocess.CalledProcessError as e:
        # Handle any errors that occur during PHP script execution
        client_socket.send(f"Error: {e}".encode())
    except Exception as e:
        # Handle other exceptions
        client_socket.send(f"An error occurred: {str(e)}".encode())


def parse_request_data(request):
    # Parse GET and POST data from the HTTP request
    request_lines = request.split('\r\n')
    headers = request_lines[1:]

    # Initialize variables for storing GET and POST data
    file_path = ''
    request_type = ''
    query_params = ''
    post_data = ''

    if(len(request_lines) > 0):
        if(len(request_lines[0].split(" ")) > 1):
            file_path = request_lines[0].split(" ")[1]
        request_type = request_lines[0].split(" ")[0]

    # get request URL parameters 
    if request_type == "GET" and 1 < len(file_path.split("?")):   
        file_path,query_params = file_path.split("?")
        print(query_params)

    elif request_type == "POST":
        # Extract POST data from the POST request
        post_data = headers[-1]
        print(post_data)

    return query_params, post_data, file_path.lstrip('/')

def handle_client(client_socket):
    # request = client_socket.recv(1024).decode()
    request = client_socket.recv(4096).decode("utf-8")
    query_params, post_data, file_path = parse_request_data(request)

    if len(request) > 0:
        # Extract the requested file path from the HTTP request
        request_parts = request.split()
        if len(request_parts) >= 2:
            # if query_params is empty, then the request is not a GET request
            if not query_params:
                file_path = request_parts[1].lstrip('/')

            print(f"Request: {file_path}")
            
            if os.path.isdir(file_path) or file_path.endswith('/') or file_path == '':
                # check if index.php exists else check for index.html
                php_index_path = os.path.join(file_path, 'index.php')
                html_index_path = os.path.join(file_path, 'index.html')

                file_path = php_index_path if os.path.isfile(os.path.join(HTDOCS_PATH, php_index_path)) else html_index_path

            # Check if the requested file is a PHP file
            if file_path.endswith('.php'):
                php_file_path = os.path.join(HTDOCS_PATH, file_path)

                # Check if the PHP file exists
                if os.path.isfile(php_file_path):
                    # Serve the PHP file, passing query parameters
                    client_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                    serve_php_file(client_socket, php_file_path, query_params, post_data)
                else:
                    client_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                    client_socket.send("File Not Found".encode())
            else:
                # Serve static files (HTML, CSS) from the htdocs folder
                file_path = os.path.join(HTDOCS_PATH, file_path)
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        client_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                        client_socket.send(f.read())
                else:
                    client_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                    client_socket.send("File Not Found".encode())

    client_socket.close()

def main():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen(5)
    print(f"Listening on {HOST}:{PORT}...")

    try:
        while True:
            # Accept incoming client connections
            client_socket, client_address = server_socket.accept()
            print(f"\nAccepted connection from {client_address}")
            
            # Handle the client's request in a separate thread
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("Server shutting down.")
        server_socket.close()

if __name__ == "__main__":
    main()
