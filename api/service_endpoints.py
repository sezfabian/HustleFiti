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

class ServiceCreate(BaseModel):
    name: str
    description: str
    user_id: str
    service_category_id: str
    sub_category: str =None
    image_paths: str = None
    video_paths: str = None
    banner_paths: str = None

#create service category
@service_router.post("/service_category", response_model=dict)
def create_service_category(category_data: ServiceCategoryCreate, session_id: str = Cookie(None)):
    try:
        category_data_dict = category_data.dict()
        if storage.find_by(ServiceCategory, **{"name": category_data_dict['name']}):
            raise HTTPException(status_code=409, detail="Service_Category already exists")
        new_category = ServiceCategory(**category_data.dict())
        storage.new(new_category)
        storage.save()
        return {"message": "Service_category created sucessfully", "service_category": new_category.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=409, detail="Category already exixts")

#Get list of service categories
@service_router.get("/service_category", response_model=list)
async def get_service_categories():
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


# Create a service
@service_router.post("/services/", response_model=dict)
async def create_service(service_data: ServiceCreate, session_id: str = Cookie(None)):
    if service_data.user_id is None:
        raise HTTPException(status_code=401, detail="Invalid User credentials")

    if storage.find_by(User, **{"id": service_data.user_id}) is None:
        raise HTTPException(status_code=401, detail="Invalid User credentials")

    if storage.find_by(ServiceCategory, **{"id": service_data.service_category_id}) is None:
        raise HTTPException(status_code=401, detail="Invalid Service Category")

    try:
        service_data_dict = service_data.dict()
        service_data_dict["is_verified"] = False
        service = Service(**service_data_dict)
        storage.new(service)
        storage.save()
        return {"message": "New Service created succesfully", "service":service_data_dict}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get all services
@service_router.get("/services/", response_model=list)
async def get_services():
    services = storage.all(Service).values()
    services_list = []
    for obj in services:
        service = {
            "id": obj.id,
            "name": obj.name,
            "user_id": obj.user_id,
            "service_category_id":  obj.service_category_id,
            "sub_category": obj.sub_category,
            "image_paths": obj.image_paths,
            "video_paths": obj.video_paths,
            "banner_paths": obj.banner_paths
        }
        services_list.append(service)

    return services_list