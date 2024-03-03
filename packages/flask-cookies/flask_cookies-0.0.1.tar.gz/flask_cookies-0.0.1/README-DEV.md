Try to create a package for flask-cookies
```
FLASK_COOKIE_DIR=/home/enrico/Dropbox/APP/flask-cookie/v0
PYTHON_PACKAGE_DIR=/home/enrico/Dropbox/PyPi/cookies-v0

mkdir $PYTHON_PACKAGE_DIR/src
mkdir $PYTHON_PACKAGE_DIR/src/flask_cookies
mkdir $PYTHON_PACKAGE_DIR/src/flask_cookies/templates/cookies
mkdir $PYTHON_PACKAGE_DIR/src/flask_cookies/static
mkdir $PYTHON_PACKAGE_DIR/tests

cp $FLASK_COOKIE_DIR/cookies.html $PYTHON_PACKAGE_DIR/src/flask_cookies/templates/cookies
cp $FLASK_COOKIE_DIR/cookies.css $PYTHON_PACKAGE_DIR/src/flask_cookies/static
cp $FLASK_COOKIE_DIR/cookies-logo.png $PYTHON_PACKAGE_DIR/src/flask_cookies/static

atom $PYTHON_PACKAGE_DIR/pyproject.toml
atom $PYTHON_PACKAGE_DIR/LICENSE
atom $PYTHON_PACKAGE_DIR/README.md
```

Test it locally
```
cp -r /home/enrico/flasket-app /tmp
cd /tmp/flasket-app

cd $PYTHON_PACKAGE_DIR
python3.9 -m venv venv
source venv/bin/activate
python -m pip install flask
python test0.py
```

Create a template:
```
mkdir templates
atom templates/ciao.html

python test0.py
```

Generate distribution archives: https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives
```
deactivate
cd $PYTHON_PACKAGE_DIR
python3.9 -m pip install --upgrade build
python3.9 -m build
```
Then upload it:
```
python3.9 -m twine upload --repository testpypi dist/*
```


Try to install in new app:
```
cp -r /tmp/flasket-app  /tmp/flasket-app1
cd /tmp/flasket-app1
# python3.9 -m venv venv
source venv/bin/activate
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps flask-cookies-cccnrc
flask run

atom app/__init__.py
atom app/templates/base.html
```

Upload to real PyPi
```

```
