from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    role = Column(String)
    created_at = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)
    updated_at = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    role = Column(String)
    created_at = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)
    updated_at = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)


class GroupPermission(Base):
    __tablename__ = 'GroupPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    group_id = Column(Integer, ForeignKey('GroupTbl.GroupId'))
    project_id = Column(Integer, ForeignKey('Project.id'))
    permission = Column(String)  # 'read', 'write', 'admin', etc.


class SubGroupPermission(Base):
    __tablename__ = 'SubGroupPermission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    subgroup_id = Column(Integer, ForeignKey('SubGroupTbl.SubGroupId'))
    project_id = Column(Integer, ForeignKey('Project.id'))
    permission = Column(String)  # 'read', 'write', 'admin', etc.


class GroupTbl(Base):
    __tablename__ = 'GroupTbl'
    __table_args__ = (
        UniqueConstraint('GroupCode', 'CountryId', name='UQ_Group'),
    )

    GroupId = Column(Integer, primary_key=True)
    GroupCode = Column(String(4))
    GroupDesc = Column(String(100))
    CountryId = Column(Integer, ForeignKey('CountryCat.CountryId'))
    ApplicationId = Column(Integer, ForeignKey('ApplicationCat.ApplicationId'))
    DateCreate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)
    DateUpdate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)


class SubGroupTbl(Base):
    __tablename__ = 'SubGroupTbl'
    __table_args__ = (
        UniqueConstraint('GroupId', 'SubGroupCode', name='UQ_Subgroup'),
        Index('IX_SubGroupTbl_SubGroupCode', 'SubGroupCode', 'SubGroupId'),
    )

    SubGroupId = Column(Integer, primary_key=True)
    GroupId = Column(Integer, ForeignKey('GroupTbl.GroupId'))
    SubGroupCode = Column(String(4))
    SubGroupDesc = Column(String(100))
    DateCreate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)
    DateUpdate = Column(DateTime, server_default=text("(getutcdate())"), nullable=False)
