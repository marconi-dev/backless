# BackLess
Um removedor de backgrounds usando tarefas assíncronas que utiliza Postgres, Redis, AWS, Google Cloud, Django e outras tecnologias.
https://backless-yaswxasiza-uc.a.run.app/ (A primeira imagem demorará bem mais do que eu gostaria para ser finalizada)
# Instalação
1. Clone este repositório e vá para a raiz do projeto.
```
git clone https://github.com/marconi-dev/backless
cd backless
```
2. Crie o arquivo .env dentro do diretório da aplicação
```
> backless/.env
```
3. Preencha o arquivo com as seguintes informações
    - `DEBUG=<True|False>` Deixe em True para ter mais informações e rodar em localhost. Caso DEBUG seja False a aplicação tentará connectar com projeto da google cloud.
    - `ALLOWED_HOSTS=<str>` Use `*` para habilitar qualquer host ou `127.0.0.1 | localhost`.
    - `SECRET_KEY=<str>` Use `django.core.management.utils.get_random_secret_key` para gerar uma SECRET_KEY.
    - `DATABASE_URL=<str>` A url de um banco de dados Postgre.
    - `CSRF_TRUSTED_ORIGINS=<str>` Deixe em `http://localhost:8000` para rodar em localhost.
    - `PROJECT_NAME=<str>` O ID do seu projeto da google cloud. Utilize `dev` para rodar com o dockercompose.
    - `QUEUE_REGION=<str>` A região do seu projeto da google cloud. Utilize `here` para rodar em localhost.
    - `QUEUE_ID=<str>` O nome da sua fila na google cloud. Utilize `anotherq` para roder em localhost.
    - `WORKER_URL=<str>` O link do outro deploy da sua applicação. O worker vai apenas lidar com a remoção do background das images. Utilize `http://localhost:8001` para rodar em localhost.
    - `DEFAULT_FILE_STORAGE=<str>` Utilize `storages.backends.s3boto3.S3Boto3Storage` para conectar a uma instância do AWS S3. Utilize `django.core.files.storage.FileSystemStorage` para rodar em localhost. Para configurar a conexão com o S3, visite https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html 
    - `REDIS_URL=<str>` A url do redis. 
    - `WS_URL=<str>` A url do servidor web. Utilize `http://localhost:8000`.
4. Crie o arquivo `key.json` no diretório da aplicação e preencha com a chave de accesso da google cloud. Para rodar localmente, é usado o projeto cloud-tasks-emulator da comunidade de GO (https://github.com/aertje/cloud-tasks-emulator). Com isso é possível rodar o projeto sem utilizar a google cloud, mas de qualquer forma a lib usada para conectar com a cloud tasks vai pedir para ter uma key, válida ou não. Sugiro pedir para uma inteligência artificial para gerar uma key com campos válidos.  
```
> backless/key.json
``` 
5. Após fazer as configurações você deve ser capaz de rodar a aplicação com docker. Na raiz do projeto, onde há um arquivo docker-compose.yml, use o comando:
```
docker-compose up
```
# Preview do projeto
Há apenas duas telas. Uma para o usuário escolher a foto que terá o fundo retirada:

![image](https://github.com/marconi-dev/backless/assets/121608492/030ca81c-a51d-49b6-a2c7-33cc560ba372)
Uma tela de espera:

![image](https://github.com/marconi-dev/backless/assets/121608492/5aad5d3c-8900-485a-b9c8-a994225b5443)
Por fim, uma tela com o resultado:

![image](https://github.com/marconi-dev/backless/assets/121608492/947fdca5-480c-45e0-b190-f8722c38076d)

# Como funciona
![image](https://github.com/marconi-dev/backless/assets/121608492/61f76707-e6dc-414b-8464-604f9b9d1117)

<i>Item listados conforme as ações tomadas quando um usuário envia uma foto para ser tratada</i>
#### Backless web: 
   É o servidor que o usuário se conecta para interagir com a aplicação. Quando o usuário envia uma foto para ser tratada, essa imagem é salva e o usuário é redirecionado para uma sala de espera onde se conecta com um websocket que vai o manter informado. Simultaneamente uma task é criada na fila do projeto.
#### Postgre: 
   É usado o banco de dados Postgre para armazenar o caminho da foto. 
#### AWS S3:
   Enquanto o Postgre salva o caminho das imagens, o arquivo fica salvo num bucket da S3.
#### Cloud tasks
   O processo de remoção do fundo das imagens pode ser demorado, por isso foi utilizado um sistema de filas para melhorar (a experiência do usuário | o tempo de resposta). No ecossistema python normalmente se usa Celery. Contudo, para esse projeto, manter um worker de celery seria caro de mais. Por isso optei por usar a cloud tasks que lida com filas de forma diferente. Quando uma task é enviada para a fila, é feita uma requisição para o servidor (worker) que só então é usado. Enquanto com o Celery eu precisaria de um worker sempre conectado a algum sistema de filas ex: RabbitMQ ou Redis.
#### Backless worker:
   O servidor que fará o processamento da imagem. Quando recebe uma requisição (feita pela cloud tasks) é enviado um sinal para o usuário avisando que a foto dele está sendo processada. Ao remover o fundo da imagem, a imagem antiga é apagada do S3 e no lugar dela é enviada outra imagem com a extenção ".png" sem o fundo. Após isso a url da imagem é enviada via websocket para o usuário. Quando o usuário se desconectar do websocket a imagem será removida tanto do banco de dados quanto do bucket, com isso nenhuma imagem será armazenada, mantendo o free tier dos serviços utilizados.
#### Redis:
   O redis é usado pela lib Channels para armazenar informações sobre os grupos. É por estar conectado ao Redis que ambos os servidores (web|worker) podem enviar mensagens para o usuário.
