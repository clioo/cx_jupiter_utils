from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index, CHAR
from sqlalchemy.sql import text, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

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
    DateCreate = Column(DateTime, server_default=func.now(), nullable=False)
    DateUpdate = Column(DateTime, server_default=func.now(), nullable=False)


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
    DateCreate = Column(DateTime, server_default=func.now(), nullable=False)
    DateUpdate = Column(DateTime, server_default=func.now(), nullable=False)

class CountryCat(Base):
    __tablename__ = 'CountryCat'
    __table_args__ = (
        UniqueConstraint('CountryCode', name='UQ_CountryCode'),
    )

    CountryId = Column(Integer, primary_key=True)
    CountryCode = Column(CHAR(2), nullable=False)
    CountryDesc = Column(String(50))
