import pip, os

_all_ = [
    "Django==1.9.1",
    "gunicorn==19.4.5",
    "whitenoise==2.0.6",
]

heroku = [
    "psycopg2=2.6.1",
]

ON_PAAS = 'DATABASE_URL' in os.environ

def install(packages):
    for package in packages:
        pip.main(['install', package])

if __name__ == '__main__':
    install(_all_)

    if(ON_PAAS):
        install(heroku)
