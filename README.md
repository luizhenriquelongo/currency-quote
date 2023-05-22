# Currency Quote

Este repositório contém um projeto Django que permite obter as cotações de moedas estrangeiras usando a API de conversão de moedas. Com base em uma taxa de câmbio atualizada, é possível obter as cotações de moedas.

## Deploy

Para acessa a versão com o deploy feito acesse a seguinte URL:
- https://currency-quote-production.up.railway.app/

Acesse também a documentação dos endpoints:
- https://currency-quote-production.up.railway.app/api/docs

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter o seguinte:

- **Python 3.10**: É necessário ter o Python 3.10 instalado em sua máquina. Você pode baixar o Python em [python.org](https://www.python.org).

- **Poetry**: O Poetry é uma ferramenta de gerenciamento de dependências e ambientes virtuais para o Python. Certifique-se de ter o Poetry instalado em sua máquina. Para obter instruções de instalação, consulte a documentação oficial do Poetry em [python-poetry.org](https://python-poetry.org/docs/#installation).

## Instalação

Siga as instruções abaixo para executar o projeto em seu ambiente local:

### Clone o repositório 
```bash
git clone https://github.com/luizhenriquelongo/currency-quote.git
```

### Instalação manual:
1. **Navegue até o diretório `backend/`**:
```bash
cd backend/
```

2. **Instale as dependências**: Navegue até o diretório do projeto e instale as dependências necessárias executando o seguinte comando:
```bash
poetry install
```

3. **Execute as migrações**: Navegue até o diretório do projeto e execute as migrações do Django usando o seguinte comando:
```bash
poetry run python manage.py migrate
```

4. **Colete os arquivos estáticos**: Execute o seguinte comando para coletar os arquivos estáticos:
```bash
poetry run python manage.py collectstatic
```
5. **Popule a tabela de moedas**: Execute o seguinte comando para popular a tabela de moedas com base nas informações fornecidas pela VATComply API:
```bash
poetry run python manage.py populate_currencies_table
```

### Instalação utilizando Make:

```bash
make build
```

## Como Usar
1. **Inicie o servidor**: De dentro da pasta `backend/`, inicie o servidor Django com o seguinte comando:
```bash
poetry run python manage.py runserver
```
ou
```bash
make run
```
2. **Acesse a aplicação**: Abra seu navegador e acesse a URL: `http://localhost:8000/`

## Endpoints

A seguir estão os endpoints disponíveis na API:

- `GET /api/rates/`: Retorna as cotações de moedas atualizadas.

- `GET /api/docs/`: Retorna a documentação da API com detalhes sobre os endpoints disponíveis.

## Testes

Para executar os testes do projeto, rode o seguinte comando:

```bash
poetry run tox
```

Isso executará os testes automatizados e fornecerá informações sobre os resultados.

## Contribuição
Contribuições são bem-vindas! Se você encontrar algum problema, tiver alguma ideia ou quiser melhorar este projeto, fique à vontade para abrir uma "issue" ou enviar uma "pull request".

## Licença
Este projeto está licenciado sob a licença MIT.