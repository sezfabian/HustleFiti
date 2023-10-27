import uuid
from fastapi import APIRouter, HTTPException, Depends, Cookie, Path
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict
from models import storage
from models.user import User
from models.service import ServiceCategory, Service, PricePackage

service_router = APIRouter()

class ServiceCategoryCreate(BaseModel):
    name: str
    sub_categories: str

class ServiceCategoryUpdate(BaseModel):
    name: Optional[str] = None
    sub_categories: Optional[str] = None

class ServiceCreate(BaseModel):
    name: str
    description: str
    service_category_id: str
    locations: str = None
    sub_category: str =None
    image_paths: str = None
    video_paths: str = None
    banner_paths: str = None

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    service_category_id: Optional[str] = None
    sub_category: Optional[str] = None
    locations: Optional[str] = None
    image_paths: Optional[str] = None
    video_paths: Optional[str] = None
    banner_paths: Optional[str] = None

class PricePackageCreate(BaseModel):
    service_id: str
    name: str
    description: str
    price: float
    duration: Optional[str] = None

class PricePackageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[str] = None

#create service category
@service_router.post("/service_category", response_model=dict)
def create_service_category(category_data: ServiceCategoryCreate, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    user = storage.find_by(User, **{"session_id": session_id})

    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    if user.to_dict()["is_admin"] != False:
        raise HTTPException(status_code=403, detail="Unauthorized")


    category_data_dict = category_data.dict()

    if storage.find_by(ServiceCategory, **{"name": category_data_dict['name']}):
        raise HTTPException(status_code=409, detail="Service_Category already exists")
    try:
        category_data_dict["id"] = str(uuid.uuid4())
        new_category = ServiceCategory(**category_data.dict())
        storage.new(new_category)
        storage.save()
        return {"message": "Service_category created sucessfully", "service_category": new_category.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))

#Get list of service categories
@service_router.get("/service_categories", response_model=list)
async def get_service_categories():
    storage.reload()
    service_categories = storage.all(ServiceCategory).values()
    categories = []
    for category in service_categories:
        category_data = {
            "id": category.id,
            "name": category.name,
            "sub_categories": category.sub_categories
        }
        categories.append(category_data)
    
    return categories

# Get a service category by id
@service_router.get("/service_category/{id}", response_model=dict)
async def get_service_category(id: str):
    service_category = storage.find_by(ServiceCategory, **{"id": id})
    if service_category is None:
        raise HTTPException(status_code=409, detail="Service category not found")
    return service_category.to_dict()

