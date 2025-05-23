from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

# Motor que vai se conectar com o banco de dados: 
engine = create_engine(
    'sqlite:///dados.db'
)
# Aqui contém todas informações para uma classe ser detectada como uma tabela de um db
Base = declarative_base() # Toda entidade nova é herdada dessa classe aqui
_Sessao = sessionmaker(engine)

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True) # Estou setando uma chave primária (id)
    nome = Column(String(40), unique=True)

Base.metadata.create_all(engine)

# Conexão temporária com o banco de dados (Sessao)
'''
with _Sessao() as sessao: 
    usuario = Usuario(nome='Marcos') # Crio apenas uma instância da classe
    sessao.add(usuario)
    sessao.commit()
'''





