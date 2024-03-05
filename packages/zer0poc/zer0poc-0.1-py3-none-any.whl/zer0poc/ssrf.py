from flask import Flask, request
from .utils import random_string
from .logging import Logger

class SSRFServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.service_name = random_string()

        self.log = Logger()

    def start(self):

        app = Flask(__name__)

        @app.route('/')
        def index():
            return 'This is a SSRF Testing Server to test SSRF in applications.'

        @app.route(f'/{self.service_name}')
        def ssrf_route():

            self.log.info(f'SSRF Request from {request.remote_addr}',indent=2)

            return f'This endpoint can be a vulnerable service\nflag={random_string(32)}'
        
        try:
            self.log.info(f'Starting SSRF Server on {self.host}:{self.port}')
            self.server = app.run(self.host, self.port, use_reloader=False)

        except Exception as e:
            self.log.error(f'Error starting SSRF Server: {e}',indent=2)
        
        self.log.success(f'SSRF Server started on {self.host}:{self.port}',indent=2)
        self.log.info(f'Service Endpoint: {self.host}:{self.port}/{self.service_name}',indent=2)

    def stop(self):
        self.log.info('Shutting down SSRF Server',indent=2)
        try:
            self.server.shutdown()
            self.server.server_close()
        except Exception as e:
            self.log.error(f'Error shutting down SSRF Server: {e}',indent=2)