from flask import Flask
from flasgger import Swagger

from WebApi.controller.query import queryModule

app = Flask(__name__)
app.register_blueprint(queryModule)
Swagger(app)

@app.route('/')
def api_root():
    return 'Welcome to python，Swagger url：/apidocs/'

app.run(debug=True)
