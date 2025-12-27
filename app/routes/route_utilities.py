from flask import abort, make_response
# from sqlalchemy import asc, desc   # need this 1
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        invalid = {"Message": f"{cls.__name__} id {model_id} is invalid."}
        abort(make_response(invalid, 400))
    
    # primary_key_column = inspect(cls).primary_key[0]  
    # query = db.select(cls).where(primary_key_column == model_id) # need to fix this 2
    # model = db.session.scalar(query)
    model = db.session.get(cls, model_id)

    if not model:
        not_found = {"Message": f"{cls.__name__} with id {model_id} is not found."}
        abort(make_response(not_found, 404))
    
    return model
    

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        invalid = {"details": "Invalid data"}
        abort(make_response(invalid, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201


# def get_model_with_filters(cls, filters=None, sort=None):
#     query = db.select(cls)

#     if filters:
#         for attribute, value in filters.items():
#             if hasattr(cls, attribute):
#                 query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
#     if sort == "asc":
#         query = query.order_by(asc(cls.title))  # here is title?
#     elif sort == "desc": 
#         query = query.order_by(desc(cls.title))
#     else:
#         query = query.order_by(cls.id) # not id?
    
#     models = db.session.scalars(query)
#     models_response = [model.to_dict() for model in models]
#     return models_response

