import usb
from opcua import Server, ua
import sys

class KeyboardOpcuaServer(object):

    def __init__(self, _url):
        self.url = _url

    def usb_dev_setup(self):
        self.dev = usb.core.find(idVendor=0x046d, idProduct=0xc31c)
        if self.dev is None:
            raise ValueError('device not found')
        self.dev.set_configuration()
        cfg = self.dev[0]
        intf = cfg[(0,0)]
        self.ep = intf[0]

    def opcua_server_setup(self):
        self.server = Server() # instantiate server class
        self.server.set_endpoint(self.url)
        namespace_1 = self.server.register_namespace("devices")
        objects_node = self.server.get_objects_node()
        keyboard = objects_node.add_object(f'ns={str(namespace_1)}; s="keyboard"', 'keyboard')
        self.key = keyboard.add_variable(f'ns={str(namespace_1)}; s="key"', 'key', 0)

    def run(self):
        self.usb_dev_setup()
        self.opcua_server_setup()
        try:
            self.server.start()
            print(f'Server started at {self.url}.', flush=True)
            while True:
                try:
                    raw_data = self.dev.read(self.ep.bEndpointAddress, self.ep.wMaxPacketSize, 1000)
                    data = ''.join([chr(x) for x in raw_data])
                    self.key.set_value(ua.Variant(data, ua.VariantType.String))
                    print(f'Key: {self.key.get_value()}', flush=True)
                except usb.core.USBError:
                    pass
        finally:
            self.server.stop()
            print(f'Server offline.', flush=True)

def main():
    keyboard_opcua_server = KeyboardOpcuaServer("opc.tcp://127.0.0.1:51213")
    keyboard_opcua_server.run()

if __name__ == "__main__":
    main()
