# Projeto Livraria API: Aprendendo FastAPI e SQLAlchemy

Este projeto é uma API simples para gerenciamento de livros, desenvolvida como um exercício prático para aprender e demonstrar o uso de FastAPI, Pydantic e SQLAlchemy em conjunto.

## Propósito ✏️

O objetivo principal é entender como essas três tecnologias se integram para construir APIs web modernas, eficientes e robustas em Python, cobrindo:

* **FastAPI:** Para a criação rápida de endpoints da API, roteamento, injeção de dependências e documentação automática.
* **Pydantic:** Para validação de dados de entrada e saída (serialização/desserialização) e configurações.
* **SQLAlchemy:** Para a interação com o banco de dados (ORM), definição de modelos e execução de queries.

## Tecnologias Utilizadas 💡

### 1. FastAPI
* **Descrição:** Um framework web moderno e de alta performance para construir APIs com Python 3.7+ baseado em type hints padrão do Python. É conhecido por sua velocidade (comparável a Node.js e Go), facilidade de uso e documentação automática interativa (Swagger UI e ReDoc).
* **Site:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

### 2. Pydantic
* **Descrição:** Uma biblioteca de validação de dados e gerenciamento de configurações usando type hints do Python. FastAPI usa Pydantic extensivamente para definir, validar e documentar os corpos das requisições e respostas da API de forma clara e concisa.
* **Site:** [https://pydantic-docs.helpmanual.io/](https://pydantic-docs.helpmanual.io/)

### 3. SQLAlchemy
* **Descrição:** Um toolkit SQL e Object-Relational Mapper (ORM) para Python. Ele fornece uma maneira flexível e poderosa de interagir com bancos de dados relacionais, permitindo que você defina modelos de dados como classes Python e execute queries de forma programática.
* **Site:** [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)

### 4. Uvicorn
* **Descrição:** Um servidor ASGI (Asynchronous Server Gateway Interface) leve e rápido, usado para executar aplicações FastAPI.
* **Site:** [https://www.uvicorn.org/](https://www.uvicorn.org/)

## Configuração e Instalação 📥

### Pré-requisitos
* Python 3.7 ou superior.

### Passos

1.  **Clone o repositório (se aplicável) ou crie a estrutura de arquivos conforme desenvolvido.**

2.  **Crie e ative um ambiente virtual:**
    É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

    ```bash
    # No Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # No Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    Com o ambiente virtual ativado, instale os pacotes necessários usando `pip`:

    ```bash
    pip install fastapi uvicorn[standard] sqlalchemy pydantic
    ```
    * `fastapi`: O framework principal.
    * `uvicorn[standard]`: O servidor ASGI para rodar a aplicação. A opção `[standard]` inclui algumas dependências úteis como `python-multipart` para formulários e `websockets`.
    * `sqlalchemy`: O ORM para interagir com o banco de dados (neste projeto, usamos SQLite, que é suportado nativamente pelo Python, não exigindo um driver de banco de dados separado para instalação via pip).
    * `pydantic`: Embora seja uma dependência do FastAPI e instalado automaticamente com ele, é bom estar ciente de sua importância.

4.  **Gere o arquivo `requirements.txt`:**
    Após instalar as dependências e confirmar que sua aplicação está funcionando, é uma boa prática gerar um arquivo `requirements.txt`. Este arquivo lista todos os pacotes no seu ambiente virtual com suas versões exatas, garantindo que outros possam recriar o ambiente de forma idêntica.

    Dentro do seu ambiente virtual ativado, na pasta raiz do projeto, execute:
    ```bash
    pip freeze > requirements.txt
    ```
    Este comando criará o arquivo `requirements.txt`. Adicione este arquivo ao seu sistema de controle de versão (ex: Git). Posteriormente, para instalar as dependências a partir deste arquivo em um novo ambiente, use: `pip install -r requirements.txt`.

## Estrutura do Projeto (Simplificada) 📜
FastAPI_Studies/
├── venv/                     # Ambiente virtual
├── app/
│   ├── init.py           # Inicializador do pacote 'app'
│   ├── main.py               # Ponto de entrada da API FastAPI, define os endpoints
│   ├── models.py             # Modelos de dados SQLAlchemy (estrutura das tabelas)
│   ├── schemas.py            # Schemas Pydantic (validação e serialização de dados)
│   ├── crud.py               # Funções CRUD (operações de banco de dados)
│   └── database.py           # Configuração do banco de dados SQLAlchemy (engine, session)
└── requirements.txt          # Arquivo com as dependências do projeto


## Executando a Aplicação 🌐

1.  Navegue até o diretório raiz do projeto (onde a pasta `app` está localizada).
2.  Certifique-se de que seu ambiente virtual está ativado.
3.  Execute o servidor Uvicorn:

    ```bash
    uvicorn app.main:app --reload
    ```
    * `app.main`: Refere-se ao arquivo `main.py` dentro da pasta `app`.
    * `:app`: Refere-se à instância `app = FastAPI()` dentro do `main.py`.
    * `--reload`: Faz o servidor reiniciar automaticamente após alterações no código (ótimo para desenvolvimento).

## Acessando a API e a Documentação ⚙️

Após iniciar o servidor, você pode acessar:

* **API (Swagger UI):** `http://127.0.0.1:8000/docs`
    * Interface interativa para visualizar e testar todos os endpoints da API.
* **API (ReDoc):** `http://127.0.0.1:8000/redoc`
    * Documentação alternativa e mais formal da API.

## Endpoints Principais 🔗

* `POST /books/`: Cria um novo livro.
* `GET /books/`: Lista todos os livros (com paginação).
* `GET /books/{book_id}`: Obtém detalhes de um livro específico.
* `PUT /books/{book_id}`: Atualiza um livro existente.
* `DELETE /books/{book_id}`: Remove um livro.
