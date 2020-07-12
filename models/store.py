from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') # it Allow the store table to see items table and we use lazy= 'dynamic' To prevent it from creating a file for each item that has a stored id. It will take up space

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "items": [item.json() for item in self.items.all()],#Because i use lazy= 'dynamic' i can use self.items as a query but it will go to table every time and it will be slowe
            }

    @classmethod
    def find_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name = name LIMIT 1

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()