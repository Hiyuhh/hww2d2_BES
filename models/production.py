from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class Production(Base):
    __tablename__ = "production"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(db.ForeignKey('products.id'), nullable=False)
    quantity_produced: Mapped[int] = mapped_column(nullable=False)
    date_produced: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
