from flask_restx import Resource, Namespace
from models.service import Service, ServiceCategory, PricePackage
from .api_models import services_model, service_model_input, service_category_model, service_category_model_input, price_packages_model, price_packages_model_input
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


@ns.route('/service_category')
class ServiceCategoryListApi(Resource):
    """get all services categories"""
    @ns.marshal_list_with(service_category_model)
    def get(self):
        service_categories = db.session.query(ServiceCategory).all()
        return [service_category for service_category in service_categories], 201

    @ns.expect(service_category_model_input)
    @ns.marshal_with(service_category_model)
    def post(self):
        service_category = ServiceCategory(name=ns.payload['name'], sub_categories=ns.payload['sub_categories'])
        db.session.add(service_category)
        db.session.commit()
        return service_category, 201


@ns.route('/service_category/<int:id>')
class ServiceCategoryApi(Resource):
    @ns.marshal_with(service_category_model)
    def get(self, id):
        service_category = db.session.execute(db.select(ServiceCategory).filter_by(id=id)).scalar_one()
        return service_category, 200

    @ns.expect(service_category_model_input)
    @ns.marshal_with(service_category_model)
    def put(self, id):
        service_category = db.session.execute(db.select(ServiceCategory).filter_by(id=id)).scalar_one()
        service_category.name = ns.payload['name']
        service_category.sub_categories = ns.payload['sub_categories']
        db.session.add(service_category)
        db.session.commit()
        return service_category, 201

    def delete(self, id):
        service_category = db.session.execute(db.select(ServiceCategory).filter_by(id=id)).scalar_one()
        db.session.delete(service_category)
        db.session.commit()
        return {}, 204


@ns.route('/price_packages')
class PricePackageListApi(Resource):
    """get all price packages"""
    @ns.marshal_list_with(price_packages_model)
    def get(self):
        price_packages = db.session.query(PricePackage).all()
        return [price_package for price_package in price_packages], 200

    @ns.expect(price_packages_model_input)
    @ns.marshal_with(price_packages_model)
    def post(self):
        price_package = PricePackage(
                name=ns.payload['name'],
                service_id=ns.payload['service_id'],
                description=ns.payload['description'],
                price=ns.payload['price'],
                duration=ns.payload['duration'])
        db.session.add(price_package)
        db.session.commit()
        return price_package, 201

@ns.route('/price_packages/<int:id>')
class PricePackagesApi(Resource):
    @ns.marshal_with(price_packages_model)
    def get(self, id):
        price_package = db.session.execute(db.select(PricePackage).filter_by(id=id)).scalar_one()
        return price_package, 200

    @ns.expect(price_packages_model_input)
    @ns.marshal_with(price_packages_model)
    def put(self, id):
        price_package = db.session.execute(db.select(PricePackage).filter_by(id=id)).scalar_one()
        price_package.name = ns.payload['name']
        price_package.service_id = ns.payload['service_id']
        price_package.description = ns.payload['description']
        price_package.price = ns.payload['price']
        price_package.duration = ns.payload['duration']
        db.session.add(price_package)
        db.session.commit()
        return price_package, 201
    
    def delete(self, id):
        price_package = db.session.execute(db.select(PricePackage).filter_by(id=id)).scalar_one()
        db.session.delete(price_package)
        db.session.commit()
        return {}, 204
