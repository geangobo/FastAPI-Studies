from sqlalchemy import Column, Integer, String
# Importamos 'Base' do nosso arquivo database.py
from .database import Base

class Book(Base):
    # Nome da tabela no banco de dados
    __tablename__ = "books"

    # Definição das colunas da tabela
    id = Column(Integer, primary_key=True, index=True)  # Chave primária, auto-incrementada por padrão
    title = Column(String, index=True)                  # Título do livro, indexado para buscas rápidas
    author = Column(String, index=True)                 # Autor do livro, indexado
    isbn = Column(String, unique=True, index=True, nullable=True) # ISBN, único e opcional
    published_year = Column(Integer, nullable=True)     # Ano de publicação, opcional
    genre = Column(String, nullable=True)               # Gênero do livro, opcional

    def __repr__(self):
        # Um método opcional para facilitar a visualização do objeto Book ao imprimir
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"

# Você poderia adicionar mais modelos aqui no futuro, por exemplo:
# class Author(Base):
#     __tablename__ = "authors"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     # ... e um relacionamento em Book com o autor