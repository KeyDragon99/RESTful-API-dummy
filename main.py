from flask import Flask, request
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
import os.path, csv

rqp = reqparse.RequestParser()
rqp.add_argument('id', type=int)
rqp.add_argument('name', type=str, required=True)
rqp.add_argument('mpg', type=float)
rqp.add_argument('cylinders', type=int)
rqp.add_argument('displacement', type=float)
rqp.add_argument('horsepower', type=float)
rqp.add_argument('weight', type=float)
rqp.add_argument('acceleration', type=float)
rqp.add_argument('model_year', type=int)
rqp.add_argument('origin', type=str)

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class CarModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    mpg = db.Column(db.Float, nullable=True)
    cylinders = db.Column(db.Integer, nullable=True)
    displacement = db.Column(db.Float, nullable=True)
    horsepower = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    acceleration = db.Column(db.Float, nullable=False)
    model_year = db.Column(db.Integer, nullable=True)
    origin = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return (f"Car:(name: {self.name}, mpg: {self.mpg}, cylinders: {self.cylinders}, "
                f"displacement: {self.displacement}, horsepower: {self.horsepower}, weight: {self.weight}, "
                f"acceleration: {self.acceleration}, model_year: {self.model_year}, origin: {self.origin})")

if not os.path.isfile('./instance/database.db'):
    with app.app_context():
        db.create_all()
        print('Database was created!')

    with open('Automobile.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        with app.app_context():
            for i, lines in enumerate(csvFile):
                if not i == 0:
                    lines = [None if s == "" else s for s in lines]
                    model = CarModel(name=lines[0], mpg=lines[1], cylinders=lines[2], 
                                     displacement=lines[3], horsepower=lines[4],
                                     weight=lines[5], acceleration=lines[6], 
                                     model_year=lines[7], origin=lines[8])
                    db.session.add(model)
                    db.session.commit()
            
resource_fields = {
    'name': fields.String,
    'mpg': fields.Float,
    'cylinders': fields.Integer,
    'displacement': fields.Float,
    'horsepower': fields.Float,
    'weight': fields.Float,
    'acceleration': fields.Float,
    'model_year': fields.Integer,
    'origin': fields.String
}

class Car_Brands(Resource):

    @marshal_with(resource_fields)
    def get(self):
        args = rqp.parse_args()
        filtered_args = {k: v for k, v in args.items() if v}
        result = CarModel.query.filter_by(**filtered_args).all()

        if not result:
            abort(404, message="None found.")
        return result
    
api.add_resource(Car_Brands, "/Car_Brands")    #<int:car_id>

if __name__ == "__main__":
    app.run(debug=True)
