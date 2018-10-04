# Segundo Serviço

#### Descrição
Esse serviço é reponsável por:
- receber o nome da pessoa via POST
- gravar no banco de dados PostGre o nome da pessoa
- inserir na fila "request-tj-sp" o ID e o NOME da pessoa em forma de json
- ouvir a fila "response" para poder capturar os dados da pesquisa que vem do terceiro serviço
- atualizar no banco de dados a resposta que está na fila "response"

## Como utilizar
Após o clone do projeto você deve instalar os pacotes necessários. Para isso rode o comando abaixo no terminal:

```
pip install -r requirements.txt
```

Após a instalação dos pacotes execute o comando abaixo para inicar o servidor:

```
python main.py
```

Obs.: Você deve estar no diretório do projeto.


## Documentação API Rest

### {GET} /busca/:id

Busca um dado do banco de dados.

### {POST} /save

Body:
```
{
    name: string,
    response: string (OPCIONAL)
}
```

Salva um dado no banco de dados.

### {PATCH} /update/:id

Body:
```
{
    response: string
}
```

Atualiza um dado no banco de dados.
