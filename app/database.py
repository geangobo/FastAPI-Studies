from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão para o SQLite.
# O arquivo do banco de dados ('sql_app.db') será criado na raiz do projeto
# (onde você executa o comando uvicorn).
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Cria a engine do SQLAlchemy.
# A engine é o ponto de partida para qualquer aplicação SQLAlchemy.
# Ela gerencia as conexões com o banco de dados.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # O argumento connect_args={"check_same_thread": False} é necessário apenas para SQLite.
    # Ele permite que mais de uma thread interaja com o banco de dados, o que é
    # importante para aplicações web como FastAPI.
    connect_args={"check_same_thread": False}
)

# Cria uma classe SessionLocal.
# Cada instância de SessionLocal será uma sessão de banco de dados.
# A sessão é o principal meio de interagir com o banco de dados (fazer queries, commits, etc.).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base.
# Seus modelos de dados (tabelas do banco) herdarão desta classe.
Base = declarative_base()

# Função auxiliar para criar todas as tabelas no banco de dados
# que são definidas pelos modelos que herdam de Base.
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)