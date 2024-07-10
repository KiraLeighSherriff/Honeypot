import socket

  
# This file is for responding to the commands that are entered by the user in the SSH terminal 
# it will include some of the most common commands done when a user ssh into a computer for the fist
# time. This file was made separate from ssh_server so it is more easily read and modified by adding 
# more elif statement if need 
   
   
class TelnetCommands():
    def __init__(self):
        pass
        
       
    def HandleCommands(self, commands, channel):
        
        
        response = " "
            
        if commands == "whoami":
            response = "guest\r\n"  
        
        elif 'cd' in commands:
            response = "permission denied\r\n" 
        
        elif 'rm' in commands:
            response = "permission denied\r\n" 
        
        elif 'mv' in commands:
            response = "permission denied\r\n" 
            
        elif 'cp' in commands:
            response = "permission denied\r\n" 
            
        elif 'cat' in commands:
            response = "permission denied\r\n" 
              
        elif commands == "touch":
            response = "permission denied\r\n" 
            
        elif commands == "mkdir":
            response = "permission denied\r\n" 
            
        elif commands == "mkdir":
            response = "permission denied\r\n" 
            
        elif commands == "pwd":
            response = "/ \r\n" 
             
        elif 'sudo' in commands:
            response = "guest is not in the sudoers file. This incident will be reported.\r\n"  
            
        elif commands == "ls":
            response = " . \r\n .. \r\n bin/ \r\n dev/ \r\n home/ \r\n lost+found/ \r\n mnt/ \r\n proc/ \r\n run/ \r\n srv/ \r\n tmp/ \r\n var/ \r\n boot/ \r\n etc/ \r\n lib/ \r\n media/ \r\n opt/ \r\n root/ \r\n sbin/ \r\n sys/ \r\n usr/ \r\n"  
            
        elif commands == "ls -la":
            response = """total 68 \r
drwxr-xr-x  18 root root  4096 Jan 30 06:16 . \r
drwxr-xr-x  18 root root  4096 Jan 30 06:16 .. \r
lrwxrwxrwx   1 root root     7 Dec 11 01:03 bin -> usr/bin \r
drwxr-xr-x   3 root root  4096 Jan 30 06:42 boot \r
drwxr-xr-x  16 root root  3640 Jan 22 08:41 dev \r
drwxr-xr-x 100 root root  4096 Feb  7 21:33 etc \r
drwxr-xr-x   3 root root  4096 Dec 11 01:07 home \r
lrwxrwxrwx   1 root root     7 Dec 11 01:03 lib -> usr/lib \r
drwx------   2 root root 16384 Dec 11 01:23 lost+found \r
drwxr-xr-x   2 root root  4096 Dec 11 01:03 media \r
drwxr-xr-x   2 root root  4096 Dec 11 01:03 mnt \r
drwxr-xr-x   4 root root  4096 Jan  2 18:56 opt \r
dr-xr-xr-x 149 root root     0 Jan  1  1970 proc \r
drwx------   4 root root  4096 Jan 22 21:34 root \r
drwxr-xr-x  25 root root   820 Feb 10 18:59 run \r
lrwxrwxrwx   1 root root     8 Dec 11 01:03 sbin -> usr/sbin \r
drwxr-xr-x   2 root root  4096 Dec 11 01:03 srv \r
dr-xr-xr-x  12 root root     0 Jan  1  1970 sys \r
drwxrwxrwt  10 root root  4096 Feb 10 18:41 tmp \r
drwxr-xr-x  11 root root  4096 Dec 11 01:03 usr \r
drwxr-xr-x  12 root root  4096 Jan  2 18:30 var \r\n"""
        
        
        elif commands == "ifconfig":
            # Get the IP address of the host machine make it more realistic 
            ip = socket.gethostbyname(socket.gethostname())
            response = (f"""
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536 \r\n
    inet 127.0.0.1  netmask 255.0.0.0 \r
    inet6 ::1  prefixlen 128  scopeid 0x10<host> \r
    loop  txqueuelen 1000  (Local Loopback) \r
    RX packets 73974  bytes 6948501 (6.6 MiB) \r
    RX errors 0  dropped 0  overruns 0  frame 0 \r
    TX packets 73974  bytes 6948501 (6.6 MiB) \r
    TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0 \r
    
    \r\n
wg0: flags=209<UP,POINTOPOINT,RUNNING,NOARP>  mtu 1420 \r\n
    inet 10.246.229.1  netmask 255.255.255.0  destination 10.246.229.1 \r
    unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC) \r
    RX packets 29448  bytes 5280280 (5.0 MiB) \r
    RX errors 148  dropped 0  overruns 0  frame 148 \r
    TX packets 34783  bytes 28407576 (27.0 MiB) \r
    TX errors 0  dropped 237 overruns 0  carrier 0  collisions 0 \r

    \r\n
wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500 \r\n
    inet {ip}  netmask 255.255.255.0  broadcast 192.168.1.255 \r
    inet6 fe80::19e4:e351:21b2:b657  prefixlen 64  scopeid 0x20<link> \r
    ether b8:27:eb:01:69:ff  txqueuelen 1000  (Ethernet) \r
    RX packets 2964975  bytes 528404354 (503.9 MiB) \r
    RX errors 0  dropped 488952  overruns 0  frame 0 \r
    TX packets 1028378  bytes 160837221 (153.3 MiB) \r
    TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0 \r 
    \r\n""")  
            
        else:
            response = "Command is unknown.\r\n"
              
        # convert the response to byte so it can be sent though the socket         
        byte_response = bytes(response, 'utf8')   
        channel.send(byte_response)