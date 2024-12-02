# 🧁 CakeCup - Sistema de Pedidos de Cupcakes

Sistema de e-commerce especializado em cupcakes, desenvolvido com PyNest Framework.

## 🚀 Tecnologias

- Python 3.10+
- PyNest Framework
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Pydantic
- Uvicorn
- JWT para autenticação

## 🏗️ Arquitetura

O projeto segue uma arquitetura modular baseada em DDD (Domain-Driven Design):
```bash
cakecup_back_app/
├── src/
│ ├── core/
│ │ ├── decorators/ # Decorators para validação, auth, etc
│ │ ├── entity/ # Entidades base
│ │ ├── middleware/ # Middlewares (CORS, Response)
│ │ ├── models/ # Modelos compartilhados
│ │ └── providers/ # Providers (Database, etc)
│ ├── modules/
│ │ ├── auth/ # Módulo de autenticação
│ │ ├── cart/ # Módulo de carrinho
│ │ ├── order/ # Módulo de pedidos
│ │ ├── product/ # Módulo de produtos
│ │ └── user/ # Módulo de usuários
│ └── app_module.py # Módulo principal
└── main.py # Ponto de entrada da aplicação
```

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/tiagogois/cakecup_back_app.git
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
.\venv\Scripts\activate # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

5. Excute os sqls para criar as tabelas no banco de dados:
```bash
python loc
```

6. Inicie o servidor:
```bash
python main.py
```

# 📚 Documentação da API

A documentação da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔑 Autenticação

O sistema usa JWT (JSON Web Tokens) para autenticação. Para acessar endpoints protegidos:

1. Faça login em `/auth/login`
2. Use o token retornado no header `Authorization: Bearer {token}`

## 🛒 Funcionalidades Principais

- **Autenticação e Autorização**
  - Login/Registro de usuários
  - Gerenciamento de permissões

- **Produtos**
  - Catálogo de cupcakes
  - Gerenciamento de produtos
  - Categorização

- **Carrinho de Compras**
  - Adicionar/remover itens
  - Atualizar quantidades
  - Calcular totais

- **Pedidos**
  - Criar pedidos
  - Acompanhar status
  - Histórico de pedidos

- **Avaliações**
  - Avaliar produtos
  - Comentários

## 🧪 Testes

Execute os testes com:
```bash
pytest
```

Para testes com cobertura:
```bash
pytest --cov=src
```

## 🔄 Middlewares

- **CorsMiddleware**: Configuração de CORS
- **ResponseMiddleware**: Padronização de respostas
- **AuthenticationMiddleware**: Validação de tokens

## 📝 Modelos de Dados

### User
- id: UUID
- name: str
- email: str
- password: str
- role: UserRole

### Product
- id: UUID
- name: str
- description: str
- price: Decimal
- category: str

### Cart
- id: UUID
- user_id: UUID
- items: List[CartItem]
- total: Decimal

### Order
- id: UUID
- user_id: UUID
- items: List[OrderItem]
- total: Decimal
- status: OrderStatus

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- Tiago Gois - [GitHub](https://github.com/goistsg)

## 🙏 Agradecimentos

- PyNest Framework
- FastAPI
- Toda a comunidade Python

---

⌨️ com ❤️ por [Tiago Gois](https://github.com/goistsg)
