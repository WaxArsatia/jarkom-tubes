import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 8080

def handle_client(client_socket: socket.socket, client_address):
    print(f"Connection from {client_address}")
    
    try:
        # Receive client request
        request_data = client_socket.recv(4096).decode()
        
        if not request_data:
            return
            
        # Parse request to get file path
        request_line = request_data.split('\n')[0]
        method, path, _ = request_line.split(' ')
        
        # Set default path to index.html if root is requested
        if path == '/':
            path = '/index.html'
        
        # Remove leading slash
        file_path = path[1:]
        
        # Check if file exists and has .html extension
        if os.path.isfile(file_path) and file_path.endswith('.html'):
            # Read file content
            with open(file_path, 'rb') as file:
                content = file.read()
            
            # Create HTTP response
            header = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n"
            client_socket.sendall(header.encode() + content)
        else:
            # File not found - return 404
            not_found = "<html><body><h1>404 Not Found</h1></body></html>"
            header = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(not_found)}\r\n\r\n"
            client_socket.sendall(header.encode() + not_found.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server running on http://{HOST}:{PORT}")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
