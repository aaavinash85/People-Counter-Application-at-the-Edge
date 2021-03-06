import os
import sys
import logging as log
from openvino.inference_engine import IENetwork, IECore

class Network:
    def __init__(self):
        ### TODO: Initialize any class variables desired ###
        self.plugin = None
        self.network = None
        self.input_blob = None
        self.output_blob = None
        self.exec_network = None
        self.infer_request = None

    def load_model(self, model, CPU_EXTENSION, DEVICE, console_output= False):
        ### TODO: Load the model ###
        model_xml = model
        model_bin = os.path.splitext(model_xml)[0] + ".bin"
        
        self.plugin = IECore()
        self.network = IENetwork(model=model_xml, weights=model_bin)
        ### TODO: Check for supported layers ###
        if not all_layers_supported(self.plugin, self.network, console_output=console_output):
            self.plugin.add_extension(CPU_EXTENSION, DEVICE)
            
        self.exec_network = self.plugin.load_network(self.network, DEVICE)
        # Get the input layer
        self.input_blob = next(iter(self.network.inputs))
        self.output_blob = next(iter(self.network.outputs))
       
        ### TODO: Return the loaded inference plugin ###
        ### Note: You may need to update the function parameters. ###
        return

    def get_input_shape(self):
        ### TODO: Return the shape of the input layer ###
        input_shapes = {}
        for inp in self.network.inputs:
            input_shapes[inp] = (self.network.inputs[inp].shape)
        return input_shapes
    

    def exec_net(self, net_input, request_id):
        ### TODO: Start an asynchronous request ###
        ### TODO: Return any necessary information ###
        self.infer_request_handle = self.exec_network.start_async(
                request_id, 
                inputs=net_input)

        return 

    def wait(self):
        status = self.infer_request_handle.wait()
        return status
    def get_output(self):
        ### TODO: Extract and return the output results
        ### Note: You may need to update the function parameters. ###
        out = self.infer_request_handle.outputs[self.output_blob]
        return out

def all_layers_supported(engine, network, console_output=False):
    layers_supported = engine.query_network(network, device_name='CPU')
    layers = network.layers.keys()

    all_supported = True
    for l in layers:
        if l not in layers_supported:
            all_supported = False

    return all_supported
