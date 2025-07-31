from xmlrpc.client import Fault
from ninja import NinjaAPI, Router
from django.shortcuts import get_object_or_404
from typing import List
from .schemas import *
from ninja.errors import HttpError
from django.urls import reverse
import httpx
from zeep import Client
from .schemas import PrecoLivroSchema

api = NinjaAPI(title="Library Gateway API", description="API Gateway com REST, SOAP, HATEOAS")


@api.get("/books", response=List[BookSchema], tags=['Livro'])
def list_books(request):
    try:
        livros = Book.objects.all().prefetch_related('categories')
        if not livros:
            raise HttpError(404, "Sem livros cadastrados")
        return livros
    except Exception as e:
        raise HttpError(500, f"Erro ao listar livros: {str(e)}")
        

@api.get("/books/{id}", response=BookSchema, tags=['Livro'])
def get_book(request, id: int):
    book = get_object_or_404(Book, id=id)
    return book

@api.get("/books-hateoas", response=List[BookHATEOASSchema], tags=['Livro'])
def list_books_hateoas(request):
    livros = Book.objects.all()
    results = []

    for livro in livros:
        links = {
            "self": Link(href=f"/api/books/{livro.id}"),
            "edit": Link(href=f"/api/books/{livro.id}", method="PUT"),
            "delete": Link(href=f"/api/books/{livro.id}", method="DELETE"),
            "categories": Link(href=f"/api/books/{livro.id}/categories")
        }

        results.append({
            "id": livro.id,
            "title": livro.title,
            "author": livro.author,
            "published_date": livro.published_date.isoformat(),
            "isbn": livro.isbn,
            "links": links
        })

    return results

@api.put("/books", response=BookSchema, tags=['Livro'])
def update_book(request, book: BookSchema):
    try:
        livro = get_object_or_404(Book, id=book.id)
        book_data = book.dict()
        categories = book_data.pop('categories', None)
        for attr, value in book_data.items():
            setattr(livro, attr, value)
        livro.save()
        if categories is not None:
            livro.categories.set(categories)
        return livro
    except Exception as e:
        raise HttpError(500, f"Erro ao atualizar livro: {str(e)}")
    
@api.delete("/books/{id}", tags=['Livro'])
def delete_book(request, id: int):
    try:
        livro = get_object_or_404(Book, id=id)
        livro.delete()
        return {"success": True, "message": "Livro deletado com sucesso"}
    except Exception as e:
        raise HttpError(500, f"Erro ao deletar livro: {str(e)}")
    
@api.post("/books", response=BookSchema, tags=['Livro'])
def create_book(request, book: BookSchema):
    try:
        book_data = book.dict()
        categories = book_data.pop('categories', None)
        livro = Book.objects.create(**book_data)
        if categories is not None:
            livro.categories.set(categories)
        return livro
    except Exception as e:
        raise HttpError(500, f"Erro ao criar livro: {str(e)}")
    

@api.get("/livro-detalhado/{isbn}", response=LivroCompletoSchema)
async def get_livro_completo(request, isbn: str):
    try:
        async with httpx.AsyncClient() as client:
            res_livro = await client.get(f"http://localhost:8001/api/livros/{isbn}")
            res_preco = await client.get(f"http://localhost:8002/api/precos/{isbn}")
        
        if res_livro.status_code != 200 or res_preco.status_code != 200:
            raise HttpError(404, "Livro ou preço não encontrado")
        
        livro = res_livro.json()
        preco = res_preco.json()

        return {
            "isbn": isbn,
            "titulo": livro["titulo"],
            "autor": livro["autor"],
            "ano": livro["ano"],
            "preco": preco["preco"],
            "moeda": preco["moeda"]
        }

    except Exception as e:
        raise HttpError(500, f"Erro: {str(e)}")
    

