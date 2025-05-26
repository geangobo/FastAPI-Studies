from pydantic import BaseModel, Field
from typing import Optional

# Schema base para o Livro: define os campos comuns.
# Usado como base para outros schemas para evitar repetição.
class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = Field(default=None, description="International Standard Book Number")
    published_year: Optional[int] = Field(default=None, ge=0, le=3000, description="Ano de publicação") # Adicionando uma validação simples de ano
    genre: Optional[str] = Field(default=None, description="Gênero do livro")

# Schema para criação de Livro: herda de BookBase.
# Usado para validar os dados recebidos no corpo de uma requisição POST.
class BookCreate(BookBase):
    # Para este caso, não há campos adicionais em relação ao BookBase
    # para a criação, mas poderia haver em cenários mais complexos.
    pass

# Schema para atualização de Livro: todos os campos são opcionais.
# Usado para validar os dados recebidos no corpo de uma requisição PUT ou PATCH.
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    published_year: Optional[int] = Field(default=None, ge=0, le=3000)
    genre: Optional[str] = None

# Schema para leitura/retorno de Livro: herda de BookBase.
# Usado para formatar os dados que são retornados nas respostas da API.
# Inclui campos que são gerados pelo banco de dados, como o 'id'.
class Book(BookBase):
    id: int # O ID é gerado pelo banco, então não está em BookCreate, mas está aqui.

    class Config:
        # Pydantic V2: 'from_attributes = True'
        # Pydantic V1: 'orm_mode = True'
        # Esta configuração permite que o Pydantic leia dados diretamente
        # de modelos ORM (como os objetos SQLAlchemy que nosso CRUD retornará).
        # Ele mapeará os atributos do objeto SQLAlchemy para os campos deste schema.
        from_attributes = True