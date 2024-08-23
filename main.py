from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os.path, csv

base_rqp = reqparse.RequestParser()                                         #Define request parser values and their properties
base_rqp.add_argument('id', type=int)                                       #for basic entry handling in the database
base_rqp.add_argument('name', type=str)
base_rqp.add_argument('mpg', type=float)
base_rqp.add_argument('cylinders', type=int)
base_rqp.add_argument('displacement', type=float)
base_rqp.add_argument('horsepower', type=float)
base_rqp.add_argument('weight', type=float)
base_rqp.add_argument('acceleration', type=float)
base_rqp.add_argument('model_year', type=int)
base_rqp.add_argument('origin', type=str)

del_rqp = reqparse.RequestParser()                                          #Define request parser values for deleting entries
del_rqp.add_argument('id', type=int, required=True, help='Id is required in order to delete a car model.')

year_rqp = reqparse.RequestParser()
year_rqp.add_argument('model_year_1', type=int, required=True, help='Two year dates are required to search in year range')
year_rqp.add_argument('model_year_2', type=int, required=True, help='Two year dates are required to search in year range')

app = Flask(__name__)                                                       #Initialize the flask application for the API
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'             #Define the database URI
db = SQLAlchemy(app)

class CarModel(db.Model):                                                   #Define the columns of the database
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)
    mpg = db.Column(db.Float, nullable=True)
    cylinders = db.Column(db.Integer, nullable=True)
    displacement = db.Column(db.Float, nullable=True)
    horsepower = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    acceleration = db.Column(db.Float, nullable=True)
    model_year = db.Column(db.Integer, nullable=True)
    origin = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return (f"Car:(name: {self.name}, mpg: {self.mpg}, cylinders: {self.cylinders}, "
                f"displacement: {self.displacement}, horsepower: {self.horsepower}, weight: {self.weight}, "
                f"acceleration: {self.acceleration}, model_year: {self.model_year}, origin: {self.origin})")

if not os.path.isfile('./instance/database.db'):                            #Check if database already exists, if not, create it
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
            
resource_fields = {                                                         #Define the resource fields that will be returned
    'id': fields.Integer,                                                   
    'name': fields.String,
    'mpg': fields.Float,
    'cylinders': fields.Integer,
    'displacement': fields.Float,
    'horsepower': fields.Float,
    'weight': fields.Float,
    'acceleration': fields.Float,
    'model_year': fields.Integer,
    'origin': fields.String,
    'message': fields.String
}

class Car_Brands(Resource):

    @app.route('/get_models', methods=['GET'])                                     #Define the flask request route 
    @marshal_with(resource_fields)                                          #Marshal the return with the defined resource fields
    def get_model(self):                                                         #Find and return the searched entries
        filtered_args = {k: v for k, v in base_rqp.parse_args().items() if v}    #Filter the arguments given by the user so that 
                                                                            #there are no empty values
        result = CarModel.query.filter_by(**filtered_args).all()            #Filter the database with the given arguments

        if not result:                                                      #If no result was found, abort
            abort(404, message="None found.")

        return result
    
    # @app.route('/post_entry', methods=['POST'])
    # @marshal_with(resource_fields)                                          
    # def post_new_entries(self):
    #     filtered_args = {k: v for k, v in base_rqp.parse_args().items() if v}    
    #     result = CarModel.query.filter_by(**filtered_args).all() 

    #     if not result:                                                      #Check if there are any entries in the database with 
    #                                                                         #the exact same attributes with the ones given by the user
    #         try:                                                            #Try to insert the new object in the database
    #             with app.app_context():
    #                 model = CarModel(**filtered_args)
    #                 db.session.add(model)
    #                 db.session.commit()
    #         except IntegrityError as x:                                     #Catch integrity errors
    #             print("error:", x)
    #             abort(409, description=x)
    #         except:                                                         #Catch any other errors
    #             abort(500, description="There was an error with your request.")
    #     else:                                                                   
    #         abort(409, description="A car with the same characteristics already exist.")    #In case there is another entry
    #                                                                                         #very similar to the one given, abort

    #     return {**filtered_args, "message": "Car model added successfully!"}
    
    # @app.route('/delete', methods=['DELETE'])
    # @marshal_with(resource_fields)
    # def delete(self):                                                     #Delete the entry matching the given id
    #     filtered_args = {k: v for k, v in del_rqp.parse_args().items() if v}    #Filter the arguments given by the user so that there 
    #                                                                             #are no empty values
        
    #     try:
    #         with app.app_context():
    #             result = db.session.get(CarModel, filtered_args['id'])      #Get the object with the specified id given by the user
    #             db.session.delete(result)                                   #Delete the entry from the database
    #             db.session.commit()
    #     except:
    #         abort(500, description="There was an error deleting a car model.")

    #                                                                         #Get the values from the result object
    #     result_val = {column.name: getattr(result, column.name) for column in result.__table__.columns} 
        
    #     return {'message': 'Car model deleted successfully!', **result_val}

# class Year_Comparison(Resource):

#     @app.route('/get_year_range', methods=['GET'])
#     @marshal_with(resource_fields)
#     def get_year_range(self):

#         args = year_rqp.parse_args()
#         result = db.session().query(CarModel).filter(CarModel.model_year.between(args['model_year_1'], args['model_year_2'])).all()

#         return result

                                                                                            #Add a resource to the API
api.add_resource(Car_Brands, "/Car_Brands/get_models", "/Car_Brands/delete", "/Car_Brands/post_entry")   #<int:car_id> 
# api.add_resource(Year_Comparison, "/Year_Comparison/get_year_range")

if __name__ == "__main__":
    app.run(debug=True)
