from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Integer, Text, Float, ForeignKey
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"

# Base class inherits from DeclarativeBase for models set-up
class Base(DeclarativeBase):
    pass

# SQLAlchemy instantiated as db object
db = SQLAlchemy(model_class = Base)
db.init_app(app)

class Customers(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    phone: Mapped[str] = mapped_column(String(80), nullable=False)

    service_tickets: Mapped[list['ServiceTickets']] = relationship('ServiceTickets', back_populates='customer')

class ServiceTickets(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(String(17), nullable=False, unique=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    service_desc: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    customer: Mapped['Customers'] = relationship('Customers', back_populates='service_tickets')
    mechanics: Mapped[list['Mechanics']] = relationship('Mechanics', secondary='mechanics_service_tickets', back_populates='service_tickets')

class MechanicsServiceTickets(Base):
    __tablename__ = "mechanics_service_tickets"

    ticket_id: Mapped[int] = mapped_column(ForeignKey("service_tickets.id"), primary_key=True)
    mechanics_id: Mapped[int] = mapped_column(ForeignKey("mechanics.id"), primary_key=True)


class Mechanics(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    schedule: Mapped[str] = mapped_column(String(100), nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=True)

    service_tickets: Mapped[list['ServiceTickets']] = relationship('ServiceTickets', secondary='mechanics_service_tickets', back_populates='mechanics')


def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("All tables created successfully.")
        customer = Customers(
            first_name="John",
            last_name="Doe",
            email="john@doe.com",
            password="password123",
            phone="123-456-7890")
        
        mechanic = Mechanics(
            first_name="Jane",
            last_name="Smith",
            email="Jane@smith.com",
            address="123 Main St",
            schedule="Mon-Fri 9am-5pm",
            salary=60000)
        
        ticket = ServiceTickets(
            vin="12345678901234567",
            customer=customer,
            service_desc="Oil change and tire rotation",
            price=89.99)
        ticket.mechanics.append(mechanic)
        
        db.session.add_all([customer, mechanic, ticket])
        db.session.commit()
        print("Seed data added successfully.")
        print(f"Ticket {ticket.id} assigned to {ticket.mechanics[0].first_name}")

if __name__ == "__main__":
    seed()
