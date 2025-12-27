from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional


class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement= True)
    message: Mapped[str] = mapped_column(nullable=False)
    like_count: Mapped[int] = mapped_column(default=0, nullable=False)
    board_id: Mapped[int] = mapped_column(ForeignKey("board.board_id"), nullable=False)
    board: Mapped["Board"] = relationship(back_populates="cards")


    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }
    

    @classmethod
    def from_dict(cls, dict):
        return cls(
            message=dict["message"],
            likes_count=dict["likes_count", 0],
            board_id=dict["board_id"]
        )