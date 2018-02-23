import os, socket, time

def user_set_options():
    information_dict = {}
    information_dict['file'] = input('Enter file that you are trying to host on this server: ')
    information_dict['port'] = int(input('Enter Port: '))
    information_dict['bandwidth'] = int(input('How many bytes to send at a time (bandwidth: '))
    information_dict['latency'] = float(input('How many seconds to wait inbetween sending the num of bytes specified above (latency): '))


    if not os.path.exists(information_dict['file']):
        print("File not here! Try again")
        return None,None
    else:
        return information_dict

def script_set_options(filename, bandwidth, latency, port):
    information_dict = {}
    information_dict['file'] = filename
    information_dict['port'] = port
    information_dict['bandwidth'] = bandwidth
    information_dict['latency'] = latency

    if not os.path.exists(information_dict['file']):
        print("File not here! Try again")
        return None, None
    else:
        print('File found!')
        return information_dict

def terminate():
    exit()


def send_file(sock, file, bandwidth, latency):
    file_to_send = open(file)

    while True:
        bytes = file_to_send.read(bandwidth) # only read what the user specified to send per packet
        if not bytes: # we've read all of the bytes!
            sock.close() # close connection and file
            file_to_send.close()
            terminate()


        try:
            sock.sendall(bytes.encode()) # try sending the specified number of bytes, if something goes wrong close conn and file

        except socket.error:
            sock.close()
            file_to_send.close()
            return

        time.sleep(latency) # wait for the specified amount of time before going back up to the top of the loop to send
                          # more data


def serve(listen_socket, poetry_file, bandwidth, latency):
    print('Server Started!')
    while True:
        sock, addr = listen_socket.accept()

        print('Client connected at {}!'.format(str(addr)))

        send_file(sock, poetry_file, bandwidth, latency)

def set_up_server(information_dict):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #this is so the threading can get past the wait time
    sock.bind(('localhost', information_dict['port']))

    sock.listen(5)
    print('Serving {} on port {}'.format(information_dict['file'], information_dict['port']))

    serve(sock, information_dict['file'], information_dict['bandwidth'], information_dict['latency'])


def main():
    information_dict = user_set_options()
    set_up_server(information_dict)


