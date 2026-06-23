#!/usr/bin/env python3

# load_balancer_monitor_idiab1.py
# Author: Ibrahim Diab

# Imports the subprocess module, allowing commands to be ran in the terminal/shell (i.e. ping)
# The commands you use are dependent on the OS you're using
import subprocess

# A class for a node, which is representing a machine in a network
class Node:
        # This method simply has an IPv4 address, which is declared for testing after this class
        def __init__(self, nodeIP):
            self.IP = nodeIP

        # IPv4 addresses get checked here to see if they are valid
        # They get split into 4 parts
        def canExist(self):
            validIP = self.IP
            octets = validIP.split(".")

            # If the IP does not have 4 octets, it is not valid
            if len(octets) != 4:
                return False

            # Since IPv4 addresses have 4 octets, we declare them in a list
            octet1 = octets[0]
            octet2 = octets[1]
            octet3 = octets[2]
            lastoctet = octets[3]

            # The first and last octet in IPv4 addresses cannot be 0
            # Otherwise it is invalid
            if octet1 == "0" or lastoctet == "0":
                return False

            # IPv4 addresses can only contain integers, otherwise it's invalid
            # Every octet (except the first and last) must be higher than or equal to 0, and less than 255
            # Otherwise it is invalid
            for octet in octets:
                if octet.isdigit() != True:
                    return False
                num = int(octet)
                if num < 0 or num >= 255:
                    return False
            # The IPv4 address is valid if the loop finishes without returning False
            return True

        # This method pings the IP stored, it waits 2 seconds for a reply
        # If it's successful, it returns true
        # Otherwise, it returns false
        def isRunning(self):
            status, output = subprocess.getstatusoutput('ping -W 2 -c 1 ' + self.IP)

            if status == 0:
                return True
            else:
                return False

# The nodes IP is declared here for testing purposes
# This is not to be confused with the masters IP address
node = Node("192.168.20.60")

# This is the load balancer itself
class LoadBalancerMonitor:
    # This method declares the network address,
    # the master server,
    # and a list of slaves
    def __init__(self, networkAdress, bitmask, master):
        self.networkAdress = networkAdress
        self.bitmask = bitmask
        self.master = master
        self.slaves = []

    # Before a slave is added to the node, it needs to be checked
    # It calls node.canExist() to check if it's valid or invalid
    # The node is added to the slaves list only if the IP is valid
    def addSlave(self, node):
        if node.canExist() == True:
            self.slaves.append(node)
        else:
            print('Error. Unable to add this node to the slaves list.')

    # This method just checks if the node is already in the list and removes
    # it, or it prints an error if it isn't in the list
    def removeSlave(self, node):
        if node in self.slaves:
            self.slaves.remove(node)
        else:
            print('Error. Unable to remove this node from the slaves list.')

    # This prints a title with leading equal signs such that if the title changes,
    # the number of equal signs will change to match the length of the new title
    def menu_title(self, title):
        print()
        print(title)
        print('=' * len(title))

    # We check if the slaves are online by declaring
    # 2 variables and checking them against slave.isRunning()
    # Trailing dots are also added for each node that is checked
    # They get printed in the title, and 1 dot means 1 node is being checked
    def getStatus(self):
        onlineCount= 0
        offlineCount = 0

        print('Checking', end="", flush=True)
        for slave in self.slaves:
            if slave.isRunning() == True:
                onlineCount += 1
                print(".", end="", flush=True)
            else:
                offlineCount += 1
                print(".", end="", flush=True)

        # We check if the master is online by checking masterStatus against
        # self.master.isRunning()
        masterStatus = "Online" if self.master.isRunning() else "Offline"

        # The menu is printed here with a title and the status of the master
        # and the slaves are printed here as well
        print()
        self.menu_title('Load Balancer Status')
        print('Master: ' + masterStatus)
        print('Slaves: ' + str(onlineCount) + ' ONLINE, ' + str(offlineCount) + ' OFFLINE')

# The classes are tested by adding a bunch of test IPs into a list that are invalid and valid
# Every IPv4 address except the last one are all invalid for different reasons (i.e. first and last
# octet are 0, one octet is higher than 255 or one octet isn't an integer, etc.)
testIPS = [
    "0.16.3.5",
    "192.168.0.0",
    "10.300.9.1",
    "abc.1.2.3",
    "192.168.1",
    "172.16.42.14"
    ]

# We loop through all the IPs with the node testing IP
# by testing it against node.canExist() and printing the result
for ip in testIPS:
    node = Node(ip)
    print(ip + ": " + str(node.canExist()))

# We declare the master IP to be googles DNS server (this can be changed depending on your system needs)
# The load balancer monitor is declared here as well and we set the network address, self.bitmask and self.master accordingly
# The result is printed at the end by checking the master against isRunning()
master = Node("8.8.8.8")
monitor = LoadBalancerMonitor("8.8.8.0", 24, master)
print("The status of the master IP is: " + str(master.isRunning()))

# Adds slaves to the node for testing
# 3 IPs are online because 2 of them are popular DNS servers and the other is a loopback address
# The last IP will appear offline because it is a private IP
monitor.addSlave(Node("127.0.0.1"))
monitor.addSlave(Node("1.1.1.1"))
monitor.addSlave(Node("208.67.222.222"))
monitor.addSlave(Node("203.0.113.44"))

# After the testing is successful, we call the getStatus() method against the monitor variable
# This is what prints the final result after all the above test IPs are successfully tested
monitor.getStatus()
