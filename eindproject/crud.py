from sqlalchemy.orm import Session

import auth
import models
import schemas


def get_restaurant(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurant).offset(skip).limit(limit).all()

def create_restaurant(db: Session, restaurant:schemas.RestaurantCreate):
    db_restaurant = models.Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def update_restaurant(db: Session, restaurant_id: int, address: str):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()

    if db_restaurant:
        db_restaurant.address = address
        db.commit()
        db.refresh(db_restaurant)
        return db_restaurant

    return None

def get_owners(db: Session, skip:int = 0, limit: int = 100):
    return db.query(models.Owner).offset(skip).limit(limit).all()

def get_owner_by_name(db: Session, name: str):
    return db.query(models.Owner).filter(models.Owner.name == name).first()

def create_owner(db: Session, owner:schemas.OwnerCreate):
    hashed_password = auth.get_password_hash(owner.password)
    db_owner = models.Owner(name=owner.name, hashed_password=hashed_password, telephone=owner.telephone, restaurant_id=owner.restaurant_id)
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

def get_menu_items(db: Session, restaurant_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.restaurant_id == restaurant_id).all()

def create_menu_item(db: Session, menu_item: schemas.MenuItemCreate):
    db_menu_item = models.MenuItem(**menu_item.dict())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

def delete_menu_item(db: Session, restaurant_id: int, menu_item_id: int):
    db_menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == menu_item_id, models.MenuItem.restaurant_id == restaurant_id).first()
    if db_menu_item:
        db.delete(db_menu_item)
        db.commit()
        return db_menu_item
    return None