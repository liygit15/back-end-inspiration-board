from flask import Blueprint,request,Response
from ..models.card import Card
from ..db import db
from .route_utilities import validate_model


bp = Blueprint("card_bp", __name__, url_prefix="/cards")

@bp.delete("/<card_id>")
def delete_card(card_id):
    card =validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return Response(status=204, mimetype="application/json")