import socket
import sys

def main():
    # Check command line arguments
    if len(sys.argv) != 4:
        print("Usage: python client.py server_host server_port filename")
        sys.exit(1)
    
    # Parse command line arguments
    server_host = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("Error: Port must be an integer")
        sys.exit(1)
    filename = sys.argv[3]
    
    # Ensure filename starts with a slash
    if not filename.startswith('/'):
        filename = '/' + filename

    # Create socket and connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"Connecting to {server_host}:{server_port}...")
        client_socket.connect((server_host, server_port))
        
        # Create and send HTTP GET request
        http_request = f"GET {filename} HTTP/1.1\r\nHost: {server_host}:{server_port}\r\n\r\n"
        print(f"Sending request: GET {filename}")
        client_socket.sendall(http_request.encode())
        
        # Receive and display server response
        print("Waiting for response...")
        response = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data
        
        # Print the HTTP response
        print("\n--- HTTP Response ---")
        print(response.decode(errors='replace'))
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    main()
