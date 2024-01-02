import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
import models
import schemas
import crud
from database import SessionLocal, engine

if not os.path.exists('.\mysqldb'):
    os.makedirs('.\mysqldb')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    owner = auth.authenticate_owner(db, form_data.username, form_data.password)
    if not owner:
        raise HTTPException(
            status_code=401,
            detail="Incorrect name or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token= auth.create_access_token(
        data={"sub": owner.name}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/restaurant/", response_model=schemas.Restaurant)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    return crud.create_restaurant(db=db, restaurant=restaurant)

@app.put("/restaurant/{restaurant_id}", response_model=schemas.Restaurant)
def update_restaurant(restaurant_id: int, address: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    update = crud.update_restaurant(db=db, restaurant_id=restaurant_id, address=address)
    return update

@app.get("/restaurants/", response_model=list[schemas.Restaurant])
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    restaurants = crud.get_restaurants(db, skip, limit)
    return restaurants

@app.get("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
def read_restaurants(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = crud.get_restaurant(db, restaurant_id=restaurant_id)

    if db_restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return db_restaurant

@app.post("/owner/", response_model=schemas.Owner)
def create_owner(owner: schemas.OwnerCreate, db: Session = Depends(get_db)):
    return crud.create_owner(db=db, owner=owner)

@app.get("/owners/", response_model=list[schemas.Owner])
def read_owners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    owners = crud.get_owners(db, skip, limit)

    return owners

@app.post("/menuitem/", response_model=schemas.MenuItem)
def create_menu_item(menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    return crud.create_menu_item(db=db, menu_item=menu_item)

@app.get("/menuitems/{restaurant_id}", response_model=list[schemas.MenuItem])
def read_menu_items(restaurant_id: int, db: Session = Depends(get_db)):
    menu_items = crud.get_menu_items(db, restaurant_id)

    if not menu_items:
        raise HTTPException(status_code=404, detail="Restaurant not found or no items on menu")

    return menu_items

@app.delete("/restaurants/{restaurant_id}/menuitems/{menu_item_id}", response_model=schemas.MenuItem)
def delete_menu_item(restaurant_id: int, menu_item_id: int, db: Session = Depends(get_db)):
    deleted_menu_item = crud.delete_menu_item(db, restaurant_id, menu_item_id)

    if deleted_menu_item is None:
        raise HTTPException(status_code=404, detail="Restaurant or menu not found")

    return deleted_menu_item