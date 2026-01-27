from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.db import get_db
from app.database.models import User, Role
from app.core.security import hash_password, verify_password, create_token
from app.api.deps import get_current_user
from app.core.permissions import check_permission

router = APIRouter()


# -------- REGISTER --------
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: dict, db: Session = Depends(get_db)):

    if data["password"] != data["password_confirm"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    existing_user = db.query(User).filter(User.email == data["email"]).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    role = db.query(Role).filter(Role.name == "user").first()
    if not role:
        role = Role(name="user")
        db.add(role)
        db.commit()
        db.refresh(role)

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        hashed_password=hash_password(data["password"]),
        role_id=role.id,
        is_active=True,
    )

    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")

    return {"status": "registered"}



# -------- LOGIN --------
@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data["email"]).first()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data["password"], user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.id)
    return {"token": token}


# -------- LOGOUT --------
@router.post("/logout")
def logout():
    return {"status": "logged out"}




# -------- REGISTER --------
@router.patch("/users/me")
def update_me(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if "first_name" in data:
        current_user.first_name = data["first_name"]

    if "last_name" in data:
        current_user.last_name = data["last_name"]

    db.commit()

    return {
        "status": "updated",
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }

@router.delete("/users/me")
def delete_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.is_active = False
    db.commit()

    return {
        "status": "account deactivated"
    }



# -------- PRODUCTS (MOCK BUSINESS OBJECT) --------
@router.get("/products")
def get_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not check_permission(
        db=db,
        role_id=current_user.role_id,
        element_name="products",
        action="read",
    ):
        raise HTTPException(status_code=403, detail="Forbidden")

    return [
        {"id": 1, "name": "Product A"},
        {"id": 2, "name": "Product B"},
    ]
