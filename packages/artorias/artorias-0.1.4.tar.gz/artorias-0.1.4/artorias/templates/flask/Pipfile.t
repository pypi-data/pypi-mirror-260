[[source]]
url = "https://mirrors.aliyun.com/pypi/simple/"
verify_ssl = true
name = "aliyun"

[packages]
artorias = "*"

[dev-packages]
pytest = "*"
pytest-mock = "*"
pre-commit = "*"
flask-shell-ipython = "*"

[scripts]
serve = "gunicorn -c gunicorn.conf.py wsgi:app"

[requires]
python_version = "$python_version"
