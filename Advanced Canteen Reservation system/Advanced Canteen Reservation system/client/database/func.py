
from database import db_x
import secrets
import string

filter = db_x["FC"]
filter_product = db_x["RECIPE"]
def add(dic, pwd,is_parcel):
    filter.insert_one(
            {"dict": dic, "key": pwd, "isvalid":True, "is_parcel":is_parcel}
        )

def list_recipes():
    cursor = filter_product.find({})
    return cursor

def key_info(key):
    lol = filter.find_one({"key":key})
    if not lol.get("isvalid"):
        return False
    else:
        return lol

def update_recipe_stock(receipe_dict):
    print(receipe_dict)
    for x in receipe_dict:
        print(x)
        print(receipe_dict.get(x))
        filtere = { "recipe": x }
        newvalues = { "$set": { "stock": str(receipe_dict.get(x)) } }
        filter_product.update_one(filtere,newvalues)


def make_reservation(lst, is_parcel):
    # Generate a unique key for the reservation
    key = passgen()

    reservation_doc = {
        "dict": lst, 
        "key": key, 
        "isvalid": True, 
        "is_parcel": is_parcel
    }

    filter.insert_one(reservation_doc) 
    return key


def cancel_reservation(key):
   
    reservation = filter.find_one({"key": key, "isvalid": True})
    if reservation:
        filter.update_one({"key": key}, {"$set": {"isvalid": False}})
        return True  # Indicate that the cancellation was successful
    return False  # Indicate that the reservation was not found or was already invalid



def passgen():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(60))
    password = password.replace("'", '"')
    return password.replace('"',"*")