import socket
import threading
import os

#TODO: Add time sleep / timestamp

HOST = '127.0.0.1'
PORT = 8080

def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")
    
    # Receive client request
    request_data = client_socket.recv(4096).decode()
    
    if not request_data:
        client_socket.close()
        return
    
    # Parse request to get file path
    request_line = request_data.split('\n')[0]
    try:
        method, path, _ = request_line.split(' ')
    except ValueError:
        client_socket.close()
        return
    
    # Set default path to index.html if root is requested
    if path == '/':
        path = '/index.html'
    
    # Remove leading slash
    file_path = path[1:]
    
    # Check if file exists
    if os.path.isfile(file_path) and file_path.endswith('.html'):
        # Read file content
        with open(file_path, 'rb') as file:
            content = file.read()
        
        # Create HTTP response
        response = f"HTTP/1.1 200 OK\r\n"
        response += f"Content-Type: text/html\r\n"
        response += f"Content-Length: {len(content)}\r\n"
        response += "\r\n"
        
        # Send headers and content
        client_socket.send(response.encode())
        client_socket.send(content)
    else:
        # File not found - return 404
        not_found = "<html><body><h1>404 Not Found</h1><p>The requested file was not found on this server.</p></body></html>"
        response = f"HTTP/1.1 404 Not Found\r\n"
        response += f"Content-Type: text/html\r\n"
        response += f"Content-Length: {len(not_found)}\r\n"
        response += "\r\n"
        
        client_socket.send(response.encode())
        client_socket.send(not_found.encode())
        
    # Close connection
    client_socket.close()
    print(f"Connection with {client_address} closed")

def start_server():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind to port
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server running on http://localhost:{PORT}")
    
    try:
        while True:
            # Accept client connection
            client_socket, client_address = server_socket.accept()
            
            # Create new thread to handle client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
