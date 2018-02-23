import datetime, select, socket


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



def get_file(sockets, start):
    files_dict = {}

    for sock in sockets: # create empty dictionary for each socket to store whatever data we get while pulling asyncly
        files_dict[sock] = ('',start)

    # socket -> task numbers
    socketAndTask = {} # this dictionary is to keep track of the task numbers so we can properly switch between each one
    for i, s in enumerate(sockets):
        socketAndTask[s] = i + 1

    # we go around this loop until all the files are downloaded
    # from all the sockets. This is known as the 'reactor loop' in Twisted and is an essential part to async programming.

    while sockets:
        # rlist is almost the same format as our list of sockets in 'sockets', but is just a list of the sockets that
        # are ready for I/O
        rlist, __, __ = select.select(sockets, [], [])

        for sock in rlist:
            # if a socket is ready for I/O. then it is within our rlist, so we grab the data while it's avalible
            data = ''
            while True:
                try:
                    recieved_data = sock.recv(1024).decode()
                except socket.error as e:
                    if e.errno == 10035:
                        # this specific code only occurs when a socket, set to non-blocking, begins to block
                        # if we hit this error code, then we break, store the data we've gotten so far, and move
                        # to the next available socket in rlist
                        break
                    break
                else:
                    if not recieved_data:
                        break
                    else:
                        data += recieved_data

            task_num = socketAndTask[sock]

            if not data:
                sockets.remove(sock)
                sock.close()
                print('Finished task {} in {}'.format(task_num, files_dict[sock][1]))
            else:
                print('Task {}: got {} bytes of data'.format(task_num, len(data)))
            prevData = files_dict[sock][0]
            files_dict[sock] = (prevData + data, datetime.datetime.now() - start)

    return (files_dict, datetime.datetime.now() - start)


def connect(address):
    #connect to a specific server
    port, host = address
    sock = socket.socket()
    sock.connect((host, port))
    sock.setblocking(0)
    return sock

def go_through_ports(ports):
    #create the different sockets to connect to the different servers and ports

    start = datetime.datetime.now()

    sockets = [connect((port, 'localhost')) for port in ports]

    files, totalTime = get_file(sockets, start)

    for i, sock in enumerate(sockets):
        print('Task {}: {} bytes of text'.format(i + 1, len(files[sock])))

    print('Got {} files in {}'.format(len(ports), totalTime))
    return totalTime


def main():
    ports = get_ports()
    go_through_ports(ports)




