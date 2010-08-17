#!/usr/bin/env python

def tcpSend(host=None, port=None, data=None, receive=False, buffer=1024):
    import socket

    tcp_ip = host
    tcp_port = port
    tcp_buffer = buffer
    data_to_send = data
    data_received = ""

    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((tcp_ip, tcp_port))
    except Exception:
        print "Error setting up connection"
        raise

    try:
        connection.send(data_to_send)
        if receive:
            while True:
                data_incoming = connection.recv(tcp_buffer)
                if(not len(data_incoming)):
                    break
                data_received += data_incoming

    except Exception:
        print "Error sending/receiving data"
        raise

    if connection:
        connection.close()

    if receive:
        return data_received


def mimicNetCat(host=None, port=None, data=""):
    from sys import stdin

    while True:
        data += stdin.read()
        if(not stdin.closed):
            break

    print tcpSend(host, port, data, receive=True)



if __name__ == "__main__":
    import optparse
    parser = optparse.OptionParser()
    options, args = parser.parse_args()

    host = args[0]
    port = int(args[1])

    mimicNetCat(host, port)
