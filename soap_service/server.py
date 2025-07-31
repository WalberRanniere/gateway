from spyne import Application, rpc, ServiceBase, Unicode, Float, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class BookPrice(ComplexModel):
    preco = Float
    moeda = Unicode

class BookService(ServiceBase):

    @rpc(Unicode, _returns=BookPrice)
    def get_book_price(ctx, isbn):
        precos = {
            "9788533302273": {"preco": 49.90, "moeda": "BRL"},
            "3817172719800": {"preco": 59.90, "moeda": "BRL"},
        }

        data = precos.get(isbn, {"preco": 0.0, "moeda": "DESCONHECIDA"})
        return BookPrice(preco=data["preco"], moeda=data["moeda"])

# Configuração do app SOAP
app = Application(
    [BookService],
    tns='soap.book',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

application = WsgiApplication(app)
