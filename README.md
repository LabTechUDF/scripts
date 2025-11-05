## **Overview**

O objetivo desse projeto é atualizar a database por meio de uma planilha disponibilizada e 
registrar e comparar mudanças entre o que ja existia na database
e o que foi adicionado via planilha.

## **Estrutura do Projeto**

Esse projeto é dividido em varias etapas que são então executadas em sequencia pelo
arquivo main.py, sendo elas:

- **1 - A extração dos dados disponibilizados pela planiha no diretório "jsonfiles" em formato .json**
- **2 - A extração dos dados já existentes na database no diretório "oldjsonfiles" em formato .json**
- **3 - O processamento e comparação dos dados presentes nos arquivos .json dos 2 diretórios citados acima, onde os resultados desse processamento é salvo no diretório "comparedjsonfiles" também em formato .json**
- **4 - O envio dos dados processados (dados presentes no diretório "comparedjsonfiles") para a database mongodb**

## **Execução do Projeto**

Para executar o projeto primeiramente é necessário utilizar certas ferramentas, sendo elas:

- **1) MongoDB no Docker**:

Para rodar este projeto a melhor prática seria executá-lo com uma database local replicada 
da database presente no servidor. Para isso é utilizado uma database mongodb local presente dentro do docker.

- Instalação do Docker:

Para instalar o Docker, o recomendado seria realizar o download do "Docker Desktop", que pode ser feita atraves do site oficial: https://www.docker.com/get-started

- Executando o Docker Compose:

Para executar o docker compose, basta executar o seguinte comando no terminal:

```docker compose up -d```


OBS) Certifique-se de estar dentro e somente dentro da pasta "scripts" (a pasta raiz do projeto)

- Verificando a execução da database dentro do MongoDB Compass:

É utilizado a ferramenta MongoDB Compass para analizar os dados da database local. Para instalar o MongoDB Compass, basta baixar por meio do site oficial: https://www.mongodb.com/try/download/compass

Assim que o MongoDB Compass estiver aberto, clique no "+" na parte superior esquerda e verifique se a URI é:

```mongodb://localhost:27017```

Caso a URI estiver correta, clique em "Connect" e aguarde a mensagem de sucesso. Deverá aparecer uma nova conexão local com somente
3 databases presentes: "admin", "config" e "local".

**OBS) Em alguns casos (principalmente no windows) pode ocorrer a criação de uma outra database local "fantasma" que não está relacionada com a database configurada no docker.**

- Para verificar se isso está acontecendo, basta parar o container criado previamente, utilizando o Docker Desktop e executar um "refresh" dentro da conexão local no MongoDB Compass.

- Caso o "refresh" seja realizado com sucesso, isso indica que existe uma database local "fantasma" e deve ser excluida.

- **Removendo a conexão com a database local "fantasma"**:
Primeiramente, execute o powershell como administrador e execute o seguinte comando:
```netstat -ano | findstr :27017```

Caso seja retornado algum resultado com "LISTENING", execute o seguinte comando:
- ``` taskkill /PID {PID DO PROCESSO LISTADO COMO LISTENING} /F```

Após isso, execute o container no Docker Desktop e realize a conexão via MongoDB Compass normalmente.

- **2) Replicando a database do servidor para a database local**:

Após a configuração do docker e da database, é necessário replicar os dados da database do servidor para a database local. Para isso é utilizado os seguintes comandos:

- Extraindo os dados da database do servidor para uma pasta no computador:

```mongodump --uri="mongodb+srv://labtech:L4bT&ch4R@dwcorp.y5ugild.mongodb.net/{NOME DA DATABASE}" --out={NOME DA DATABASE}```

Quando executado, este comando criará uma pasta com o mesmo nome da database replicada localizada no diretorio onde o codigo foi executado, que conterá os dados da database em formato .json

- Replicando os dados da pasta no computador para a database local:

```mongorestore --uri="mongodb+srv://labtech:L4bT&ch4R@cluster1prod.2ajqoe5.mongodb.net/rooms-reservation-app" {NOME DA DATABASE}/{NOME DA DATABASE}```

OBS) Execute este comando no local onde a pasta com os dados da database foi criada.

- **3) Baixando as dependencias**:

Para baixar as dependencias, basta executar o seguinte comando dentro do diretorio do projeto:

```poetry install```

OBS) Caso não funcionar, baixe as dependencias necessarias utilizando o comando:

```pip install {NOME DA DEPENDENCIA}```

## **Executando o Projeto**:

Para executar o projeto, basta rodar o arquivo main.py