
import socket
import time
import statistics
import json

IP = "127.0.0.1"
N = 500
MESSAGE = b"x" * 100


# TCP Benchmark
tcp_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

tcp_socket.settimeout(3)

start = time.perf_counter()

tcp_socket.connect((IP, 5000))

handshake_time = (
    time.perf_counter() - start
) * 1000

tcp_times = []

for i in range(N):

    start = time.perf_counter()

    tcp_socket.sendall(MESSAGE)

    reply = tcp_socket.recv(1024)

    elapsed = (
        time.perf_counter() - start
    ) * 1000

    tcp_times.append(elapsed)

tcp_socket.close()


# UDP Benchmark
udp_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

udp_socket.settimeout(1)

udp_times = []
lost = 0

for i in range(N):

    start = time.perf_counter()

    udp_socket.sendto(
        MESSAGE,
        (IP, 5001)
    )

    try:
        reply, address = udp_socket.recvfrom(1024)

    except socket.timeout:
        lost += 1

    elapsed = (
        time.perf_counter() - start
    ) * 1000

    udp_times.append(elapsed)


# UDP without waiting for replies
start = time.perf_counter()

for i in range(N):

    udp_socket.sendto(
        b"NOACK" + MESSAGE,
        (IP, 5001)
    )

udp_noack_time = (
    time.perf_counter() - start
) * 1000

udp_socket.close()


# Calculate Results
results = {

    "Messages": N,

    "TCP Handshake Time (ms)": round(
        handshake_time, 4
    ),

    "TCP Average Time (ms)": round(
        statistics.mean(tcp_times), 4
    ),

    "TCP Minimum Time (ms)": round(
        min(tcp_times), 4
    ),

    "TCP Maximum Time (ms)": round(
        max(tcp_times), 4
    ),

    "TCP Total Time (ms)": round(
        sum(tcp_times), 4
    ),

    "UDP Average Time (ms)": round(
        statistics.mean(udp_times), 4
    ),

    "UDP Minimum Time (ms)": round(
        min(udp_times), 4
    ),

    "UDP Maximum Time (ms)": round(
        max(udp_times), 4
    ),

    "UDP Total Time (ms)": round(
        sum(udp_times), 4
    ),

    "UDP Lost Messages": lost,

    "UDP No-Reply Send Time (ms)": round(
        udp_noack_time, 4
    )
}


# Save Results
with open("bench.json", "w") as file:

    json.dump(results, file, indent=4)


# Display Report
print("\n========== TCP vs UDP REPORT ==========")

for key, value in results.items():

    print(f"{key}: {value}")

print("\nReport saved successfully as bench.json")
