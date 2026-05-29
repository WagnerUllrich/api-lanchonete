# Raízes do Nordeste — API Back-end

API REST desenvolvida para o Projeto Multidisciplinar – Trilha Back-End da UNINTER.

O sistema simula o back-end de uma rede de lanchonetes com múltiplas unidades e múltiplos canais de atendimento, contemplando autenticação, controle de estoque, pedidos, pagamentos simulados, fidelidade, auditoria e multicanalidade.

---

## Tecnologias Utilizadas

* Python 3.10+
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT (JSON Web Token)
* Swagger / OpenAPI
* Uvicorn

---

## Requisitos

Para executar o projeto é necessário possuir:

* Python 3.10 ou superior
* SQLite
* Git
* Pip

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/WagnerUllrich/api-lanchonete.git
cd api-lanchonete
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar ambiente virtual

Windows:

```bash
.venv\Scripts\activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Variáveis de Ambiente

Crie um arquivo `.env` utilizando o `.env.example` como base.

Exemplo:

```env
DATABASE_URL=sqlite:///./lanchonete.db
JWT_SECRET_KEY=sua_chave_secreta_super_segura
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

---

## Banco de Dados

O sistema utiliza SQLite.

O banco de dados é criado automaticamente na primeira execução da aplicação através do SQLAlchemy.

Arquivo gerado:

```txt
lanchonete.db
```

---

## Executando a Aplicação

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

```txt
http://127.0.0.1:8000
```

---

## Documentação Swagger

Swagger UI:

```txt
http://127.0.0.1:8000/docs
```

OpenAPI JSON:

```txt
http://127.0.0.1:8000/openapi.json
```

---

## Arquitetura

A aplicação segue uma arquitetura em camadas, separando responsabilidades entre:

* API (endpoints REST)
* Models (entidades do domínio)
* Schemas (contratos e validações)
* Core (segurança e autenticação)
* Database (persistência)
* Utils (auditoria e funções auxiliares)

Essa organização facilita manutenção, evolução e reutilização do código.

---

## Estrutura do Projeto

```txt
app/
├── api/       # Endpoints REST
├── core/      # Segurança, JWT e controle de acesso
├── db/        # Configuração do banco de dados
├── models/    # Entidades do domínio
├── schemas/   # Validação e contratos da API
├── utils/     # Auditoria e funções auxiliares
└── main.py    # Inicialização da aplicação
```

---

## Funcionalidades Implementadas

### Usuários

* Criar usuário
* Consultar usuário autenticado (`/usuarios/me`)
* Controle de acesso por perfil

Perfis disponíveis:

* ADMIN
* FUNCIONARIO
* CLIENTE

### Autenticação

* Login com JWT
* Geração de token de acesso
* Proteção de rotas autenticadas

### Unidades

* Criar unidade
* Listar unidades
* Buscar unidade por ID
* Atualizar unidade
* Obter cardápio por unidade

### Produtos

* Criar produto
* Listar produtos
* Buscar produto por ID
* Atualizar produto

### Estoques

* Criar estoque
* Listar estoques
* Listar estoque por unidade
* Registrar entrada de estoque
* Registro automático de saídas
* Registro automático de devoluções
* Controle de movimentações de estoque
* Controle de disponibilidade para venda

### Pedidos

* Criar pedido
* Listar pedidos
* Buscar pedido por ID
* Atualizar status do pedido
* Cancelamento de pedidos através da atualização de status
* Controle automático de saída de estoque
* Devolução automática de estoque em cancelamentos
* Registro do canal de origem do pedido
* Validação de estoque antes da criação

### Pagamentos

* Criar pagamento
* Simulação de aprovação
* Simulação de recusa
* Simulação de erro de integração
* Atualização automática do status do pedido

### Fidelidade

* Consultar saldo de pontos
* Resgatar pontos
* Acúmulo automático de pontos em pedidos entregues
* Controle de consentimento LGPD

### Logs e Auditoria

* Registro de ações sensíveis
* Consulta administrativa de logs

### Multicanalidade

* Registro obrigatório do campo `canalPedido`
* Consulta de pedidos por canal

Canais suportados:

* APP
* TOTEM
* BALCAO
* PICKUP
* WEB

---

## Endpoints Disponíveis

### Usuários

| Método | Endpoint     | Descrição                     |
| ------ | ------------ | ----------------------------- |
| POST   | /usuarios    | Criar usuário                 |
| GET    | /usuarios/me | Consultar usuário autenticado |

### Autenticação

| Método | Endpoint    | Descrição      |
| ------ | ----------- | -------------- |
| POST   | /auth/login | Realizar login |

