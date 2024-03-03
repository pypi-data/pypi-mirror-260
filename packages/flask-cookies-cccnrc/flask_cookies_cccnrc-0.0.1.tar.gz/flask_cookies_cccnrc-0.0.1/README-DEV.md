Try to create a package for flask-cookies
```
FLASK_COOKIE_DIR=/home/enrico/Dropbox/APP/flask-cookie/v0
PYTHON_PACKAGE_DIR=/home/enrico/Dropbox/PyPi/test-cookies-v0

mkdir $PYTHON_PACKAGE_DIR/src
mkdir $PYTHON_PACKAGE_DIR/src/flask_cookies_cccnrc
mkdir $PYTHON_PACKAGE_DIR/src/flask_cookies_cccnrc/templates/cookies
mkdir $PYTHON_PACKAGE_DIR/src/flask_cookies_cccnrc/static
mkdir $PYTHON_PACKAGE_DIR/tests

cp $FLASK_COOKIE_DIR/cookies.html $PYTHON_PACKAGE_DIR/src/flask_cookies_cccnrc/templates/cookies
cp $FLASK_COOKIE_DIR/cookies.css $PYTHON_PACKAGE_DIR/src/flask_cookies_cccnrc/static
cp $FLASK_COOKIE_DIR/cookies-logo.png $PYTHON_PACKAGE_DIR/src/flask_cookies_cccnrc/static

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
cd $PYTHON_PACKAGE_DIR
python3.9 -m pip install --upgrade build
python3.9 -m build
```
