import zmq
from zmq import REQ

context = zmq.Context()

# socket to talk to server

print("connecting to remote jobs server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

variable = 'python'

# do something
socket.send_string(variable)
print("sent request")
message = socket.recv()
print('waiting for respsonse')
with open('jobs.txt', 'r') as f:
    print_this = f.read()
    print_this = print_this.replace("\\n", "\n")
    print(print_this)
    f.close()

