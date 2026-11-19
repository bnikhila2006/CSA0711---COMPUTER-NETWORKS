
import socket
import threading
import time

HOST = "127.0.0.1"
TCP_PORT = 5000
UDP_PORT = 5001


def log(message):
    print(
        f"[SERVER {time.strftime('%H:%M:%S')}] {message}",
        flush=True
    )


# Handle each TCP client
def handle_tcp_client(conn, addr):
    log(f"TCP connection ESTABLISHED with {addr}")

    try:
        with conn:
            while True:
                data = conn.recv(1024)

                if not data:
                    break

                message = data.decode()
                log(f"TCP received from {addr}: {message}")

                # Send acknowledgment
                reply = f"ACK: {message}"
                conn.sendall(reply.encode())

    except ConnectionError:
        log(f"Connection error with {addr}")

    finally:
        log(f"TCP connection CLOSED with {addr}")


# TCP Server
def tcp_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, TCP_PORT))
    server.listen(5)

    log(f"TCP server listening on {HOST}:{TCP_PORT}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_tcp_client,
            args=(conn, addr),
            daemon=True
        )

        thread.start()


# UDP Server
def udp_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, UDP_PORT))

    log(f"UDP server listening on {HOST}:{UDP_PORT}")

    while True:
        data, addr = server.recvfrom(1024)

        message = data.decode()

        log(f"UDP datagram from {addr}: {message}")

        # NOACK messages do not receive a reply
        if not message.startswith("NOACK"):
            reply = f"RECEIVED: {message}"
            server.sendto(reply.encode(), addr)


# Main Program
if __name__ == "__main__":

    tcp_thread = threading.Thread(
        target=tcp_server,
        daemon=True
    )

    udp_thread = threading.Thread(
        target=udp_server,
        daemon=True
    )

    tcp_thread.start()
    udp_thread.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        log("Server shutting down")
