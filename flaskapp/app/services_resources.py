from flask_restx import Resource, Namespace
from models.service import Service
from .api_models import services_model, service_model_input
from .extensions import db

ns = Namespace('api')

@ns.route('/services')
class ServicesListApi(Resource):
    """get all services"""
    @ns.marshal_list_with(services_model)
    def get(self):
        services = db.session.query(Service).all()
        return [service for service in services], 200

    @ns.expect(service_model_input)
    @ns.marshal_with(services_model)
    def post(self):
        """post a new service"""
        service = Service(
                name=ns.payload['name'],
                user_id=ns.payload['user_id'],
                service_category_id=ns.payload['service_category_id'],
                description=ns.payload['description'],
                image_paths=ns.payload['image_paths'],
                video_paths=ns.payload['video_paths'],
                banner_paths=ns.payload['banner_paths'],
                is_verified=ns.payload['is_verified'])
        db.session.add(service)
        db.session.commit()
        return service, 201


@ns.route('/service/<int:id>')
class ServiceApi(Resource):
    @ns.marshal_with(services_model)
    def get(self, id):
        """get a single service"""
        service = db.session.execute(db.select(Service).filter_by(id=id)).scalar_one()
        return service, 200

    @ns.expect(service_model_input)
    @ns.marshal_with(services_model)
    def put(self, id):
        """modify existing service"""
        service = db.session.execute(db.select(Service).filter_by(id=id)).scalar_one()
        service.name = ns.payload['name']
        service.user_id = ns.payload['user_id']
        service.service_category_id = ns.payload['service_category_id']
        service.description = ns.payload['description']
        service.image_paths = ns.payload['image_paths']
        service.video_paths = ns.payload['video_paths']
        service.banner_paths = ns.payload['banner_paths']
        db.session.add(service)
        db.session.commit()
        return service, 201

    def delete(self, id):
        """delete a service"""
        service = db.session.execute(db.select(Service).filter_by(id=id)).scalar_one()
        db.session.delete(service)
        db.session.commit()
        return {},  204

