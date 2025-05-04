import socket
import http

HOST = ""
PORT = 8888

with socket.socket() as s:
    print(f"Connecting to {HOST}:{PORT}")
    s.bind((HOST, PORT))
    s.listen()

    while True:
        print("\nWaiting request...")
        connection, address = s.accept()
        print("Connection from", address)

        data = connection.recv(1024)
        data = data.decode().strip()
        print(f"\nReceived data: \n{data}\n")

        status_value = 200
        status_phrase = "OK"
        status = None

        try:
            status = int(data.split()[1].split("status=")[1])

            status_value = http.HTTPStatus(status)
            status_phrase = http.HTTPStatus(status_value).phrase

        except Exception:
            print(f"Info: recieved status code = {status}")

        status_line = f"{data.split()[2]} {status_value} {status_phrase}"

        response = "\r\n".join(data.split("\r\n")[1:])

        connection.send(
            f"{status_line}\r\n\r\n"
            f"Request Method: {data.split()[0]}\r\n"
            f"Request Source: {address}\r\n"
            f"Response Status: {status_value} {status_phrase}\r\n"
            f"{response}".encode()
        )

        connection.close()
