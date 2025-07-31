from wsgiref.simple_server import make_server
from server import application

if __name__ == '__main__':
    print("Servidor SOAP rodando em http://localhost:8003")
    make_server('0.0.0.0', 8003, application).serve_forever()
