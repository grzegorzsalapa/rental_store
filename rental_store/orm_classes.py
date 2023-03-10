from datetime import date
from uuid import UUID
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from rental_store.data_models import FilmType


class Base(DeclarativeBase):
    pass


class Film(Base):
    __tablename__ = "film_inventory"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    type: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Film(id={self.id!r}, title={self.title!r}, type={self.type!r})"


class Cassette(Base):
    __tablename__ = "cassette_inventory"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    film_id: Mapped[UUID] = mapped_column(ForeignKey("film_inventory.id"))
    available_flag: Mapped[bool] = mapped_column()

    def __repr__(self) -> str:
        return f"Cassette(id={self.id!r}, film_id={self.film_id!r}, available={self.available_flag})"


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r})"


class RentalRecord(Base):
    __tablename__ = "rentals"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    customer_id: Mapped["Customer"] = mapped_column(ForeignKey("customers.id"))
    cassette_id: Mapped[UUID] = mapped_column(ForeignKey("cassette_inventory.id"), primary_key=True)
    date_of_rent: Mapped[date] = mapped_column()
    up_front_days: Mapped[int] = mapped_column()
    charge: Mapped[int] = mapped_column()
    date_of_return: Mapped[Optional[date]] = mapped_column()
    surcharge: Mapped[Optional[int]] = mapped_column()

    def __repr__(self) -> str:
        return f"Rental record(id={self.id!r}, customer_id={self.customer_id!r}, cassette_id={self.cassette_id!r})"
