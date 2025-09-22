#%%
import socket

arduino_ip = "192.168.2.197"   # your Arduino's IP
arduino_port = 8080           # port you configured

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((arduino_ip, arduino_port))

#%%
sock.sendall(b'H')   # same as ser.write(b'H')
sock.close()