# jarkom-tubes

Simple Python socket-based HTTP server experiment with two server modes:

- single-client handling (`server_single.py`)
- multi-client handling using threads (`server_multi.py`)

## Overview

This repository contains a basic HTTP file server and client scripts for testing requests.
The server listens on `127.0.0.1:8080`, serves files from the current directory, and returns file content for GET requests.

## Features

- Serves local files over HTTP using raw TCP sockets.
- Defaults `/` request path to `/index.html`.
- Returns `HTTP/1.1 404 Not Found` with body `File is not found.` when a file does not exist.
- Provides two server implementations:
  - `server_single.py`: handles one client at a time.
  - `server_multi.py`: handles each client in a separate daemon thread.
- Includes two client testers:
  - `client.py`: sends one HTTP GET request.
  - `multi_client.py`: sends 5 concurrent HTTP GET requests.

## Tech Stack

- Python 3
- Standard library modules only (`socket`, `threading`, `os`, `sys`, `time`)

## Setup and Run

Run commands from this repository root.

1. Start a server (choose one):

```bash
python3 server_single.py
```

or

```bash
python3 server_multi.py
```

2. In another terminal, run a single request client:

```bash
python3 client.py 127.0.0.1 8080 /index.html
```

3. Or run the concurrent client test:

```bash
python3 multi_client.py 127.0.0.1 8080 /test.html
```

## Project Structure

```text
jarkom-tubes/
├── server_single.py   # Single-connection HTTP file server
├── server_multi.py    # Multi-threaded HTTP file server
├── client.py          # Single HTTP request client
├── multi_client.py    # Concurrent HTTP request client (5 threads)
├── index.html         # Default file served for /
├── test.html          # Additional test file
└── README.md
```

## Notes

- The server serves files relative to the process working directory.
- No separate dependency installation is required.
