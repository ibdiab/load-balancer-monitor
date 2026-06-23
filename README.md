A basic load balancer monitor written in python. It has basic functions such as:
  - Declaring the node's IP for testing
  - Declaring random IPs for testing the node class
  - Declaring the master's IP
  - Adding/removing slave IPs for testing
    
# INSTALLATION INSTRUCTIONS
1. If you don't have python installed, install it here: https://www.python.org/
  - For MacOS users, check if you have python installed with
    
    ```
    python3 --version
    ```
    If this command fails or prompts you to install dev tools, install it via homebrew

    ```
    brew install python3
    ```
  - For Linux users, check if you have python installed with
    
    ```
    python3 --version
    ```
    If this command fails, update your system to get the latest packages and then install it via your package manager:

    **Debian/Ubuntu**
    
    ```
    sudo apt update; sudo apt upgrade; sudo apt install python3
    ```
    **Fedora**
    
    ```
    sudo dnf upgrade; sudo dnf install python3
    ```
    **Arch**
    
    ```
    sudo pacman -Syu python
    ```
    **Other distros**
    If your distro isn't listed here, please install it via your distros package manager.
    
2. Install `load_balancer_monitor.py` from the repository.
   
3. You may then open the file in your preferred IDE or follow the instructions below to run it via terminal depending on your OS:
   
4. On **Windows**, open command prompt or PowerShell and navigate to the directory you installed this. (ex.
   
    ```
    cd C:\Users\user\Downloads
    ```
    )
Run the script with

    ```
    py load_balancer_monitor.py
    ```
    or
    ```
    python load_balancer_monitor.py
    ```
On **MacOS/Linux**, open terminal and navigate to the directory you installed it:
  - MacOS: ex.
    
    ```
    cd /Users/user/Downloads
    ```
  - Linux: ex.
    
    ```
    cd /home/user/Downloads
    ```
From there, give the script executable permissions with

    ```
    chmod +x load_balancer_monitor.py
    ```
    , then run it with
    ```
    ./load_balancer_monitor.py
    ```
# EDITING THE IPs

- ```
  node = Node("192.168.20.60")
  ```
  The node's IP is declared here for testing, the IP address here doesn't matter as long it's a valid IPv4 address.
  
- ```
  testIPS = [
    "0.16.3.5",
    "192.168.0.0",
    "10.300.9.1",
    "abc.1.2.3",
    "192.168.1",
    "172.16.42.14"
    ]
  ```
  These are random IP addresses used for testing the classes. Every address except the last one are invalid for various reasons (ex. one octet isn't an integer, first octet is 0, etc.).
- ```
  master = Node("8.8.8.8")
    monitor = LoadBalancerMonitor("8.8.8.0", 24, master)
  ```
  The master's IP is declared here (in this case it's Google's DNS server, this can be changed depending on your requirements). The load balancer monitor is also declared and we set the network address (in this case again it's Google's DNS).
- ```
  monitor.addSlave(Node("127.0.0.1"))
    monitor.addSlave(Node("1.1.1.1"))
    monitor.addSlave(Node("208.67.222.222"))
    monitor.addSlave(Node("203.0.113.44"))
  ```
  These are slaves used for testing. You can add or remove them. In this case, 3 of them are online as they are DNS servers and the other is a loopback address. The last IP is a private IP, so it will appear offline. Again, feel free to change this based on your requirements.