### Unidades

| Método | Endpoint                        | Descrição                 |
| ------ | ------------------------------- | ------------------------- |
| GET    | /unidades                       | Listar unidades           |
| POST   | /unidades                       | Criar unidade             |
| GET    | /unidades/{unidade_id}          | Buscar unidade            |
| PUT    | /unidades/{unidade_id}          | Atualizar unidade         |
| GET    | /unidades/{unidade_id}/cardapio | Obter cardápio da unidade |

### Produtos

| Método | Endpoint               | Descrição         |
| ------ | ---------------------- | ----------------- |
| GET    | /produtos              | Listar produtos   |
| POST   | /produtos              | Criar produto     |
| GET    | /produtos/{produto_id} | Buscar produto    |
| PUT    | /produtos/{produto_id} | Atualizar produto |

### Estoques

| Método | Endpoint                       | Descrição                       |
| ------ | ------------------------------ | ------------------------------- |
| GET    | /estoques                      | Listar estoques                 |
| POST   | /estoques                      | Criar estoque                   |
| GET    | /estoques/unidade/{unidade_id} | Listar estoque por unidade      |
| POST   | /estoques/entradas             | Registrar entrada de estoque    |
| GET    | /estoques/movimentos           | Listar movimentações de estoque |

### Pedidos

| Método | Endpoint                    | Descrição                  |
| ------ | --------------------------- | -------------------------- |
| POST   | /pedidos                    | Criar pedido               |
| GET    | /pedidos                    | Listar pedidos             |
| GET    | /pedidos/{pedido_id}        | Buscar pedido              |
| PATCH  | /pedidos/{pedido_id}/status | Atualizar status do pedido |

### Pagamentos

| Método | Endpoint    | Descrição       |
| ------ | ----------- | --------------- |
| POST   | /pagamentos | Criar pagamento |

### Fidelidade

| Método | Endpoint              | Descrição                 |
| ------ | --------------------- | ------------------------- |
| GET    | /fidelidades/saldo    | Consultar saldo de pontos |
| POST   | /fidelidades/resgatar | Resgatar pontos           |

### Auditoria

| Método | Endpoint         | Descrição                   |
| ------ | ---------------- | --------------------------- |
| GET    | /logs-auditorias | Consultar logs de auditoria |

---

## Fluxo Principal

1. Usuário realiza login
2. Cliente cria pedido
3. Sistema valida disponibilidade de estoque
4. Pagamento mock é processado
5. Pedido muda para EM_PREPARO
6. Funcionário/Cozinha atualiza o status
7. Pedido é entregue
8. Pontos de fidelidade são creditados automaticamente

---

## Segurança e LGPD

* Senhas armazenadas utilizando hash
* Autenticação JWT
* Controle de acesso baseado em perfis
* Consentimento LGPD para programa de fidelidade
* Fidelidade condicionada ao consentimento do usuário
* Auditoria de ações sensíveis
* Senhas nunca retornadas pela API

---

## Pagamento Mock

O sistema utiliza um serviço de pagamento simulado para fins acadêmicos.

Resultados possíveis:

* APROVADO
* RECUSADO
* ERRO

Quando aprovado:

* O pagamento é registrado
* O pedido muda automaticamente para `EM_PREPARO`

Quando recusado ou ocorre erro:

* O pagamento é registrado
* O pedido permanece aguardando nova tentativa de pagamento

---

## Requisitos Não Funcionais Atendidos

### Segurança

* Senhas com hash
* Autenticação JWT
* Controle de acesso por perfil
* Consentimento LGPD

### Auditoria

* Registro de ações sensíveis
* Histórico de auditoria consultável por administradores

### Disponibilidade

* API REST documentada via Swagger/OpenAPI
* Banco criado automaticamente na inicialização

### Tolerância a Falhas

* Simulação de falhas na integração de pagamento
* Tratamento de pagamentos recusados
* Tratamento de erros de integração

### Controle de Estoque

* Entrada de estoque
* Saída automática por venda
* Devolução automática em cancelamentos
* Restrição de venda por indisponibilidade

---

## Fluxo Sugerido para Testes

1. Criar usuário ADMIN
2. Realizar login
3. Criar unidade
4. Criar produto
5. Criar estoque
6. Criar cliente
7. Criar pedido
8. Processar pagamento
9. Atualizar status do pedido
10. Consultar fidelidade
11. Consultar logs de auditoria

---

## Autor

Wagner Ullrich

Projeto Multidisciplinar – Trilha Back-End – UNINTER
