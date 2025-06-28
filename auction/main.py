from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb://auction_mongo:27017")

db = client["auction_db"]
auctions = db["auctions"]

class AuctionCreate(BaseModel):
    title: str
    description: str
    starting_price: float
    ends_at: str
    owner_id: str



@app.post("/create")
def create_auction(auction: AuctionCreate):
    auction_dict = auction.dict()
    auction_dict.update({
        "current_price": auction.starting_price,
        "status": "pending",
        "created_at": datetime.utcnow()
    })
    result = auctions.insert_one(auction_dict)
    return {"message": "Enchère créée", "auction_id": str(result.inserted_id)}

@app.get("/list/{owner_id}")
def list_user_auctions(owner_id: str):
    return [dict(auction, _id=str(auction["_id"])) for auction in auctions.find({"owner_id": owner_id})]

@app.delete("/delete/{auction_id}")
def delete_auction(auction_id: str):
    result = auctions.delete_one({"_id": ObjectId(auction_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Enchère non trouvée")
    return {"message": "Enchère supprimée"}

@app.get("/auctions")
def list_all_auctions():
    return [dict(auction, _id=str(auction["_id"])) for auction in auctions.find()]
