from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = FastAPI()
client = MongoClient("mongodb://mongo:21020")
db = client["auction_db"]
bids = db["bids"]
auctions = db["auctions"]

class BidCreate(BaseModel):
    user_id: str
    auction_id: str
    amount: float

@app.post("/place")
def place_bid(bid: BidCreate):
    auction = auctions.find_one({"_id": ObjectId(bid.auction_id)})
    if not auction:
        raise HTTPException(status_code=404, detail="Enchère introuvable")
    if bid.amount <= auction["current_price"]:
        raise HTTPException(status_code=400, detail="Montant trop bas")
    bids.insert_one(bid.dict() | {"timestamp": datetime.utcnow()})
    auctions.update_one(
        {"_id": ObjectId(bid.auction_id)},
        {"$set": {"current_price": bid.amount}}
    )
    return {"message": "Enchère placée avec succès"}

@app.get("/bids/{auction_id}")
def list_bids(auction_id: str):
    return [dict(bid, _id=str(bid["_id"])) for bid in bids.find({"auction_id": auction_id})]
