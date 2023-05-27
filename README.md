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
