from opcua import Server
import random
import time

server = Server() # instantiate server class
url = 'opc.tcp://127.0.0.1:51213'
server.set_endpoint(url) # specify th port the server will use to communicate data
# Add a namespace in the server. There are lready namespace in the server, each one with a specific id
name_1 = 'room 1'
namespace_1 = server.register_namespace(name_1) # create a namespace called 'room 1' and return the integer namespace id (in this case = 2)
# The server is already populated with various nodes with server information, we need the one that stores objects (T.B.N. namespaces and
# nodes are independent, e.g. we can store an object in a namespace and one of its variables in another namespace)
objects_node = server.get_objects_node() # this is the root node, to which we can add all the nodes (objects we want)
# Add temperature sensor object (node)
temperature_sensor = objects_node.add_object(f'ns={str(namespace_1)}; s="temperature_sensor"', 'temperature sensor') # in this way we create the
# object called 'temperature_sensor' in the namespace 1 (we have to specify the namspace this object belongs to and a string)
temperature = temperature_sensor.add_variable(f'ns={str(namespace_1)}; s="temperature"', 'temperature', 0) # in this way we create a variable called 'Temperature' in the object (node) 'temperature_sensor' with a default value of 0
# Add light bulb object (node)
light_bulb = objects_node.add_object(f'ns={str(namespace_1)}; s="light_bulb"', 'light bulb')
light_bulb_state = light_bulb.add_variable(f'ns={str(namespace_1)}; s="light_bulb_state"', 'light bulb state', False)
light_bulb_state.set_writable() # this variable is writable from the client side

try:
	server.start()
	print(f'Server started at {url}.', flush=True)
	while True:
		temperature_val = random.uniform(21.5, 22)
		temperature.set_value(temperature_val)
		print(f'Temperature: {round(temperature.get_value(),1)}, light bulb state: {light_bulb_state.get_value()}.', flush=True)
		time.sleep(2)
finally:
	server.stop()
	print(f'Server offline.', flush=True)