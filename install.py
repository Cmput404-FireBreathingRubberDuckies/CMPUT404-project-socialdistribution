import pip, os

psycopg2 = "psycopg2==2.6.1"

ON_PAAS = 'DATABASE_URL' in os.environ

def install(packages):
    for package in packages:
        pip.main(['install', package])

if __name__ == '__main__':
    f = open('requirements.txt', 'r')
    _all_ = [line.rstrip('\n') for line in f]

    if(not ON_PAAS):
        _all_.remove(psycopg2)

    print "Installing: ", _all_

    install(_all_)