# Update a service category
@service_router.put("/service_category/{id}", response_model=dict)
async def update_service_category(id: str, category_data: ServiceCategoryUpdate, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    if user.to_dict()["is_admin"] != False:
        raise HTTPException(status_code=403, detail="Unauthorized")

    service_category = storage.find_by(ServiceCategory, **{"id": id})
    if service_category is None:
        raise HTTPException(status_code=409, detail="Service category not found")

    try:
        category_data_dict = category_data.dict()
        storage.update(service_category, **category_data_dict)
        storage.save()
        return {"message": "Service category updated successfully", "service_category": service_category.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete a service category
@service_router.delete("/service_category/{id}", response_model=dict)
async def delete_service_category(id: str, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    if user.to_dict()["is_admin"] != False:
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    service_category = storage.find_by(ServiceCategory, **{"id": id})
    if service_category is None:
        raise HTTPException(status_code=404, detail="Service category not found")
    storage.delete(service_category)
    return {"message": "Service category deleted successfully"}



# Create a service
@service_router.post("/services/", response_model=dict)
async def create_service(service_data: ServiceCreate, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")
        

    if storage.find_by(ServiceCategory, **{"id": service_data.service_category_id}) is None:
        raise HTTPException(status_code=401, detail="Invalid Service Category")

    try:
        service_data_dict = service_data.dict()
        service_data_dict["user_id"] =   user.to_dict()["id"]
        service_data_dict["is_verified"] = False
        service = Service(**service_data_dict)
        storage.new(service)
        storage.save()
        service = None
        return {"message": "New Service created succesfully", "service":service_data_dict}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get a list all services
@service_router.get("/services/", response_model=list)
async def get_services():
    services = storage.all(Service).values()
    packages = storage.all(PricePackage).values()
    services_list = []
    for obj in services:
        user = storage.find_by(User, **{"id": obj.user_id})

        related_packages = []
        for package in packages:
            if package.service_id == obj.id:
                related_packages.append({
                    "id": package.id,
                    "name": package.name,
                    "description": package.description,
                    "duration": package.duration,
                    "price": package.price
                })

        service = {
            "id": obj.id,
            "name": obj.name,
            "user_id": obj.user_id,
            "user_name": user.username,
            "service_category_id":  obj.service_category_id,
            "sub_category": obj.sub_category,
            "locations": obj.locations,
            "image_paths": obj.image_paths,
            "video_paths": obj.video_paths,
            "banner_paths": obj.banner_paths,
            "no_of_ratings": obj.no_of_ratings,
            "average_rating": obj.average_rating,
            "is_verified": obj.is_verified,
            "price_packages": related_packages
        }
        services_list.append(service)

    return services_list

# Get a service by user
@service_router.get("/services/{id}", response_model=dict)
async def get_service(id: str):
    service = storage.find_by(Service, **{"id": id})

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service_dict = service.to_dict()
    packages = storage.all(PricePackage).values()
    related_packages = []

    for package in packages:
        if package.service_id == service_dict["id"]:
            related_packages.append({
                "id": package.id,
                "name": package.name,
                "description": package.description,
                "duration": package.duration,
                "price": package.price
            })
    service_dict["price_packages"] = related_packages
    return service_dict

# Get a services by user id
@service_router.get("/services/user/{id}", response_model=list)
async def get_user_services(id: str):
    user = storage.find_by(User, **{"id": id})
    services_list = []
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        services = storage.all(Service).values()
        for service in services:
            if service.user_id == id:
                services_list.append(service.to_dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return services_list

# Update a service
@service_router.put("/services/{id}", response_model=dict)
async def update_service(id: str, service_data: ServiceUpdate, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    service = storage.find_by(Service, **{"id": id})
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        service_data_dict = service_data.dict()
        if storage.find_by(ServiceCategory, **{"id": service_data_dict['service_category_id']}) is None:
            raise HTTPException(status_code=409, detail="Invalid Service Category")

        storage.update(service, **service_data_dict)
        storage.save()
        service = storage.find_by(Service, **{"id": id})
        return {"message": "Service updated successfully", "service": service.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete a service
@service_router.delete("/services/{id}", response_model=dict)
async def delete_service(id: str, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    service = storage.find_by(Service, **{"id": id})
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if service.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    storage.delete(service)
    storage.save()
    return {"message": "Service deleted successfully"}

# Create a service price package
@service_router.post("/service_price_package", response_model=dict)
async def create_service_price_package(package_data: PricePackageCreate, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    package_data_dict = package_data.dict()

    service = storage.find_by(Service, **{"id": package_data_dict['service_id']})
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if service.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        package_data_dict["service_id"] = service_id
        price_package = PricePackage(**package_data_dict)
        storage.new(price_package)
        storage.save()
        price_package = None
        return {"message": "Service price package created successfully", "price_package": price_package.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get all service price packages
@service_router.get("/service_price_package", response_model=list)
async def get_service_price_packages():
    price_packages = storage.all(PricePackage).values()
    packages = []
    for package in price_packages:
        package_data = {
            "id": package.id,
            "service_id": package.service_id,
            "name": package.name,
            "description": package.description,
            "price": package.price,
            "duration": package.duration
        }
        packages.append(package_data)
    
    return packages

# Get a service price package by id
@service_router.get("/service_price_package/{id}", response_model=dict)
async def get_service_price_package(id: str):
    price_package = storage.find_by(PricePackage, **{"id": id})
    if price_package is None:
        raise HTTPException(status_code=404, detail="Service price package not found")
    return price_package.to_dict()

# Update a service price package
@service_router.put("/service_price_package/{id}", response_model=dict)
async def update_service_price_package(id: str, package_data: PricePackageUpdate):
    price_package = storage.find_by(PricePackage, **{"id": id})
    if price_package is None:
        raise HTTPException(status_code=404, detail="Service price package not found")
    
    try:
        package_data_dict = package_data.dict()
        storage.update(price_package, **package_data_dict)
        storage.save()
        return {"message": "Service price package updated successfully", "price_package": price_package.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Delete a service price package
@service_router.delete("/service_price_package/{id}", response_model=dict)
async def delete_service_price_package(id: str):
    price_package = storage.find_by(PricePackage, **{"id": id})
    if price_package is None:
        raise HTTPException(status_code=404, detail="Service price package not found")
    storage.delete(price_package)
    storage.save()
    return {"message": "Service price package deleted successfully"}
