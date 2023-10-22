from fastapi import APIRouter, HTTPException, Depends, Cookie, Path
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict
from models import storage
from models.user import User
from models.service import ServiceCategory, Service, PricePackage
from models.contract import Contract
from models.reviews import ServiceReview, ClientReview

reviews_router = APIRouter()

class ClientReviewCreate(BaseModel):
    rating: float
    comment: str

class ServiceReviewCreate(BaseModel):
    rating: float
    comment: str

# Create a new client review
@reviews_router.post("/client_review/{contract_id}", response_model=dict, tags=["reviews"])
async def create_client_review(contract_id: str, client_review_data: ClientReviewCreate, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")
    
    contract = storage.find_by(Contract, **{"id": contract_id})
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    client = storage.find_by(User, **{"id": contract.user_id}).to_dict()
    
    service = storage.find_by(Service, **{"id": contract.service_id})
    
    if user.to_dict()["id"] != service.to_dict()["user_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        client_review_data_dict = client_review_data.dict()
        client_review_data_dict["user_id"] = contract.to_dict()["user_id"]
        client_review_data_dict["contract_id"] = contract_id

        review = ClientReview(**client_review_data_dict)

        # Update client rating
        new_rating = (client["no_of_ratings"] * client["average_rating"] + review.rating) / (client["no_of_ratings"] + 1)
        rating_count = client["no_of_ratings"] + 1
        update_dict = {"average_rating": new_rating, "no_of_ratings": rating_count}

        # Save client review
        storage.update(client, **update_dict)
        storage.new(review)
        storage.save()
        return {"message": "Client review created successfully", "client_review": client_review.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Delete a client review
@reviews_router.delete("/client_review/{review_id}", response_model=dict, tags=["reviews"])
async def delete_client_review(review_id: str, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")
    
    review = storage.find_by(ClientReview, **{"id": review_id})
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    if user.to_dict()["id"] != review.to_dict()["user_id"] or user.to_dict()["is_admin"] is False:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    try:
        storage.delete(review)
        storage.save()
        return {"message": "Review deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# get all reviews of a client
@reviews_router.get("/client_reviews/{user_id}", response_model=list, tags=["reviews"])
async def get_client_reviews(user_id: str, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")
    
    reviews = storage.all(ClientReview)
    return [review.to_dict() for review in reviews if review.to_dict()["user_id"] == user_id]


# Create a new service review
@reviews_router.post("/service_review/{contract_id}", response_model=dict, tags=["reviews"])
async def create_service_review(contract_id: str, service_review_data: ServiceReviewCreate, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    user = storage.find_by(User, **{"session_id": session_id})
    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")
    
    contract = storage.find_by(Contract, **{"id": contract_id})
    service = storage.find_by(Service, **{"id": contract.to_dict()["service_id"]}).to_dict()

    if contract is None or contract.to_dict()["user_id"] != user.to_dict()["id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    

    try:
        service_review_data_dict = service_review_data.dict()
        service_review_data_dict["user_id"] = user.to_dict()["id"]
        service_review_data_dict["contract_id"] = contract_id
        service_review = ServiceReview(**service_review_data_dict)
        storage.new(service_review)

        # update service rating
        new_rating = (service["no_of_ratings"] * service["average_rating"] + service_review.rating) / (service["no_of_ratings"] + 1)
        rating_count = service["no_of_ratings"] + 1
        update_dict = {"average_rating": new_rating, "no_of_ratings": rating_count}

        storage.update(service, **update_dict)
        storage.save()
        return {"message": "Service review created successfully", "service_review": service_review.to_dict()}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Delete a service review
@reviews_router.delete("/service_review/{review_id}", response_model=dict, tags=["reviews"])
async def delete_service_review(review_id: str, session_id: str = Cookie(None)):
    if session_id is None:
        raise HTTPException(status_code=403, detail="User not logged in")

    user = storage.find_by(User, **{"session_id": session_id})

    if user is None:
        raise HTTPException(status_code=403, detail="User session expired")

    review = storage.find_by(ServiceReview, **{"id": review_id})
    if review is None:
        raise HTTPException(status_code=404, detail="Service review not found")

    if user.to_dict()["id"] != review.to_dict()["user_id"] or user.to_dict()["is_admin"] is False:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        storage.delete(review)
        storage.save()
        return {"message": "Service review deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get all reviws of a service
@reviews_router.get("/service_reviews/{service_id}", response_model=list, tags=["reviews"])
async def get_service_reviews(service_id: str):
    try:
        reviews = storage.all(ServiceReview)
        reviews_list = [review.to_dict() for review in reviews if review.to_dict()["service_id"] == service_id]
        return reviews_list
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
