from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index, Boolean, CHAR
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from db.schemas.landing.enums import PermissionTypes

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    UserId = Column(Integer, primary_key=True)
    Email = Column(String(255), unique=True)
    Role = Column(String)
    IsSuperUser = Column(Boolean, default=False)  # New column to identify if user is a superuser
    DateCreate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)
    DateUpdate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)


class GroupTbl(Base):
    __tablename__ = 'GroupTbl'

    GroupId = Column(Integer, primary_key=True, autoincrement=False)
    GroupCode = Column(String(4))
    GroupDesc = Column(String(100))
    CountryId = Column(Integer, ForeignKey('CountryCat.CountryId'))
    DateCreate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)
    DateUpdate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)


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
    DateCreate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)
    DateUpdate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)


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
    ProjectName = Column(String)
    DateCreate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)
    DateUpdate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)


class ProjectPermission(Base):
    __tablename__ = 'ProjectPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.UserId'))
    project_id = Column(Integer, ForeignKey('Project.ProjectId'))
    permission = Column(PermissionTypes)

class CountryPermission(Base):
    __tablename__ = 'CountryPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.UserId'))
    country_id = Column(Integer, ForeignKey('CountryCat.CountryId'))
    permission = Column(PermissionTypes)

class GroupPermission(Base):
    __tablename__ = 'GroupPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.UserId'))
    group_id = Column(Integer, ForeignKey('GroupTbl.GroupId'))
    country_id = Column(Integer, ForeignKey('CountryCat.CountryId'))  # New column
    project_id = Column(Integer, ForeignKey('Project.ProjectId'))  # New column
    permission = Column(PermissionTypes)

class SubGroupPermission(Base):
    __tablename__ = 'SubGroupPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.UserId'))
    subgroup_id = Column(Integer, ForeignKey('SubGroupTbl.SubGroupId'))
    group_id = Column(Integer, ForeignKey('GroupTbl.GroupId'))  # New column
    country_id = Column(Integer, ForeignKey('CountryCat.CountryId'))  # New column
    project_id = Column(Integer, ForeignKey('Project.ProjectId'))  # New column
    permission = Column(PermissionTypes)
