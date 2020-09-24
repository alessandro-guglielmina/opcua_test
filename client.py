from opcua import Client

client = Client('opc.tcp://127.0.0.1:51213')
client.connect()
client.get_namespace_array()
objects_node = client.get_objects_node()
# Print children nodes
print(objects_node.get_children(), flush=True)
# Get directly a specific node
temperature = client.get_node('ns=2;s="temperature"')
# get a node value (if it's a variable)
temperature.get_value()

                                         
light_bulb_state=client.get_node('ns=2;s="light_bulb_state"')
# If the variable is writable, its value can be set from the client side
light_bulb_state.set_value(True)

# Close client session (the servere remains connected)
client.close_session()