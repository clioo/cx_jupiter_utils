from db.schemas.landing.tables import (
    SubGroupTbl, GroupTbl, CountryCat, Project, ProjectPermission, CountryPermission, GroupPermission, SubGroupPermission, UserTbl, PermissionView
)
from sqlalchemy.orm import Session
from lib.constants import AvailablePermissions
from lib.exceptions import UserNotFoundException, NoGeographicalScopeException
from sqlalchemy import and_
from typing import Type


def _is_user_granted_for_permission_level_by_geographical_codes(
        permission_level: AvailablePermissions,
        permission_entry: PermissionView,
        country_code: str|None = None,
        group_code: str|None = None,
        subgroup_code: str = None
) -> AvailablePermissions|None:
    if not any([country_code, group_code, subgroup_code]):
        raise NoGeographicalScopeException("At least one of country_code, group_code or subgroup_code must be provided.")
    if country_code and permission_entry.CountryCode == country_code and permission_entry.CountryPermissionPermission == permission_level:
        return permission_level
    if group_code and permission_entry.GroupCode == group_code and permission_entry.GroupPermissionPermission == permission_level:
        return permission_level
    if subgroup_code and permission_entry.subgroupCode == subgroup_code and permission_entry.SubGroupPermissionPermission == permission_level:
        return permission_level
    return None



def get_project_by_name(db: Session, project_name: str) -> Project|None:
    return db.query(Project).filter(Project.ProjectName == project_name).first()


def get_country_by_country_code(db: Session, country_code: str) -> CountryCat|None:
    return db.query(CountryCat).filter(CountryCat.CountryCode == country_code).first()


def get_group_by_group_code(db: Session, group_code: str) -> GroupTbl|None:
    return db.query(GroupTbl).filter(GroupTbl.GroupCode == group_code).first()


def get_subgroup_by_subgroup_code(db: Session, subgroup_code: str) -> SubGroupTbl|None:
    return db.query(SubGroupTbl).filter(SubGroupTbl.SubGroupCode == subgroup_code).first()



def get_user_by_email(db: Session, email: str) -> UserTbl|None:
    return db.query(UserTbl).filter(UserTbl.Email == email).first()



def get_project_permission_by_user_id_and_project_id(db: Session, user_id: int, project_id: int) -> ProjectPermission|None:
    return db.query(ProjectPermission).filter(ProjectPermission.user_id == user_id, ProjectPermission.project_id == project_id).first()


def get_permission_from_view_by_user_id_and_project_name(db: Session, user_id: int, project_name: str) -> PermissionView|None:
    return db.query(PermissionView).filter(and_(PermissionView.UserId == user_id, PermissionView.ProjectName == project_name)).first()



def get_permission_level_by_user_email(
        db: Session,
        user_email: str,
        project_name: str|None = None,
        country_code: str|None = None,
        group_code: str|None = None,
        subgroup_code: str|None = None
) -> AvailablePermissions|None:
    user = get_user_by_email(db=db, email=user_email)
    if not user:
        raise UserNotFoundException(f'User with email {user_email} not found')
    

    if user.IsSuperUser:
        return AvailablePermissions.ADMIN
    
    permission_entry  = get_permission_from_view_by_user_id_and_project_name(db=db, user_id=user.UserId, project_name=project_name)
    if not permission_entry:
        # Means no permission found for that project
        return None

    # If user has ADMIN project permissions, return ADMIN
    if permission_entry.ProjectPermissionPermission == AvailablePermissions.ADMIN:
        return AvailablePermissions.ADMIN
    
    if not any([country_code, group_code, subgroup_code]):
        return None
    
    for permission in [AvailablePermissions.READ_WRITE, AvailablePermissions.READ]:
        is_granted = _is_user_granted_for_permission_level_by_geographical_codes(
            permission_level=AvailablePermissions.READ_WRITE,
            permission_entry=permission_entry,
            country_code=country_code,
            group_code=group_code,
            subgroup_code=subgroup_code
        )
        if is_granted:
            return permission
        
    return None



