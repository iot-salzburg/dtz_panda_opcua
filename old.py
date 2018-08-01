from opcua import Server
from random import randint
import datetime
import time

server = Server()

url = "opc.tcp://192.168.48.44:4840"
server.set_endpoint(url)

# Add name to the address space     # setup our own namespace, not really necessary but should as spec
name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

# get Objects node, this is where we should put our nodes
node = server.get_objects_node()

# Add a parameter object to the address space
Param = node.add_object(addspace, "Parameters")

# Parameters - Addresspsace, Name, Initial Value
Temp = Param.add_variable(addspace, "Temperature", 0)
Press = Param.add_variable(addspace, "Pressure", 0)
ConBeltState = Param.add_variable(addspace, "Conveyor Belt - State", "init")
ConBeltDistance = Param.add_variable(addspace, "Conveyor Belt - Distance", 0.0)
Time = Param.add_variable(addspace, "Time", 0)

# Set parameters writable by clients
Temp.set_writable()
Press.set_writable()
Time.set_writable()
ConBeltState.set_writable()

# Start the server
server.start()
print("Server started ad {}".format(url))

try:
    # Assign random values to the parameters
    while True:
        # calculate random values
        Temperature = randint(10,50)  # Assign random value from 10 to 50
        Pressure = randint(200, 999)
        TIME = datetime.datetime.now()  # current time
        with open("state.log") as f:
            state = f.read()
        with open("distance.log") as f:
            distance = f.read()

        # set the random values inside the node
        print(Temperature, Pressure, TIME, state)
        Temp.set_value(Temperature)
        Press.set_value(Pressure)
        Time.set_value(TIME)
        ConBeltState.set_value(state)
        ConBeltDistance.set_value(distance)
        # sleep 2 seconds
        time.sleep(2)


finally:
    #close connection, remove subcsriptions, etc
    server.stop()