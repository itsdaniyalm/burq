from faker import Faker
from db import engine, SessionLocal, Base
from models import Contact, Deal, Activity, DealStatus
import random

fake = Faker()

ACTIVITY_TYPES = ["call", "email", "meeting", "note"]
DEAL_STATUSES = list(DealStatus)

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing
    db.query(Activity).delete()
    db.query(Deal).delete()
    db.query(Contact).delete()
    db.commit()

    for _ in range(40):
        contact = Contact(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            company=fake.company(),
            title=fake.job(),
            status=random.choice(DEAL_STATUSES),
        )
        db.add(contact)
        db.flush()

        # 1-3 deals per contact
        for _ in range(random.randint(1, 3)):
            deal = Deal(
                title=f"{fake.bs().title()} Deal",
                value=round(random.uniform(1000, 50000), 2),
                status=random.choice(DEAL_STATUSES),
                contact_id=contact.id
            )
            db.add(deal)
            db.flush()

            # 1-4 activities per deal
            for _ in range(random.randint(1, 4)):
                db.add(Activity(
                    type=random.choice(ACTIVITY_TYPES),
                    note=fake.sentence(),
                    contact_id=contact.id,
                    deal_id=deal.id
                ))

    db.commit()
    db.close()
    print("Seeded successfully.")

if __name__ == "__main__":
    seed()