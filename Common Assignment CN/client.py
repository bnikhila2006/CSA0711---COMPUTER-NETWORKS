
import socket
import sys
import time


# TCP Communication
def tcp_send(cid, ip, port, messages):

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.settimeout(3)

    try:
        start = time.perf_counter()

        client.connect((ip, port))

        handshake_time = (
            time.perf_counter() - start
        ) * 1000

        print(
            f"[{cid}] Connection Status: CONNECTED "
            f"to {ip}:{port} "
            f"(handshake {handshake_time:.3f} ms)"
        )

        times = []

        for message in messages:

            start = time.perf_counter()

            client.sendall(
                f"{cid}: {message}".encode()
            )

            reply = client.recv(1024).decode()

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            times.append(elapsed)

            print(
                f"[{cid}] Sent: {message} | "
                f"Received: {reply} | "
                f"Time: {elapsed:.3f} ms | "
                f"ACK: RECEIVED"
            )

        return times

    finally:
        client.close()
        print(f"[{cid}] Connection Status: CLOSED")


# UDP Communication
def udp_send(cid, ip, port, messages):

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    client.settimeout(1)

    times = []

    try:
        for message in messages:

            start = time.perf_counter()

            client.sendto(
                f"{cid}: {message}".encode(),
                (ip, port)
            )

            try:
                data, address = client.recvfrom(1024)

                reply = data.decode()

                ack = "RECEIVED (application-level)"

            except socket.timeout:

                reply = "-"

                ack = "NO REPLY (packet may be lost)"

            elapsed = (
                time.perf_counter() - start
            ) * 1000

            times.append(elapsed)

            print(
                f"[{cid}] Sent: {message} | "
                f"Received: {reply} | "
                f"Time: {elapsed:.3f} ms | "
                f"ACK: {ack}"
            )

        return times

    finally:
        client.close()


# Main Program
if __name__ == "__main__":

    if len(sys.argv) < 5:
        print(
            "Usage: python client.py "
            "<client_id> <server_ip> <TCP|UDP> "
            "<message> [count]"
        )
        sys.exit(1)

    cid = sys.argv[1]
    ip = sys.argv[2]
    protocol = sys.argv[3].upper()
    message = sys.argv[4]

    count = int(sys.argv[5]) if len(sys.argv) > 5 else 1

    if count < 1:
        print("Message count must be at least 1")
        sys.exit(1)

    messages = [
        f"{message} #{i+1}"
        for i in range(count)
    ]

    if protocol == "TCP":

        tcp_send(cid, ip, 5000, messages)

    elif protocol == "UDP":

        udp_send(cid, ip, 5001, messages)

    else:

        print("Invalid protocol. Choose TCP or UDP.")
