import socket
import sys
import threading
import time

# Number of concurrent requests
NUM_REQUESTS = 5

def make_request(server_host, server_port, filename, thread_id):
    """Make a single HTTP request"""
    start_time = time.time()
    
    # Create socket and connect to server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print(f"Thread {thread_id}: Connecting to {server_host}:{server_port}...")
        client_socket.connect((server_host, server_port))
        
        # Create and send HTTP GET request
        http_request = f"GET {filename} HTTP/1.1\r\nHost: {server_host}:{server_port}\r\n\r\n"
        print(f"Thread {thread_id}: Sending request: GET {filename}")
        client_socket.sendall(http_request.encode())
        
        # Receive server response
        print(f"Thread {thread_id}: Waiting for response...")
        response = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data
        
        # Print the status line from the HTTP response
        status_line = response.split(b'\r\n')[0].decode(errors='replace')
        print(f"Thread {thread_id}: Received: {status_line}")
        print(f"Thread {thread_id}: Completed in {time.time() - start_time:.2f} seconds")
        
    except Exception as e:
        print(f"Thread {thread_id} Error: {e}")
    finally:
        # Close the socket
        client_socket.close()

def main():
    # Check command line arguments
    if len(sys.argv) != 4:
        print("Usage: python multi_client.py server_host server_port filename")
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

    print(f"Starting {NUM_REQUESTS} concurrent requests to {server_host}:{server_port}")
    
    # Create threads for concurrent requests
    threads = []
    start_time = time.time()
    
    for i in range(NUM_REQUESTS):
        thread = threading.Thread(target=make_request, args=(server_host, server_port, filename, i))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    total_time = time.time() - start_time
    print(f"\nAll {NUM_REQUESTS} requests completed in {total_time} seconds total")

if __name__ == "__main__":
    main()
