Raízes do Nordeste — API Back-end

API REST desenvolvida para a disciplina Projeto Multidisciplinar – Trilha Back-End da UNINTER.

O projeto simula o sistema de uma rede de lanchonetes com múltiplas unidades e canais de atendimento, permitindo cadastro de usuários, gerenciamento de produtos, controle de estoque, pedidos, pagamentos simulados, fidelidade e auditoria.

Tecnologias Utilizadas
Python 3.10+
FastAPI
SQLAlchemy
SQLite
Pydantic
JWT
Uvicorn
Swagger/OpenAPI
Como Executar o Projeto
1. Clonar o repositório
git clone https://github.com/WagnerUllrich/api-lanchonete.git
cd api-lanchonete
2. Criar ambiente virtual
python -m venv .venv
3. Ativar ambiente virtual

Windows:

.venv\Scripts\activate
4. Instalar dependências
pip install -r requirements.txt
5. Configurar variáveis de ambiente

Criar um arquivo .env com base no .env.example.

Exemplo:

DATABASE_URL=sqlite:///./lanchonete.db
JWT_SECRET_KEY=sua_chave_secreta
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
6. Iniciar a aplicação
uvicorn app.main:app --reload

A API ficará disponível em:

http://127.0.0.1:8000
Banco de Dados

O projeto utiliza SQLite.

O banco é criado automaticamente na primeira execução da aplicação.

Arquivo gerado:

lanchonete.db

Também existe uma seed automática que cria um usuário administrador padrão caso ele ainda não exista.

Usuário padrão para testes

E-mail:

admin@gmail.com

Senha:

123456

Perfil:

ADMIN
Documentação da API

Swagger:

http://127.0.0.1:8000/docs

OpenAPI:

http://127.0.0.1:8000/openapi.json
Estrutura do Projeto

- api: contém os endpoints e rotas da API REST.
- core: contém os compongentes de segurança, autenticação JWT e controle de acesso.
- db: contém a configuração e conexão com o banco de dados.
- models: contém as entidades e tabelas do sistema.
- schemas: contém os contratos de entrada e saída da API, além das validações.
- utils: contém funções auxiliares e recursos de auditoria.
- main.py: responsável pela inicialização da aplicação, criação das tabelas e registro das rotas.

A pasta docs contém os diagramas e documentos do projeto, incluindo o DER e demais artefatos de modelagem.

A aplicação foi organizada em camadas para separar responsabilidades entre regras de negócio, persistência, autenticação e endpoints.

Principais Funcionalidades
Cadastro de usuários
Login com JWT
Controle de acesso por perfil
Gerenciamento de unidades
Gerenciamento de produtos
Controle de estoque por unidade
Criação e consulta de pedidos
Pagamento mock
Programa de fidelidade
Logs de auditoria
Suporte a múltiplos canais de venda (APP, TOTEM, BALCAO, PICKUP e WEB)
Fluxo Principal Implementado
Usuário realiza login
Produto e estoque são cadastrados
Cliente cria um pedido
O pagamento mock é processado
O pedido muda para EM_PREPARO
O status é atualizado para PRONTO
O pedido é marcado como ENTREGUE
Os pontos de fidelidade são creditados automaticamente
Coleção Postman

A coleção utilizada nos testes está disponível no repositório:

API Raízes do Nordeste.postman_collection.json

Para executar os testes:

Execute o teste T01 - Login válido
Copie o access_token retornado
Cole o valor na variável token do ambiente do Postman
Execute os demais testes da coleção
DER

O Diagrama Entidade-Relacionamento (DER) está disponível na pasta `docs` do projeto, juntamente com os demais diagramas.

Segurança e LGPD

O projeto implementa:

Senhas armazenadas com hash
Autenticação JWT
Controle de acesso por perfis
Consentimento LGPD para fidelidade
Auditoria de ações sensíveis
Padronização de erros da API
Senhas nunca retornadas nas respostas
Autor

Wagner Ullrich RU: 4819534

Projeto Multidisciplinar – Trilha Back-End – UNINTER