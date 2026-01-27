from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import AccessRoleRule, BusinessElement
from app.api.deps import get_current_user


def check_permission(element: str, action: str):
    def checker(user=Depends(get_current_user), db: Session = Depends(get_db)):
        rule = (
            db.query(AccessRoleRule)
            .join(BusinessElement)
            .filter(
                BusinessElement.name == element,
                AccessRoleRule.role_id == user.role_id
            )
            .first()
        )

        if not rule or not getattr(rule, f"{action}_permission"):
            raise HTTPException(status_code=403)

        return user

    return checker
