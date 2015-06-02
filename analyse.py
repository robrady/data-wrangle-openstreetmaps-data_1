import pprint
import re
from collections import defaultdict

__author__ = 'ronanbrady2'

# Prints all street suffixes, e.g. Lane, Avenue, to allow audit analysis
def printAllStreetSuffixes(db):
    pipeline = [
                 { "$group" : {
                      "_id" : "$address.street" ,
                      "count" : { "$sum" : 1 } }},
        { "$sort" : { "_id" : 1 }}]

    result = db.openmap.aggregate(pipeline)

    valsfound = defaultdict(int)
    regx = re.compile("\s(\w+)$", re.IGNORECASE)
    for r in result:
        val = r['_id']


        if(not val is None):
            i = regx.finditer(val)
            for match in i:
                streettype = match.group(0).strip()
                valsfound[streettype] += 1
    pprint.pprint(valsfound)

# Prints all addresses with Postcode
def printAllWithPostcodes(db):
    result = db.openmap.find({"address.postcode" : { "$exists" : "true"} })
    pprint.pprint(result)

# Prints all addresses with County
def printAllWithCounty(db):
    result = db.openmap.find({ "address.county" : { "$exists" : "true" } }).count()
    pprint.pprint(result)

def printAllAmenities(db):
    result = db.openmap.find({ "amenity" : { "$exists" : "true" } }).count()
    pprint.pprint(result)

def capacityOfAllCarparks(db):
    pipeline = [ { "$match" : { "amenity" : "parking"} }]
    # turns out none of the car parks have capacity in the listing
     # { "$group" : { "_id" : None , "total_capacity" : {"$sum" : "capacity"}} } ]

    result = db.openmap.aggregate(pipeline)
    for r in result:
        pprint.pprint(r)

def pubsByContributor(db):
    pipeline = [ { "$match" : { "amenity" : "pub"} },
        { "$group" : { "_id" : "$created.user", "count" : { "$sum" : 1 }}},
        { "$sort" : { "count" : -1 }}]

    result = db.openmap.aggregate(pipeline)
    for r in result:
        pprint.pprint(r)

def pubsWithBeerGardens(db):
    pipeline = [ { "$match" : { "amenity" : "pub"} },
                 { "$match" : { "beer_garden" : "yes"} },
        { "$group" : { "_id" : None, "count" : { "$sum" : 1 }}}]

    result = db.openmap.aggregate(pipeline)
    for r in result:
        pprint.pprint(r)

def fastFoodByCuisine(db):
    pipeline = [ { "$match" : { "amenity" : "fast_food"} },
        { "$group" : { "_id" : "$cuisine", "count" : { "$sum" : 1 }}},
        { "$sort" : { "count" : -1 }}]

    result = db.openmap.aggregate(pipeline)
    for r in result:
        pprint.pprint(r)

def printTop10AppearingAmenities(db):
    pipeline = [{"$match": {"amenity": {"$exists": "true"}}},
                {"$group":{"_id":"$amenity", "count": {"$sum":1}}},
                {"$sort":{"count": -1}}, {"$limit":10}]
    result = db.openmap.aggregate(pipeline)
    for r in result:
        pprint.pprint(r)

# Connects to 'udwrangle' DB and returns DB object
def connectDB() :
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.udwrangle
    return db

if __name__ == "__main__":
    db = connectDB()
    #printAllStreetSuffixes(db)
    #printAllWithPostcodes(db)
    #printAllWithCounty(db)
    #printTop10AppearingAmenities(db)
    #printAllAmenities(db)
    #capacityOfAllCarparks(db)
    #pubsByContributor(db)
    #pubsWithBeerGardens(db)
    fastFoodByCuisine(db)


