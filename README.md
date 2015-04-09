# Simple html interface to browse jokes on mikroskeem’s server
It’s alive at http://jokes.mikroskeem.eu/

# Requierments
just plain stock python3 should do it but [uwsgi] usage is recommended

# How to run
in the project folder run

    python3 app.py

or use awesome [uwsgi] to run dev server
with auto reload on code change

    uwsgi --ini config.ini:dev


and then open http://127.0.0.1:8080/ in your browser

[uwsgi]: http://uwsgi-docs.readthedocs.org/
