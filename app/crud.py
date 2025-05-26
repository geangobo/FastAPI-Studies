from sqlalchemy.orm import Session
from . import models, schemas # Importa os módulos models e schemas do mesmo diretório 'app'

# --- FUNÇÕES DE LEITURA (Read) ---

def get_book(db: Session, book_id: int):
    """
    Busca um livro específico pelo seu ID.
    """
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_isbn(db: Session, isbn: str):
    """
    Busca um livro específico pelo seu ISBN.
    """
    return db.query(models.Book).filter(models.Book.isbn == isbn).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    """
    Busca uma lista de livros com paginação (skip e limit).
    """
    return db.query(models.Book).offset(skip).limit(limit).all()

# --- FUNÇÃO DE CRIAÇÃO (Create) ---

def create_book(db: Session, book: schemas.BookCreate):
    """
    Cria um novo livro no banco de dados.
    'book' é um objeto Pydantic schemas.BookCreate.
    """
    # Converte o schema Pydantic para um modelo SQLAlchemy
    # **book.model_dump() desempacota o dicionário do schema Pydantic
    # como argumentos nomeados para o construtor de models.Book
    db_book = models.Book(**book.model_dump()) # Para Pydantic V2
    # Se estivesse usando Pydantic V1, seria: db_book = models.Book(**book.dict())

    db.add(db_book)  # Adiciona o objeto à sessão do SQLAlchemy
    db.commit()      # Salva as mudanças no banco de dados
    db.refresh(db_book) # Atualiza o objeto db_book com dados do banco (como o ID gerado)
    return db_book

# --- FUNÇÃO DE ATUALIZAÇÃO (Update) ---

def update_book(db: Session, book_id: int, book_update: schemas.BookUpdate):
    """
    Atualiza um livro existente.
    'book_update' é um objeto Pydantic schemas.BookUpdate com os campos a serem atualizados.
    """
    db_book = get_book(db, book_id=book_id)
    if db_book:
        # book_update.model_dump(exclude_unset=True) cria um dicionário
        # apenas com os campos que foram explicitamente enviados na requisição de atualização.
        update_data = book_update.model_dump(exclude_unset=True) # Pydantic V2
        # Pydantic V1 seria: update_data = book_update.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_book, key, value) # Define o atributo no objeto SQLAlchemy

        db.commit()
        db.refresh(db_book)
    return db_book

# --- FUNÇÃO DE DELEÇÃO (Delete) ---

def delete_book(db: Session, book_id: int):
    """
    Deleta um livro do banco de dados.
    """
    db_book = get_book(db, book_id=book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book # Retorna o objeto deletado (ou None se não encontrado)