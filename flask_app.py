from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Calendar(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        name = request.args['name']
        day = request.args['day']
        month = request.args['month']

        data = pd.read_csv('users.csv')

        new_data = pd.DataFrame({
            'name': [name],
            'day': [day],
            'month': [month]
        })

        data = data.append(new_data, ignore_index=True)
        data.to_csv('users.csv', index=False)
        return {'data': new_data.to_dict('records')}, 200

    def delete(self):
        name = request.args['name']
        data = pd.read_csv('users.csv')
        data = data[data['name'] != name]

        data.to_csv('users.csv', index=False)
        return {'message': 'Record deleted successfully.'}, 200


class Ay(Resource):
    def get(self):
        data = pd.read_csv('users.csv', usecols=[2])
        data = data.to_dict('records')

        return {'data': data}, 200


class Name(Resource):
    def get(self, name):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name:
                return {'data': entry}, 200
        return {'message': 'No entry found with this name !'}, 404


# Add URL endpoints
api.add_resource(Calendar, '/calendar')
api.add_resource(Ay, '/ay')
api.add_resource(Name, '/<string:name>')

if __name__ == '__main__':
    #     app.run(host="0.0.0.0", port=5000)
    app.run("localhost", 8080)
