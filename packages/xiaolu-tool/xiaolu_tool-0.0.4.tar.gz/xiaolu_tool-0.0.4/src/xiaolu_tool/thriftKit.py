from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol
from thrift.transport import TTransport
from thrift.transport.TSocket import TSocket
import conf
from log import logging
from dataclasses import dataclass


class ThriftKit:
    def __init__(self, config_name, package_path, client_service):
        self.di_client = None
        self.transport = None
        assert config_name, "Config name should be a non-none value."
        assert package_path, "Package path should be a non-none value."
        assert client_service, "Target client server should be a non-none value."

        self.thrift_param = ThriftParam.of(config_name)
        self.package_path = package_path
        self.client_service = client_service

    def begin(self):
        self.transport = TSocket(self.thrift_param.host, self.thrift_param.port)

        self.transport.setTimeout(60000)
        self.transport = TTransport.TFramedTransport(self.transport)

        protocol = TBinaryProtocol(self.transport)

        ps_protocol = TMultiplexedProtocol(
            protocol,
            self.package_path,
        )
        self.di_client = self.client_service.Client(ps_protocol)
        logging.info("Start open {}".format(self.package_path))
        self.transport.open()
        return self

    def close(self):
        assert self.transport, "Please use begin() to begin this kit."
        self.transport.close()

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        self.close()


@dataclass
class ThriftParam:
    host: str
    port: int

    @classmethod
    def of(cls, t):
        param = conf.get_param('thrift.ini', t + "_" + conf.get_env())
        return cls(param['host'], param['port'])
