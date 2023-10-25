#  Criando uma API async com rate limit e testável

###  Sobre este tutorial:

-  O tutorial é didático e iremos utilizar um cenário de uma API simples de mensagens;
-  Não teremos tantas validações por conta do tempo do tutorial, então alguns cenários não estão cobertos;
-  Aceito contribuições no repositório do projeto;
-  A parte de banco de dados está toda pronta e não será coberta como parte do tutorial.
-  Como no tutorial não temos a implementação de autenticação, vamos usar o Postman ou qualquer outra aplicação que faça requisição passando a chave valor no header:

> x-real-ip: 168.227.17.187

###  Problema a ser resolvido:

Uma API de envio de mensagens, cujas funcionalidades serão:

-  Criar um usuário
-  Listar os usuários
-  Ver os detalhes de um usuário
-  Enviar uma mensagem para um usuário
-  Listar mensagens
-  Ver os detalhes de uma mensagem
-  Responder mensagem
-  Encaminhar mensagem para um usuário
-  Apagar mensagem

### Executando o Projeto:

Antes de rodar o projeto, execute:

```
pip install -r requirements.txt
```

Para rodar o projeto, execute:

```
uvicorn main:app --reload
```

Para rodar os testes, execute:

```
pytest tests
```
