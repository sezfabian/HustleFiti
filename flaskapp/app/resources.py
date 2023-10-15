from flask_restx import Resource, Namespace
from models.service import Service, ServiceCategory, PricePackage
from models.contract import Contract
from models.reviews import ServiceReview, ClientReview
from .api_models import services_model, service_model_input, service_category_model, service_category_model_input, price_packages_model, price_packages_model_input, contract_model, contract_model_input, service_reviews_model, service_reviews_model_input, client_reviews_model, client_reviews_model_input
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


@ns.route('/service/<string:id>')
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


@ns.route('/service_category/<string:id>')
class ServiceCategoryApi(Resource):
    @ns.marshal_with(service_category_model)
    def get(self, id):
        service_category = db.session.execute(db.select(ServiceCategory).filter_by(id=id)).scalar_one()
        return service_category, 200

    @ns.doc(params={'id': 'A UUID identifier in string format (e.g., "a1a184da-4be6-4c3e-9d4f-5ed3eb5ff8f7")'})
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

@ns.route('/price_packages/<string:id>')
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


@ns.route('/contract')
class ContractListApi(Resource):
    @ns.marshal_list_with(contract_model)
    def get(self):
        contracts = db.session.query(Contract).all()
        return [contract for contract in contracts], 200

    @ns.expect(contract_model_input)
    @ns.marshal_with(contract_model)
    def post(self):
        contract = Contract(
                user_id=ns.payload['user_id'],
                service_id=ns.payload['service_id'],
                location=ns.payload['location'],
                duration=ns.payload['duration'],
                price_package_id=ns.payload['price_package_id'],
                total_amount=ns.payload['total_amount'],
                contract_start_date=ns.payload['contract_start_date'],
                contract_end_date=ns.payload['contract_end_date'],
                contract_status=ns.payload['contract_status'],
                paid_amount=ns.payload['paid_amount'])
        db.session.add(contract)
        db.session.commit()
        return contract, 201

@ns.route('/contract/<string:id>')
class ContractApi(Resource):
    @ns.marshal_with(contract_model)
    def get(self, id):
        contract = db.session.execute(db.select(Contract).filter_by(id=id)).scalar_one()
        return contract, 200

    @ns.expect(contract_model_input)
    @ns.marshal_with(contract_model)
    def put(self, id):
        contract = db.session.execute(db.select(Contract).filter_by(id=id)).scalar_one()
        contract.user_id = ns.payload['user_id']
        contract.service_id = ns.payload['service_id']
        contract.location = ns.payload['location']
        contract.duration = ns.payload['duration']
        contract.price_package_id = ns.payload['price_package_id']
        contract.total_amount = ns.payload['total_amount']
        contract.contract_start_date = ns.payload['contract_start_date']
        contract.contract_end_date = ns.payload['contract_end_date']
        contract.contract_status = ns.payload['contract_status']
        contract.paid_amount = ns.payload['paid_amount']
        db.session.add(contract)
        db.session.commit()
        return contract, 201

    def delete(self, id):
        contract = db.session.execute(db.select(Contract).filter_by(id=id)).scalar_one()
        db.session.delete(contract)
        db.session.commit()
        return {}, 204


@ns.route('/service_review')
class ServiceReviewListApi(Resource):
    @ns.marshal_list_with(service_reviews_model)
    def get(self):
        service_reviews = db.session.query(ServiceReview).all()
        return [service_review for service_review in service_reviews], 200

    @ns.expect(service_reviews_model_input)
    @ns.marshal_with(service_reviews_model)
    def post(self):
        service_review = ServiceReview(
                user_id=ns.payload['user_id'],
                contract_id=ns.payload['contract_id'],
                service_id=ns.payload['service_id'],
                rating=ns.payload['rating'],
                comment=ns.payload['comment'])
        db.session.add(service_review)
        db.session.commit()
        return service_review, 201

@ns.route('/service_review/<string:id>')
class ServiceReviewiApi(Resource):
    @ns.marshal_with(service_reviews_model)
    def get(self, id):
        service_review = db.session.execute(db.select(ServiceReview).filter_by(id=id)).scalar_one()
        return service_review, 200

    @ns.expect(service_reviews_model_input)
    @ns.marshal_with(service_reviews_model)
    def put(self, id):
        service_review = db.session.execute(db.select(ServiceReview).filter_by(id=id)).scalar_one()
        service_review.user_id = ns.payload['user_id']
        service_review.contract_id = ns.payload['contract_id']
        service_review.service_id = ns.payload['service_id']
        service_review.rating = ns.payload['rating']
        service_review.comment = ns.payload['comment']
        db.session.add(service_review)
        db.session.commit()
        return service_review, 201

    def delete(self, id):
        service_review = db.session.execute(db.select(ServiceReview).filter_by(id=id)).scalar_one()
        db.session.delete(service_review)
        db.session.commit()
        return {}, 204


@ns.route('/client_review')
class ClientReviewListApi(Resource):
    @ns.marshal_list_with(client_reviews_model)
    def get(self):
        client_reviews = db.session.query(ClientReview).all()
        return [client_review for client_review in client_reviews], 200

    @ns.expect(client_reviews_model_input)
    @ns.marshal_with(client_reviews_model)
    def post(self):
        client_review = ClientReview(
                contract_id=ns.payload['contract_id'],
                user_id=ns.payload['user_id'],
                rating=ns.payload['rating'],
                comment=ns.payload['comment'])
        db.session.add(client_review)
        db.session.commit()
        return client_review, 201

@ns.route('/client_review/<string:id>')
class ClientReviewApi(Resource):
    @ns.marshal_with(client_reviews_model)
    def get(self, id):
        client_review = db.session.execute(db.select(ClientReview).filter_by(id=id)).scalar_one()
        return client_review, 200

    @ns.expect(client_reviews_model_input)
    @ns.marshal_with(client_reviews_model)
    def put(self, id):
        client_review = db.session.execute(db.select(ClientReview).filter_by(id=id)).scalar_one()
        client_review.contract_id = ns.payload['contract_id']
        client_review.user_id = ns.payload['user_id']
        client_review.rating = ns.payload['rating']
        client_review.comment = ns.payload['comment']
        db.session.add(client_review)
        db.session.commit()
        return client_review, 201
    
    def delete(self, id):
        client_review = db.session.execute(db.select(ClientReview).filter_by(id=id)).scalar_one()
        db.session.delete(client_review)
        db.session.commit()
        return {}, 204
