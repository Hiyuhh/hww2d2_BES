from sqlalchemy.orm import Session
from database import db
from models.customer import Customer

def save(customer_data):
    with Session(db.engine) as session:
        with session.begin():
            new_customer = Customer(name=customer_data['name'], email=customer_data['email'])
            session.add(new_customer)
            session.commit()
        session.refresh(new_customer)
        return new_customer
    
def find_all(page=1, per_page=10):
    query = db.select(Customer).offset((page-1) * per_page).limit(per_page)
    customers = db.session.execute(query).scalars().all()
    return customers