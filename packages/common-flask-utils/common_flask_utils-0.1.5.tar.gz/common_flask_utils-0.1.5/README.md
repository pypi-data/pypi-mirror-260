# common flask utils
This utils is use some of python package to enhance flask.Flask.

All of this usage you can see in [ flask ]( https://github.com/pallets/flask )

# requirement
Use following libraries to enhance Flask.

- [ flask-sqlalchemy ]( https://github.com/pallets-eco/flask-sqlalchemy )
    > Is a extension for Flask that adds  support for [ SQLAlchemy ]( https://www.sqlalchemy.org/ ) to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

- [ python-i18n ]( https://github.com/danhper/python-i18n )
    > This library provides i18n functionality for Python3 out of the box. The usage is mostly based on Rails i18n library.

- [ pyjwt ]( https://github.com/jpadilla/pyjwt )
    > This library provides jwt token for Python3. Python implementation of [ RFC 7519 ]( https://github.com/jpadilla/pyjwt?tab=readme-ov-file )

- [ flask-cors ]( https://github.com/corydolphin/flask-cors )
    > A Flask extension for handling Cross Origin Resource Sharing(CORS), making cross-origin AJAX possible.

# installation

```SHELL
pip install common-flask-utils
```

# usage
## base usage
```PYTHON
from common_utils import Flask

app: Flask = Flask(__name__)
app.run()
```
## auto register blueprint

```PYTHON
from common_utils import Flask
app: Flask = Flask(__name__, controller_scan_dir = "app.modules")
app.run()
```
or 

```PYTHON
from common_utils import Flask, blueprint_registration
app: Flask = Flask(__name__)
blueprint_registration(app, blueprint_dir="app.modules")
app.run()
```

you should use Outlining to init controller like blueprint and place it inside modules package.

like:

```python
# app/modules/controller.py 
controller: Outlining = Outlining("Root", __name__, url_prefix="/root")

@controller.get("")
def index():
    return "root page"
```

after that, you can visit webpage use url like: http://localhost:5000/root, if you are not change host and port in config or pass it through app.run()

if inside app.modules you have sub package, like:

```python
# app/modules/v1/controller.py
controller: Outlining = Outlining("Root", __name__, url_prefix="/root")

@controller.get("")
def index():
    return "root page"
```
then you can visit webpage use url like: http://localhost:5000/v1/root

auto blueprint registration is provide by method @see: **blueprint_registration** in side **common_utils/utils/blueprint_util.py**























