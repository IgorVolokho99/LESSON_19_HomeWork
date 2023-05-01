from flask_restx import Resource, Namespace
from flask import request

from decorators import auth_required, admin_required
from dao.model.director import DirectorSchema
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        request_json = request.json
        director_service.create()
        return "", 201


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        request_json = request.json
        if "id" not in request_json:
            request_json["id"] = rid

        director_service.update(request_json)

    @admin_required
    def delete(self, rid):
        director_service.delete(rid)
        return "", 204