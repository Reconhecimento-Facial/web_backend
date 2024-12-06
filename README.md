# Reconhecimento Facial - Backend

Este repositório contém o backend da aplicação de reconhecimento facial, desenvolvido utilizando Docker para facilitar a configuração e execução do ambiente.

## Pré-requisitos

Antes de começar, você precisará ter as seguintes ferramentas instaladas em sua máquina:

- [Git](https://git-scm.com)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Como rodar a aplicação

Siga os passos abaixo para clonar o repositório e executar a aplicação:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Reconhecimento-Facial/web_backend.git

2. **Navegue até o diretório do projeto:**

    ```bash
    cd web_backend

3. **Crie um arquivo .env na raíz do projeto**

    ```
    DATABASE_URL="postgresql+psycopg://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>"
    SECRET_KEY="<YOUR_SECRET_KEY>"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=<INT>
    POSTGRES_DB=<DB_NAME>
    POSTGRES_USER=<DB_USER>
    POSTGRES_PASSWORD=<DB_PASSWORD>

4. **Execute o Docker Compose:**
    ```
    docker compose up --build