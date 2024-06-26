from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.customer import Customer
from models.product import Product
from models.order import Order


def save(order_data):
    with Session(db.engine) as session:
        with session.begin():
            product_ids = [prod['id'] for prod in order_data['products']]
            product_query = select(Product).where(Product.id.in_(product_ids))
            products = session.execute(product_query).scalars().all()

            if len(product_ids) != len(products):
                raise ValueError("One or more products do not exist")
            
            customer_id = order_data['customer_id']
            customer = session.get(Customer, customer_id)

            if not customer:
                raise ValueError(f"Customer with ID {customer_id} does not exist")

            new_order = Order(customer_id=order_data['customer_id'], products=products)
            session.add(new_order)
            session.commit()

        session.refresh(new_order)

        for product in new_order.products:
            session.refresh(product)

        return new_order


def find_all():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()
    return orders