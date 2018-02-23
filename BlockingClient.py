import datetime, socket


def get_ports():

    port1 = int(input('Enter Port1: '))
    port2 = int(input('Enter Port2: '))
    port3 = int(input('Enter Port3: '))

    return (port1, port2, port3)

def set_ports(portList):
    port1 = portList[0]
    port2 = portList[1]
    port3 = portList[2]

    return (port1, port2, port3)


def get_file(address):
    #function to download the file based on the host address and port number
    port, host = address
    sock = socket.socket()
    sock.connect((host,port))

    file = ''

    while True:

        # This is the 'blocking' call in this synchronous program.
        # The recv() method will block for an indeterminate period
        # of time waiting for bytes to be received from the server.

        data = sock.recv(1024).decode()

        if not data:
            sock.close()
            break

        file += data

    return file

def go_through_ports(ports):
    resultDict = {}
    for port in ports:
        print(port)
    totalTime = datetime.timedelta()

    for i, port in enumerate(ports):
        print('File {}: get poetry from: 127.0.0.1:{}'.format(i + 1, port))

        start = datetime.datetime.now()

        file = get_file((port,'localhost'))

        time = datetime.datetime.now() - start
        print('File #{}: got {} number of bytes from 127.0.0.1:{} in {}'.format(i + 1, len(file), port, time))
        resultDict[i+1] = time

        totalTime += time

    print('Got {} files in {}'.format(len(ports), totalTime))
    return totalTime


def main():
    ports = get_ports()
    go_through_ports(ports)

