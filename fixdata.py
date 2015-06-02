import pprint

__author__ = 'ronanbrady2'

# Connects to 'udwrangle' DB and returns DB object
def connectDB() :
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.udwrangle
    return db

if __name__ == "__main__":
    db = connectDB()

    mapping = { "Ave": "Avenue",
            "Avevnue": "Avenue",
            "Cente": "Centre",
            "Center": "Centre",
            "Center": "Centre",
            "Donghmede": "Donaghmede",
            "Nouth": "North",
            "Roafd": "Road",
            "Sreet": "Street",
            "St": "Street",
            "street": "Street",
            "heights": "Heights",
            "lane": "Lane",
            "park": "Park",
            "place": "Place",
            "road": "Road"
            }



    correctedcount = 0
    for misspelling, correction in mapping.items():
        pprint.pprint(misspelling)
        regex = "\w " + misspelling + "$"
        results = db.openmap.find({"address.street" : { "$regex" : regex}})
        for obj in results:
            street = obj["address"]["street"]
            print(street)

            correctedstreet = street.replace(misspelling, correction)
            obj["address"]["street"] = correctedstreet
            print(correctedstreet)
            correctedcount += 1
            db.openmap.save(obj)
    print("total corrected: {0}".format(correctedcount))
