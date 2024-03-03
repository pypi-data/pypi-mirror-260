from src import Cookies

### and add it to a Flask hello world application
from flask import Flask, render_template

GTM_ID = 'GTM-NXWSMNRF'
cookies = Cookies(GTM_ID)

app = Flask(__name__)

cookies.init_app(app)

@app.route('/')
def index():
    return( render_template( 'ciao.html' ))

app.run(host='127.0.0.12', port=5555, debug=True)
