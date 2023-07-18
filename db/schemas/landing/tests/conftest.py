import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.schemas.landing.tables import (Base, Project, GroupTbl, SubGroupTbl,
                                       CountryCat, UserTbl, ProjectPermission,
                                       CountryPermission, GroupPermission,
                                       SubGroupPermission, PermissionView)
from sqlalchemy import MetaData


@pytest.fixture()
def test_db():
    engine = create_engine('sqlite:///:memory:')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Get the metadata for all tables except PermissionView
    metadata = MetaData()
    for table in Base.metadata.tables.values():
        if table.name != 'PermissionView':
            table.tometadata(metadata)

    metadata.create_all(bind=engine)

    db = SessionLocal()

    db.commit()
    yield db
    db.close()

def create_permission_view_query(db, user_id: int) -> list[PermissionView]:
    result = db.query(
        UserTbl,
        ProjectPermission,
        Project,
        CountryPermission,
        CountryCat,
        GroupPermission,
        GroupTbl,
        SubGroupPermission,
        SubGroupTbl
    ).filter(
        UserTbl.UserId == user_id
    ).outerjoin(
        ProjectPermission, UserTbl.UserId == ProjectPermission.user_id
    ).outerjoin(
        Project, ProjectPermission.project_id == Project.ProjectId
    ).outerjoin(
        CountryPermission, UserTbl.UserId == CountryPermission.user_id
    ).outerjoin(
        CountryCat, CountryPermission.country_id == CountryCat.CountryId
    ).outerjoin(
        GroupPermission, UserTbl.UserId == GroupPermission.user_id
    ).outerjoin(
        GroupTbl, GroupPermission.group_id == GroupTbl.GroupId
    ).outerjoin(
        SubGroupPermission, UserTbl.UserId == SubGroupPermission.user_id
    ).outerjoin(
        SubGroupTbl, SubGroupPermission.subgroup_id == SubGroupTbl.SubGroupId
    ).all()

    view_list = []
    for row in result:
        view_obj = PermissionView(
            UserId=row[0].UserId,
            Email=row[0].Email,
            IsSuperUser=row[0].IsSuperUser,
            ProjectPermissionProjectId=row[1].project_id if row[1] else None,
            ProjectPermissionPermission=row[1].permission if row[1] else None,
            CountryPermissionCountryId=row[3].country_id if row[3] else None,
            CountryPermissionPermission=row[3].permission if row[3] else None,
            GroupPermissionGroupId=row[5].group_id if row[5] else None,
            GroupPermissionProjectId=row[5].project_id if row[5] else None,
            GroupPermissionPermission=row[5].permission if row[5] else None,
            SubGroupPermissionSubgroupId=row[7].subgroup_id if row[7] else None,
            SubGroupPermissionGroupId=row[7].group_id if row[7] else None,
            SubGroupPermissionProjectId=row[7].project_id if row[7] else None,
            SubGroupPermissionPermission=row[7].permission if row[7] else None,
            subgroupCode=row[8].SubGroupCode if row[8] else None,
            CountryCode=row[4].CountryCode if row[4] else None,
            GroupCode=row[6].GroupCode if row[5] else None,
            ProjectName=row[2].ProjectName if row[2] else None
        )
        view_list.append(view_obj)

    return view_list
    

def create_mock_user(db, email="testuser@email.com", is_superuser=False) -> UserTbl:
    # Create a superuser
    test_user = UserTbl(
        Email=email,
        IsSuperUser=is_superuser,
    )
    db.add(test_user)
    db.commit()
    return test_user

def create_mock_country(db, country_id: int, country_code: str, country_desc: str) -> CountryCat:
    country = CountryCat(CountryId=country_id, CountryCode=country_code, CountryDesc=country_desc)
    db.add(country)
    db.commit()
    return country


def create_mock_group(db, group_id: int, group_code: str, group_desc: str, country_id: int) -> GroupTbl:
    group = GroupTbl(GroupId=group_id, GroupCode=group_code, GroupDesc=group_desc, CountryId=country_id)
    db.add(group)
    db.commit()
    return group


def create_mock_subgroup(db, subgroup_id: int, subgroup_code: str, subgroup_desc: str, group_id: int) -> SubGroupTbl:
    subgroup = SubGroupTbl(SubGroupId=subgroup_id, SubGroupCode=subgroup_code, SubGroupDesc=subgroup_desc, GroupId=group_id)
    db.add(subgroup)
    db.commit()
    return subgroup

