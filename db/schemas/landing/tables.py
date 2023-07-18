from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index, Boolean, CHAR, MetaData, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from db.schemas.landing.enums import PermissionTypes


Base = declarative_base()
metadata = MetaData()


class GroupTbl(Base):
    __tablename__ = 'GroupTbl'

    GroupId = Column(Integer, primary_key=True, autoincrement=False)
    GroupCode = Column(String(4))
    GroupDesc = Column(String(100))
    CountryId = Column(Integer, ForeignKey('CountryCat.CountryId'))
    DateCreate = Column(DateTime, server_default=func.now(), nullable=False)
    DateUpdate = Column(DateTime, server_default=func.now(), nullable=False)


class SubGroupTbl(Base):
    __tablename__ = 'SubGroupTbl'
    __table_args__ = (
        UniqueConstraint('GroupId', 'SubGroupCode', name='UQ_Subgroup'),
        Index('IX_SubGroupTbl_SubGroupCode', 'SubGroupCode', 'SubGroupId'),
    )

    SubGroupId = Column(Integer, primary_key=True, autoincrement=False)
    GroupId = Column(Integer, ForeignKey('GroupTbl.GroupId'))
    SubGroupCode = Column(String(4))
    SubGroupDesc = Column(String(100))
    DateCreate = Column(DateTime, server_default=func.now(), nullable=False)
    DateUpdate = Column(DateTime, server_default=func.now(), nullable=False)


class CountryCat(Base):
    __tablename__ = 'CountryCat'
    __table_args__ = (
        UniqueConstraint('CountryCode', name='UQ_CountryCode'),
    )

    CountryId = Column(Integer, primary_key=True, autoincrement=False)
    CountryCode = Column(CHAR(2), nullable=False)
    CountryDesc = Column(String(50))


class Project(Base):
    __tablename__ = 'Project'

    ProjectId = Column(Integer, primary_key=True)
    ProjectName = Column(String, unique=True)
    DateCreate = Column(DateTime, server_default=func.now(), nullable=False)
    DateUpdate = Column(DateTime, server_default=func.now(), nullable=False)


class CountryPermission(Base):
    """
    Someone with CountryPermissions will have permissions for all groups and subgroups of the specific country,
    project permissions will be needed if user is not an admin UserTbl
    """
    __tablename__ = 'CountryPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('UserTbl.UserId'))
    country_id = Column(Integer, ForeignKey('CountryCat.CountryId'))
    permission = Column(PermissionTypes)


class ProjectPermission(Base):
    """
    Anyone with project permission will have permissions for that specific project,
    group permissions will be needed user is not an admin UserTbl
    """
    __tablename__ = 'ProjectPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('UserTbl.UserId'))
    project_id = Column(Integer, ForeignKey('Project.ProjectId'))
    permission = Column(PermissionTypes)


class GroupPermission(Base):
    """Someone with GroupPermissions will have permissions for all subgroups, project permissions will be needed if user is not an admin UserTbl"""
    __tablename__ = 'GroupPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('UserTbl.UserId'))
    group_id = Column(Integer, ForeignKey('GroupTbl.GroupId'))
    country_id = Column(Integer, ForeignKey('CountryCat.CountryId'))  # New column
    project_id = Column(Integer, ForeignKey('Project.ProjectId'))  # New column
    permission = Column(PermissionTypes)

class SubGroupPermission(Base):
    """Someone with SubGroupPermissions will have permissions for all projects of the specific subgroup, project permissions will be needed if user is not an admin UserTbl"""
    __tablename__ = 'SubGroupPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('UserTbl.UserId'))
    subgroup_id = Column(Integer, ForeignKey('SubGroupTbl.SubGroupId'))
    group_id = Column(Integer, ForeignKey('GroupTbl.GroupId'))  # New column
    country_id = Column(Integer, ForeignKey('CountryCat.CountryId'))  # New column
    project_id = Column(Integer, ForeignKey('Project.ProjectId'))  # New column
    permission = Column(PermissionTypes)


class UserTbl(Base):
    __tablename__ = 'UserTbl'

    UserId = Column(Integer, primary_key=True)
    Email = Column(String(255), unique=True)
    IsSuperUser = Column(Boolean, default=False)  # New column to identify if user is a superuser
    DateCreate = Column(DateTime, server_default=func.now(), nullable=False)
    DateUpdate = Column(DateTime, server_default=func.now(), nullable=False)

class PermissionView(Base):
    __tablename__ = 'PermissionView'

    UserId = Column(Integer, primary_key=True)
    Email = Column(String(255))
    IsSuperUser = Column(Boolean)
    ProjectPermissionProjectId = Column(Integer)
    ProjectPermissionPermission = Column(PermissionTypes)
    CountryPermissionCountryId = Column(Integer)
    CountryPermissionPermission = Column(PermissionTypes)
    GroupPermissionGroupId = Column(Integer)
    GroupPermissionProjectId = Column(Integer)
    GroupPermissionPermission = Column(PermissionTypes)
    SubGroupPermissionSubgroupId = Column(Integer)
    SubGroupPermissionGroupId = Column(Integer)
    SubGroupPermissionProjectId = Column(Integer)
    SubGroupPermissionPermission = Column(PermissionTypes)
    subgroupCode = Column(String(4))
    CountryCode = Column(String(2))
    GroupCode = Column(String(4))
    ProjectName = Column(String)
