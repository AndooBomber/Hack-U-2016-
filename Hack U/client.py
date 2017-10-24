import time
import os
import base64
import socket
import struct
import array


def make_ws_data_frame(data):
    FIN = 0x80
    RSV1 = 0x0
    RSV2 = 0x0
    RSV3 = 0x0
    OPCODE = 0x1
    MASK = 0x80
    payload = 0x0

    frame = struct.pack('B', FIN | RSV1 | RSV2 | OPCODE)
    data_len = len(data)
    if data_len <= 125:
        payload = struct.pack('B', MASK | data_len)
    elif data_len < 0xFFFF:
        payload = struct.pack('!BH', 126 | MASK, data_len)
    else:
        payload = struct.pack('!BQ', 127 | MASK, data_len)

    frame += payload
    masking_key = os.urandom(4)
    mask_array = array.array('B', masking_key)
    unmask_data = array.array('B', data.encode('UTF-8'))

    for i in range(data_len):
        unmask_data[i] = unmask_data[i] ^ masking_key[i % 4]

    mask_data = unmask_data.tobytes()
    frame += masking_key
    frame += mask_data

    return [frame, len(frame)]

HTTP_GET = """GET / HTTP/1.1\r
Connection: Keep-Alive\r
\r\n"""

ws_upgrade_header = {
    'Upgrade' : 'websocket',
    'Connection' : 'Upgrade',
    'Sec-WebSocket-Key' : base64.b64encode(os.urandom(16)).decode('UTF-8'),
    'Sec-WebSocket-Version' : '13',
}

sock = socket.create_connection(['my.domain.com', 8080])

sock.send(HTTP_GET.encode('UTF-8'))

recv_buf = ""
recv_buf = sock.recv(4096)

print(recv_buf.decode('UTF-8'))

headers = "GET /ws HTTP/1.1\r\nHost: my.domain.com\r\n"
for key in ws_upgrade_header:
    headers += key + ": " + ws_upgrade_header[key] + "\r\n"

headers += "\r\n"

print(headers)

sock.send(headers.encode('UTF-8'))

time.sleep(1)

recv_buf = sock.recv(4096)
print(recv_buf.decode('UTF-8'))

time.sleep(1)

message, message_len = make_ws_data_frame('Hello')

sock.send(message)

sock.close()
