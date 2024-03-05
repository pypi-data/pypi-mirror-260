#!/usr/bin/env python3
import grpc

from openobd_protocol import RemoteDiagnosticServices_pb2_grpc as grpc_service
from openobd_protocol import ModuleConfiguration_pb2 as grpc_module_configuration
from openobd_protocol.CAN import CanServices_pb2_grpc as can_service


class OpenOBDClient(object):

    rest_api = None
    token = None

    """
    Client for gRPC functionality
    """
    def __init__(self, rest_api=None):
        rest_api = rest_api

    def connected(self):
        """Reports back if OpenOBD client is connected

        TODO: Write function
        """
        return True

    def __create_socket__(self):
        '''REST API calls to create a socket and retrieve GRPC host and token'''

        #self.__connect_through_grpc__()

    def __connect_through_grpc__(self, grpc_host, grpc_port=443, token=token):
        self.token = token

        ''' Check if local grpc-proxy is running '''
        if grpc_port == 443:
            self.channel = grpc.secure_channel(grpc_host, grpc.ssl_channel_credentials())
        else:
            self.channel = grpc.insecure_channel('{}:{}'.format(grpc_host, grpc_port))

        '''
        Bind the openobd and the server
        '''
        self.rds = grpc_service.RemoteDiagnosticServicesStub(self.channel)
        self.can = can_service.CanServicesStub(self.channel)

    def __metadata__(self):
        metadata = (("authorization", "Bearer {}".format(self.token)),)
        return metadata

    def requestModuleConfiguration(self, module_configuration : grpc_module_configuration.ModuleConfiguration):
        """
        Client function to call the rpc for GetServerResponse
        """
        return self.rds.requestModuleConfiguration(request=module_configuration, metadata=self.__metadata__())

