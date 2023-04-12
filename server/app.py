from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        response = make_response(
            {
                "message": "Hello Campers!"
            },
            200
            )
        return response 
api.add_resource(Index, '/')

class Campers(Resource):
    def get(self):
        campers = Camper.query.all()
        campers_dict_list = [camper.to_dict() for camper in campers]

        return make_response(
            campers_dict_list,
            200
        )
    
    def post(self):
        data = request.get_json()
        try:
            new_camper = Camper(
                name = data['name'],
                age = data['age']
            )
            db.session.add(new_camper)
            db.session.commit()
        except ValueError as e: 
            return make_response(
                e.__str__()
            , 422)
        
        return make_response(
            new_camper.to_dict(),
            201
        )

    
api.add_resource(Campers, '/campers')

class CampersById(Resource):
    def get(self, id):
        camper = Camper.query.filter(Camper.id == id).first()

        if not camper:
            return make_response(
                {"error": "camper not found"},
                404
            )
        
        return make_response(
            camper.to_dict(),
            200
        )
    
    def patch(self, id):
        camper = Camper.query.filter(Camper.id == id).first()
        data = request.get_json()
        # try:
        for attr in data:
            setattr(camper, attr, data[attr])
        
        db.session.add(camper)
        db.session.commit()
        # except ValueError as e: 
        # return make_response(
        #     e.__str__()
        # , 422)
        return make_response(
            camper.to_dict(),
            202
        )
    
    def delete(self, id):
        camper = Camper.query.filter(Camper.id == id).first()

        if not camper:
            return make_response(
                {"error": "camper not found"},
                404
            )
        
        db.session.delete(camper)
        db.session.commit()

        return make_response(
            {"message": "deleted successful"},
            202
        )

api.add_resource(CampersById, '/campers/<int:id>')

class Activites(Resource):
    def get(self):
        activites = Activity.query.all()
        activities_dict_list = [act.to_dict() for act in activites]

        return make_response(
            activities_dict_list,
            200
        )
api.add_resource(Activites, "/activities")

class ActivitesById(Resource):
    def get(self, id):
        activity = Activity.query.filter(Activity.id == id).first()

        return make_response(
            activity.to_dict(),
            200
        )
    
    def delete(self, id):
        activity = Activity.query.filter(Activity.id == id).first()

        db.session.delete(activity)
        db.session.commit()

        return make_response(
            {'message': 'deleted successfully'},
            202
        )

api.add_resource(ActivitesById, '/activities/<int:id>')

class Signups(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_signup = Signup(
                time = data['time'],
                camper_id = data['camper_id'],
                activity_id = data['activity_id']
            )
            db.session.add(new_signup)
            db.session.commit()
        except ValueError as e:
            return make_response(
                e.__str__(),
                422
            )
        return make_response(
            new_signup.to_dict(),
            201
        )

api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
