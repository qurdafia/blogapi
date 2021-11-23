# Blog API
This is a simple implemtation of Blog API in Django REST Framework

Instructions:

1. Set up a local development environment (virtual environment) and install the required Django depedencies
2. You can use the requirements.txt file
3. This app uses PostgreSQL which installed locally (you may need to install the engine in your OS)
4. All sensitive information are not included in this repository like secret key and database credentials, you can install the Environ package and set up your .env file
5. Create a superuser if you want to test the admin
6. Use the JSON files for fixtures to be the parameters in seeding data (ex. python manage.py loaddata <fixturefile>)
7. This app uses the DRF TokenAuthentication, thus use Token for Authorization (ex. 'Authorization: Token <token>')