from django.http import JsonResponse
from django.views import View

class LivroView(View):
    def get(self, request, isbn):
        livros = {
            "9788533302273": {
                "titulo": "As Cronicas de Narnia",
                "autor": "C. S. Lewis",
                "ano": 1950
            },
            "3817172719800": {
                "titulo": "O Labirinto do Fauno",
                "autor": "Guillermo Del Toro",
                "ano": 2006
            }
        }
        return JsonResponse(livros.get(isbn, {"erro": "Livro não encontrado"}))
