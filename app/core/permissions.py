from sqlalchemy.orm import Session
from app.database.models import BusinessElement, AccessRoleRule


def check_permission(
    db: Session,
    role_id: int,
    element_name: str,
    action: str,
) -> bool:
    """
    Проверяет, имеет ли роль право на действие над бизнес-объектом
    action: read | create | update | delete
    """

    element = (
        db.query(BusinessElement)
        .filter(BusinessElement.name == element_name)
        .first()
    )

    if not element:
        return False

    rule = (
        db.query(AccessRoleRule)
        .filter(
            AccessRoleRule.role_id == role_id,
            AccessRoleRule.element_id == element.id,
        )
        .first()
    )

    if not rule:
        return False

    if action == "read":
        return rule.read_permission
    if action == "create":
        return rule.create_permission
    if action == "update":
        return rule.update_permission
    if action == "delete":
        return rule.delete_permission

    return False
