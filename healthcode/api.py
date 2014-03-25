from flask import Flask
#from flask.ext import restless
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

class ApiTest(restful.Resource):
    def get(self):
        return {'api': 'test'}

api.add_resource(ApiTest, '/')

if __name__ == '__main__':
    app.run(debug=True)
