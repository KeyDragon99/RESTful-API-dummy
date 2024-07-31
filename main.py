from flask import Flask, request
from flask_restful import Api, Resource, reqparse

rqp = reqparse.RequestParser()
rqp.add_argument('year', type=int)
rqp.add_argument('acceleration', type=int)

app = Flask(__name__)
api = Api(app)

class Car_Brands(Resource):

    def put(self, car_brand):
        args = rqp.parse_args()
        return {car_brand: args}
    
api.add_resource(Car_Brands, "/Car_Brands/<string:car_brand>")

if __name__ == "__main__":
    app.run(debug=True)
