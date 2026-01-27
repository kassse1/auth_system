from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.db import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class BusinessElement(Base):
    __tablename__ = "business_elements"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class AccessRoleRule(Base):
    __tablename__ = "access_role_rules"
    id = Column(Integer, primary_key=True)

    role_id = Column(Integer, ForeignKey("roles.id"))
    element_id = Column(Integer, ForeignKey("business_elements.id"))

    read_permission = Column(Boolean, default=False)
    read_all_permission = Column(Boolean, default=False)
    create_permission = Column(Boolean, default=False)
    update_permission = Column(Boolean, default=False)
    update_all_permission = Column(Boolean, default=False)
    delete_permission = Column(Boolean, default=False)
    delete_all_permission = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Boolean, default=True)

    role = relationship("Role")
