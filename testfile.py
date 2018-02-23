import AsynchronousClient as AC
import BlockingClient as BC
import BlockingServer as BS
import threading
import pandas as pd
import random

def simulateServers(resultTable, bandwidth, latency, portList, fileList, index):
    threads = []

    #creates three threads that spin up three different servers on 3 different ports
    #we need the threads because the servers are set up to continuously listen, so the threads make it so that we
    #can have multiple running at the same time.
    for i in range(3):
        information_dict = BS.script_set_options(fileList[i], bandwidth, latency, portList[i])
        t1 = threading.Thread(target=BS.set_up_server, args=(information_dict,))
        threads.append(t1)
        t1.start()

    ports = BC.set_ports(portList)#call blocking client's set ports to make the connections
    BCTime = BC.go_through_ports(ports)#call blocking client's function to dl the files and everything else
    #after the 'BC.go_through_ports() function finished we shut down all 3 servers and start them up again for the
    #async client

    for i in range(3):
        information_dict = BS.script_set_options(fileList[i], bandwidth, latency, portList[i])
        t1 = threading.Thread(target=BS.set_up_server, args=(information_dict,))
        threads.append(t1)
        t1.start()

    ports = AC.set_ports(portList) #call Async client's set ports to make the connections
    ACTime = AC.go_through_ports(ports)

    #returns the tables after theyve been updated with the relevant information
    #we pass in all relevant information like bandwidth, latency, times, etc. to be recorded in the dataframe
    return outPut(resultTable, bandwidth, latency, BCTime, ACTime, index)


def outPut(resultTable, bandwidth, latency, BCTime, ACTime, index): #function for getting the results back from the
    #servers and clients; it updates the pandas df every iteration of 'simulateServers'
    BCTable, ACTable = resultTable

    #updates the pandas array
    BCTable[index][0] = latency
    BCTable[index][1] = bandwidth
    BCTable[index][2] = BCTime

    ACTable[index][0] = latency
    ACTable[index][1] = bandwidth
    ACTable[index][2] = ACTime

    resultTable = (BCTable, ACTable)
    return resultTable




def testTwoRandGrowth(resultTable, portList, fileList):

    for i in range(25):
        bandwidth = random.randint(10,150) #sets the bandwidth to a random number between 10 and 150 bytes
        print('BANDWIDTH: {}'.format(bandwidth))
        latency = random.uniform(.1,1) #sets the latency to be a random number between .1 and 1 second
        print('LATENCY: {}'.format(latency))
        resultTable = simulateServers(resultTable, bandwidth, latency, portList, fileList, i) #interface with the clients
        print(resultTable)
    filename1 = 'RandAsynch.csv'
    filename2 = 'RandBlocking.csv'
    resultTable[0].to_csv(filename2)
    resultTable[1].to_csv(filename1)


def testOneLinearGrowth(resultTable, portList, fileList):
    bandwidth = 10 # initalize bandwidth and latency for test
    latency = .1

    for i in range(25):
        print('BANDWIDTH: {}'.format(bandwidth))
        print('LATENCY: {}'.format(latency))
        resultTable = simulateServers(resultTable, bandwidth, latency, portList, fileList, i) #call simulation func for
                                                                                              #linear growth
        bandwidth += 5
        latency += .07

    #save the results in csv files
    filename2 = 'LinearAsynch.csv'
    filename1 = 'LinearBlocking.csv'
    resultTable[0].to_csv(filename1)
    resultTable[1].to_csv(filename2)


def main():
    rows = ['latency', 'bandwidth', 'time'] #rows for the data table
    columns = [i for i in range(25)] # columns numbered 0 - 24 for iterations of server-client relations

    frame = pd.DataFrame([[None for x in range(25)],
                          [None for x in range(25)],
                          [None for x in range(25)]
                          ])
    BCTable = pd.DataFrame(frame, index=rows, columns=columns) #create table for Blocking Client

    ACTable = pd.DataFrame(frame, index=rows, columns=columns) #create table for Async Client
    resultTable = (BCTable, ACTable) #merge the two together in a tuple

    portList = [8001,8101,8201] #the ports for which we will be hosting our servers
    fileList = ['file1.txt', 'file2.txt', 'file3.txt'] #files that we are sharing


    # We'll be running two tests on the servers to simualate various network traffic
    # the first test will up the bandwidth and latency by a constant amount (+5 and +.1) respectively
    # the other test, 'testTwoRandGrowth' will change the bandwidth randomly between 1-150 and the latency
    # will be anywhere from .1 - 5. Both functions run 25 times each and output their results to different
    # csv files.

    #testOneLinearGrowth(resultTable, portList, fileList)
    #testTwoRandGrowth(resultTable, portList, fileList)
    demo(50,.2,portList,fileList)




def demo(bandwidth, latency, portList, fileList):

    threads = []

    # creates three threads that spin up three different servers on 3 different ports
    # we need the threads because the servers are set up to continuously listen, so the threads make it so that we
    # can have multiple running at the same time.
    for i in range(3):
        information_dict = BS.script_set_options(fileList[i], bandwidth, latency, portList[i])
        t1 = threading.Thread(target=BS.set_up_server, args=(information_dict,))
        threads.append(t1)
        t1.start()

    ports = BC.set_ports(portList)  # call blocking client's set ports to make the connections
    BCTime = BC.go_through_ports(ports)  # call blocking client's function to dl the files and everything else
    # after the 'BC.go_through_ports() function finished we shut down all 3 servers and start them up again for the
    # async client

    for i in range(3):
        information_dict = BS.script_set_options(fileList[i], bandwidth, latency, portList[i])
        t1 = threading.Thread(target=BS.set_up_server, args=(information_dict,))
        threads.append(t1)
        t1.start()

    ports = AC.set_ports(portList)  # call Async client's set ports to make the connections
    ACTime = AC.go_through_ports(ports)


if __name__ == '__main__':
    main()