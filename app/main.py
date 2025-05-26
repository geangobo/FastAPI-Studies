from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List # Para listas nos tipos de resposta

# Importações relativas dos nossos módulos
from . import crud, models, schemas
from .database import SessionLocal, engine, create_db_and_tables

# --- Criação das Tabelas do Banco de Dados ---
# Isso garantirá que todas as tabelas definidas em models.py
# sejam criadas no banco de dados na primeira vez que a aplicação rodar.
# Em um ambiente de produção, você provavelmente usaria Alembic para migrações.
create_db_and_tables()
# Alternativamente, usando o evento de startup do FastAPI:
# app = FastAPI()
# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# --- Instância da Aplicação FastAPI ---
app = FastAPI(
    title="API de Gerenciamento de Livros",
    description="Uma API para adicionar, visualizar, atualizar e deletar livros.",
    version="0.1.0"
)

# --- Dependência para Sessão do Banco de Dados ---
def get_db():
    """
    Função de dependência que cria e gerencia uma sessão de banco de dados por requisição.
    Garante que a sessão seja fechada após a requisição, mesmo se ocorrerem erros.
    """
    db = SessionLocal()
    try:
        yield db  # Fornece a sessão para a função da rota
    finally:
        db.close() # Fecha a sessão após o uso

# --- Endpoints da API ---

@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_new_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Cria um novo livro.
    - **title**: Título do livro (obrigatório)
    - **author**: Autor do livro (obrigatório)
    - **isbn**: ISBN (opcional)
    - **published_year**: Ano de publicação (opcional)
    - **genre**: Gênero (opcional)
    """
    # Verifica se já existe um livro com o mesmo ISBN, se um ISBN for fornecido
    if book.isbn:
        db_book_by_isbn = crud.get_book_by_isbn(db, isbn=book.isbn)
        if db_book_by_isbn:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Livro com ISBN {book.isbn} já existe.")
    return crud.create_book(db=db, book=book)

@app.post("/books/bulk/", response_model=List[schemas.Book], status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_multiple_books(books_to_create: List[schemas.BookCreate], db: Session = Depends(get_db)):
    """
    Cria múltiplos livros de uma vez.
    Envie uma lista de objetos de livros (schemas.BookCreate) no corpo da requisição.
    """
    created_books_list = []
    errors_details = [] # Para coletar informações sobre erros, se houver

    for book_data in books_to_create:
        # Validação de ISBN duplicado (opcional, mas recomendado para consistência)
        # Esta é uma verificação antes de tentar inserir no banco.
        # A função crud.create_book também pode ter sua própria lógica de erro ou o banco pode rejeitar.
        if book_data.isbn:
            existing_book_by_isbn = crud.get_book_by_isbn(db, isbn=book_data.isbn)
            if existing_book_by_isbn:
                # Decide como lidar:
                # 1. Levantar uma exceção e parar todo o lote (mais simples de implementar inicialmente)
                # 2. Adicionar a um log de erros e continuar com os próximos (mais complexo)
                # 3. Retornar uma resposta mista (alguns criados, alguns com erro)
                # Para este exemplo, vamos ser rigorosos como no endpoint de criação única:
                errors_details.append({"isbn": book_data.isbn, "error": "ISBN já existe"})
                # Se quiser parar no primeiro erro de ISBN duplicado no lote:
                # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Livro com ISBN {book_data.isbn} já existe no banco ou no lote.")
                continue # Pula para o próximo livro do lote se um ISBN já existe

        # Se chegou aqui, o ISBN (se fornecido) não foi encontrado previamente OU não foi fornecido
        try:
            created_book = crud.create_book(db=db, book=book_data) # crud.create_book faz o commit
            created_books_list.append(created_book)
        except Exception as e: # Captura uma exceção mais genérica do crud.create_book
                               # Por exemplo, IntegrityError do banco se o ISBN for único e já existir
                               # e não foi pego pela verificação anterior (condição de corrida ou ISBN nulo antes e agora preenchido).
            db.rollback() # Importante reverter se o crud.create_book falhou após um add mas antes do commit, ou se o commit falhou.
                          # A sua função crud.create_book atual já faz o commit. Se ela falhar, o estado da sessão é importante.
            errors_details.append({"title": book_data.title, "error": str(e)})
            # Se a sua função crud.create_book não fizer commit e você fizer commit aqui no final,
            # um único rollback aqui seria mais apropriado para a transação inteira.

    # Se você quiser retornar um erro geral caso algum livro tenha falhado:
    if errors_details and not created_books_list: # Nenhum livro foi criado, só erros
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Nenhum livro pôde ser criado devido a erros.", "errors": errors_details})
    
    # Se alguns foram criados e outros não, você pode querer uma resposta mais complexa
    # ou simplesmente retornar os que foram criados com sucesso.
    # Por simplicidade, se houver erros mas alguns livros foram criados, retornamos os criados.
    # Uma resposta mais completa poderia incluir os detalhes dos erros.

    if not created_books_list and not errors_details:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum dado de livro fornecido ou todos os dados eram inválidos antes da tentativa de criação.")

    return created_books_list

@app.get("/books/", response_model=List[schemas.Book], tags=["Books"])
def read_all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista de livros, com opção de paginação.
    - **skip**: Número de registros a pular.
    - **limit**: Número máximo de registros a retornar.
    """
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def read_single_book(book_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um livro específico pelo seu ID.
    - **book_id**: ID do livro a ser buscado.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def update_existing_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    """
    Atualiza um livro existente.
    Você pode enviar apenas os campos que deseja atualizar.
    - **book_id**: ID do livro a ser atualizado.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado para atualização")

    # Verifica se o ISBN está sendo atualizado para um valor que já existe em outro livro
    if book_update.isbn and book_update.isbn != db_book.isbn:
        existing_book_with_isbn = crud.get_book_by_isbn(db, isbn=book_update.isbn)
        if existing_book_with_isbn and existing_book_with_isbn.id != book_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Outro livro já existe com o ISBN {book_update.isbn}")

    return crud.update_book(db=db, book_id=book_id, book_update=book_update)

@app.delete("/books/{book_id}", response_model=schemas.Book, tags=["Books"]) # Ou poderia retornar um status_code=204 e sem response_model
def delete_existing_book(book_id: int, db: Session = Depends(get_db)):
    """
    Deleta um livro existente.
    - **book_id**: ID do livro a ser deletado.
    """
    db_book = crud.get_book(db, book_id=book_id) # Primeiro, verifique se o livro existe
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado para deletar")
    crud.delete_book(db=db, book_id=book_id)
    return db_book # Retorna o livro deletado como confirmação
    # Alternativamente, para um DELETE que não retorna conteúdo:
    # if crud.delete_book(db=db, book_id=book_id):
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")

