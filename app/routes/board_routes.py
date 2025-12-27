from flask import Blueprint,request,Response,abort, make_response
from ..models.board import Board
from ..models.card import Card
from .route_utilities import validate_model, create_model
from ..db import db

bp = Blueprint("board_bp",__name__,url_prefix="/boards")

@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)


@bp.get("")
def get_all_boards():
    query = db.select(Board)
    boards = db.session.scalars(query)
    boards_list = [board.to_dict() for board in boards]
    return {"boards": boards_list}, 200



@bp.get("/<board_id>")
def get_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict(), 200
    

@bp.get("/<board_id>/cards")
def get_cards_on_board(board_id):
    board = validate_model(Board, board_id)
    cards = board.cards
    cards_list = [card.to_dict() for card in cards]

    return {"cards": cards_list}, 200


@bp.put("/<board_id>")
def replace_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    board.title = request_body["title"]
    board.owner = request_body["owner"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<board_id>/cards")
def create_card_on_board(board_id):
    board = validate_model(Board, board_id)
    data = request.get_json()
    return create_model(Card, {**data, "board_id": board_id})

    # solution1
    # card = Card.from_dict(data)
    # card.board_id = board.board_id

    # db.session.add(card)
    # db.session.commit()
    # return card.to_dict(), 201 
    # solution2:
    # card =create_model(Card, data)
    # card.board_id = board.board_id

    # db.session.commit()

    # return card.to_dict(), 201
        
@bp.put("/<board_id>/cards/<card_id>")
def edit_card_on_board(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)
    if card.board_id != board.board_id:
        abort(make_response(
            {"details": "card does not belong to this board"}, 404
        ))
    data = request.get_json()

    if "message" in data:
        card.message = data["message"]
    if "likes_count" in data:
        card.likes_count = data["likes_count"]
    
    db.session.commit()
    
    return card.to_dict(), 200


@bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
