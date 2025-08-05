from .models import Book, Category
from typing import Dict, Any
from ninja import Schema, ModelSchema
from pydantic import BaseModel
from typing import List


class CategorySchema(ModelSchema):
    class Config:
        model = Category
        model_fields = '__all__'

class BookSchema(ModelSchema):
    categories: List[CategorySchema] 
    class Config:
        model = Book
        model_fields = '__all__'


class Link(Schema):
    href: str
    method: str = 'GET'

class BookHATEOASSchema(Schema):
    id: int
    title: str
    author: str
    published_date: str
    isbn: str
    links: Dict[str, Link]

class CategoryHATEOASSchema(Schema):
    id: int
    name: str
    links: Dict[str, Link]


class LivroCompletoSchema(Schema):
    isbn: str
    titulo: str
    autor: str
    ano: int
    preco: float
    moeda: str

class PrecoLivroSchema(Schema):
    isbn: str
    preco: float
    moeda: str

class LivroDetalhadoSOAPSchema(Schema):
    isbn: str
    titulo: str
    autor: str
    ano: int
    preco: float
    moeda: str

class LivroMensagemSchema(BaseModel):
    isbn: str

class LivroProcessadoSchema(Schema):
    """Schema para livros processados pelo consumer"""
    isbn: str
    titulo: str
    autor: str
    preco: float
    moeda: str

class BookCreateSchema(Schema):
    isbn: str
    title: str
    author: str
    published_date: str
    categories: List[int] = []  # IDs das categorias

