from django.http import JsonResponse
from django.views import View

class PrecoView(View):
    def get(self, request, isbn):
        precos = {
            "9788533302273": { "preco": 49.90, "moeda": "BRL" },
            "3817172719800": { "preco": 59.90, "moeda": "BRL" }
        }
        return JsonResponse(precos.get(isbn, {"erro": "Preço não encontrado"}))
