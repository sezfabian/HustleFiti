from flask_restx import Resource, Namespace
from ...models.service import Service
from .api_models import service_model

ns = Namespace('api')

ns.route('/services')
class ServicesListApi(Resource):
    """get all services"""
    @ns.marshal_list_with(service_model)
    def get(self):
        return Service.query.all()


