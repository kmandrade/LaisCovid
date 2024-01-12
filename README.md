Projeto desenvolvido referente ao processo seletivo (EDITAL Nº 28/2023 – LAIS/UFRN).

Para rodar o projeto no Windows:
Crie um ambiente virtual com o comando: python -m venv venv
Ative o ambiente virtual com o comando: .\venv\Scripts\Activate.ps1
Instale as dependências com o comando: pip install -r  requirements.txt
Altere em lais_covid => settings.py as configurações de banco de dados para o seu ambiente local (atualmente configurado para uso do PostegreSql Local)
Atualize o banco de dados com o comando: python manage.py migrate
Rode o comando para popular os estabelecimentos: 
python manage.py popular_estabelecimentos https://selecoes.lais.huol.ufrn.br/media/estabelecimentos_pr.xml

Rode o projeto com o comando: python manage.py runserver
Tudo pronto! Basta utilizar a aplicação.