@api.get("/categories", response=List[CategorySchema], tags=['Categoria'])
def list_categories(request):
    try:
        categories = Category.objects.all()
        if not categories:
            raise HttpError(404, "Sem categorias cadastradas")
        return categories
    except Exception as e:
        raise HttpError(500, f"Erro ao listar categorias: {str(e)}")
    
@api.get("/categories/{id}", response=CategorySchema, tags=['Categoria'])
def get_category(request, id: int):
    try:
        category = get_object_or_404(Category, id=id)
        return category
    except Exception as e:
            raise HttpError(500, f"Erro ao obter categoria: {str(e)}")
    
@api.post("/categories", response=CategorySchema, tags=['Categoria'])
def create_category(request, category: CategorySchema):
    try:
        category_data = category.dict()
        new_category = Category.objects.create(**category_data)
        return new_category
    except Exception as e:
        raise HttpError(500, f"Erro ao criar categoria: {str(e)}")
    
@api.put("/categories/{id}", response=CategorySchema, tags=['Categoria'])
def update_category(request, id: int, category: CategorySchema):
    try:
        existing_category = get_object_or_404(Category, id=id)
        category_data = category.dict()
        for attr, value in category_data.items():
            setattr(existing_category, attr, value)
        existing_category.save()
        return existing_category
    except Exception as e:
        raise HttpError(500, f"Erro ao atualizar categoria: {str(e)}")
    
@api.delete("/categories/{id}", tags=['Categoria'])
def delete_category(request, id: int):
    try:
        category = get_object_or_404(Category, id=id)
        category.delete()
        return {"success": True, "message": "Categoria deletada com sucesso"}
    except Exception as e:
        raise HttpError(500, f"Erro ao deletar categoria: {str(e)}")
    
@api.get("categories-hateoas", response=List[CategoryHATEOASSchema], tags=['Categoria'])
def list_categories_hateoas(request):
    categories = Category.objects.all()
    results = []

    for category in categories:
        links = {
            "self": Link(href=f"/api/categories/{category.id}"),
            "edit": Link(href=f"/api/categories/{category.id}", method="PUT"),
            "delete": Link(href=f"/api/categories/{category.id}", method="DELETE")
        }

        results.append({
            "id": category.id,
            "name": category.name,
            "links": links
        })

    return results


soap_client = Client("http://localhost:8003/?wsdl")


@api.get("/preco-soap/{isbn}", response=PrecoLivroSchema, tags=['Preço (SOAP)'])
def preco_livro_soap(request, isbn: str):
    try:
        result = soap_client.service.get_book_price(isbn)

        if not result:
            raise HttpError(404, "Preço não encontrado")

        return {
            "isbn": isbn,
            "preco": result.preco,
            "moeda": result.moeda
        }

    except Fault as fault:
        raise HttpError(500, f"Erro SOAP: {fault.message}")
    except Exception as e:
        raise HttpError(500, f"Erro interno ao consultar preço: {str(e)}")
    

@api.get("/livro-detalhado-soap/{isbn}", response=LivroDetalhadoSOAPSchema, tags=['Livro + Preço (REST + SOAP)'])
async def livro_detalhado_soap(request, isbn: str):
    try:
        # Consulta detalhes do livro via REST interno
        async with httpx.AsyncClient() as client:
            res_livro = await client.get(f"http://localhost:8001/api/livros/{isbn}")
        
        if res_livro.status_code != 200:
            raise HttpError(404, "Livro não encontrado")

        livro = res_livro.json()

        # Consulta preço via serviço SOAP
        preco = soap_client.service.get_book_price(isbn)
        if not preco:
            raise HttpError(404, "Preço não encontrado")

        return {
            "isbn": isbn,
            "titulo": livro["titulo"],
            "autor": livro["autor"],
            "ano": livro["ano"],
            "preco": preco.preco,
            "moeda": preco.moeda
        }

    except Exception as e:
        raise HttpError(500, f"Erro ao consultar dados combinados: {str(e)}")
