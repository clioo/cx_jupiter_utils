from db.schemas.landing.tables import Project, ProjectPermission, CountryPermission, GroupPermission, SubGroupPermission
from db.schemas.landing.services import get_permission_level_by_user_email
from lib.constants import AvailablePermissions
from db.schemas.landing.tests.conftest import create_mock_user, create_mock_country, create_mock_group, create_mock_subgroup, create_permission_view_query

# Test if user can be created
def test_create_user(test_db):
    db = test_db
    test_user = create_mock_user(db, is_superuser=True)
    assert test_user.UserId is not None


def test_superuser_access_to_all_projects(test_db):
    db = test_db
    test_user = create_mock_user(db, is_superuser=True)

    # Create two projects
    project1 = Project(ProjectName="Project3")
    project2 = Project(ProjectName="Project4")
    db.add(project1)
    db.add(project2)
    db.commit()

    # Test if superuser has admin level access to both projects
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName) == AvailablePermissions.ADMIN
    assert get_permission_level_by_user_email(db, test_user.Email, project2.ProjectName) == AvailablePermissions.ADMIN


def test_superuser_access_to_projects_per_country(test_db):
    db = test_db
    # Create a superuser
    test_user = create_mock_user(db, is_superuser=True)

    # Create countries

    country1 = create_mock_country(db=db, country_id=3, country_code="US", country_desc="United States")
    country2 = create_mock_country(db=db, country_id=4, country_code="CA", country_desc="Canada")

    # Create groups associated with countries
    group1 = create_mock_group(db=db, group_id=1, group_code="G1", group_desc="Group 1", country_id=country1.CountryId)
    group2 = create_mock_group(db=db, group_id=2, group_code="G2", group_desc="Group 2", country_id=country2.CountryId)

    # Create subgroups associated with groups
    create_mock_subgroup(db=db, subgroup_id=1, subgroup_code="SG1", subgroup_desc="Sub Group 1", group_id=group1.GroupId)
    create_mock_subgroup(db=db, subgroup_id=2, subgroup_code="SG2", subgroup_desc="Sub Group 2", group_id=group2.GroupId)

    # Create projects and associate them with subgroups (which are in turn associated with groups and countries)
    project1 = Project(ProjectName="Project1")
    project2 = Project(ProjectName="Project2")
    db.add(project1)
    db.add(project2)
    db.commit()

    # Test if superuser has admin level access to both projects (via country permissions)
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName, country_code=country1.CountryCode) == AvailablePermissions.ADMIN
    assert get_permission_level_by_user_email(db, test_user.Email, project2.ProjectName, country_code=country2.CountryCode) == AvailablePermissions.ADMIN


def test_superuser_access_to_projects_in_certain_group(test_db):
    db = test_db

    # Create a superuser
    test_user = create_mock_user(db, is_superuser=True)

    # Create a country
    country = create_mock_country(db, country_id=5, country_code="MX", country_desc="Mexico")

    # Create two groups associated with the same country
    group1 = create_mock_group(db, group_id=3, group_code="G3", group_desc="Group 3", country_id=country.CountryId)
    group2 = create_mock_group(db, group_id=4, group_code="G4", group_desc="Group 4", country_id=country.CountryId)

    # Create subgroups associated with groups
    create_mock_subgroup(db, subgroup_id=3, subgroup_code="SG3", subgroup_desc="Sub Group 3", group_id=group1.GroupId)
    create_mock_subgroup(db, subgroup_id=4, subgroup_code="SG4", subgroup_desc="Sub Group 4", group_id=group2.GroupId)

    # Create projects and associate them with subgroups (which are in turn associated with groups and countries)
    project1 = Project(ProjectId=3, ProjectName="Project3")
    project2 = Project(ProjectId=4, ProjectName="Project4")
    db.add(project1)
    db.add(project2)
    db.commit()

    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName, group_code=group1.GroupCode) == AvailablePermissions.ADMIN
    assert get_permission_level_by_user_email(db, test_user.Email, project2.ProjectName, group_code=group2.GroupCode) == AvailablePermissions.ADMIN



def test_superuser_access_to_projects_in_certain_subgroup(test_db):
    db = test_db

    # Create a superuser
    test_user = create_mock_user(db, is_superuser=True)

    # Create a country
    country = create_mock_country(db, country_id=6, country_code="BR", country_desc="Brazil")

    # Create a group associated with the country
    group = create_mock_group(db, group_id=5, group_code="G5", group_desc="Group 5", country_id=country.CountryId)

    # Create two subgroups associated with the same group
    subgroup1 = create_mock_subgroup(db, subgroup_id=5, subgroup_code="SG5", subgroup_desc="Sub Group 5", group_id=group.GroupId)
    subgroup2 = create_mock_subgroup(db, subgroup_id=6, subgroup_code="SG6", subgroup_desc="Sub Group 6", group_id=group.GroupId)

    # Create projects
    project1 = Project(ProjectId=5, ProjectName="Project5")
    project2 = Project(ProjectId=6, ProjectName="Project6")
    db.add(project1)
    db.add(project2)
    db.commit()

    # Test if superuser has admin level access to both projects in subgroup1
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName, subgroup_code=subgroup1.SubGroupCode) == AvailablePermissions.ADMIN
    assert get_permission_level_by_user_email(db, test_user.Email, project2.ProjectName, subgroup_code=subgroup1.SubGroupCode) == AvailablePermissions.ADMIN

    # Test if superuser has admin level access to both projects in subgroup2
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName, subgroup_code=subgroup2.SubGroupCode) == AvailablePermissions.ADMIN
    assert get_permission_level_by_user_email(db, test_user.Email, project2.ProjectName, subgroup_code=subgroup2.SubGroupCode) == AvailablePermissions.ADMIN


def test_user_access_to_project_in_certain_subgroup(mocker, test_db):
    db = test_db

    # Create a non-superuser
    test_user = create_mock_user(db, is_superuser=False)

    # Create a country
    country = create_mock_country(db, country_id=7, country_code="FR", country_desc="France")

    # Create a group associated with the country
    group = create_mock_group(db, group_id=6, group_code="G6", group_desc="Group 6", country_id=country.CountryId)

    # Create a subgroup associated with the group
    subgroup = create_mock_subgroup(db, subgroup_id=7, subgroup_code="SG7", subgroup_desc="Sub Group 7", group_id=group.GroupId)

    # Create projects
    project1 = Project(ProjectId=7, ProjectName="Project7")
    project2 = Project(ProjectId=8, ProjectName="Project8")
    db.add(project1)
    db.add(project2)
    db.commit()

    # Create subgroup permission for the user for subgroup1
    subgroup_permission = SubGroupPermission(
        user_id=test_user.UserId,
        subgroup_id=subgroup.SubGroupId,
        group_id=group.GroupId,
        country_id=country.CountryId,
        project_id=project1.ProjectId,
        permission=AvailablePermissions.READ_WRITE
    )
    db.add(subgroup_permission)
    db.commit()

    permission_list = create_permission_view_query(db, test_user.UserId)
    if len(permission_list) > 0:
        permission = permission_list[0]
        mocker.patch(
            "db.schemas.landing.services.get_permission_from_view_by_user_id_and_project_name",
            return_value=permission
        )

    # Test if user has read/write level access to project1 in the certain subgroup
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName, subgroup_code=subgroup.SubGroupCode) == AvailablePermissions.READ_WRITE


def test_user_access_to_project_in_certain_group(mocker, test_db):
    db = test_db

    # Create a non-superuser
    test_user = create_mock_user(db, is_superuser=False)

    # Create a country
    country = create_mock_country(db, country_id=7, country_code="FR", country_desc="France")

    # Create a group associated with the country
    group = create_mock_group(db, group_id=6, group_code="G6", group_desc="Group 6", country_id=country.CountryId)

    # Create projects
    project1 = Project(ProjectId=7, ProjectName="Project7")
    project2 = Project(ProjectId=8, ProjectName="Project8")
    db.add(project1)
    db.add(project2)
    db.commit()

    # Create group permission for the user for group
    group_permission = GroupPermission(
        user_id=test_user.UserId,
        group_id=group.GroupId,
        country_id=country.CountryId,
        project_id=project1.ProjectId,
        permission=AvailablePermissions.READ_WRITE
    )
    db.add(group_permission)
    db.commit()

    permission_list = create_permission_view_query(db, test_user.UserId)
    if len(permission_list) > 0:
        permission = permission_list[0]
        mocker.patch(
            "db.schemas.landing.services.get_permission_from_view_by_user_id_and_project_name",
            return_value=permission
        )

    # Test if user has read/write level access to project1 in the certain group
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName, group_code=group.GroupCode) == AvailablePermissions.READ_WRITE


def test_user_access_to_project_in_certain_country(mocker, test_db):
    db = test_db

    # Create a non-superuser
    test_user = create_mock_user(db, is_superuser=False)

    # Create a country
    country = create_mock_country(db, country_id=7, country_code="FR", country_desc="France")

    # Create projects
    project1 = Project(ProjectId=7, ProjectName="Project7")
    project2 = Project(ProjectId=8, ProjectName="Project8")
    db.add(project1)
    db.add(project2)
    db.commit()

    # Create country permission for the user for country
    country_permission = CountryPermission(
        user_id=test_user.UserId,
        country_id=country.CountryId,
        permission=AvailablePermissions.READ_WRITE
    )
    db.add(country_permission)
    db.commit()

    permission_list = create_permission_view_query(db, test_user.UserId)
    if len(permission_list) > 0:
        permission = permission_list[0]
        mocker.patch(
            "db.schemas.landing.services.get_permission_from_view_by_user_id_and_project_name",
            return_value=permission
        )

    # Test if user has read/write level access to project1 in the certain country
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName, country_code=country.CountryCode) == AvailablePermissions.READ_WRITE


def test_user_access_to_specific_project_read_write_no_permission(mocker, test_db):
    """
    To have read or write/write permissions level, a geographical scope must be provided, admin level access is enough for project level access.
    """
    db = test_db

    # Create a non-superuser
    test_user = create_mock_user(db, is_superuser=False)

    # Create projects
    project1 = Project(ProjectId=7, ProjectName="Project7")
    project2 = Project(ProjectId=8, ProjectName="Project8")
    db.add(project1)
    db.add(project2)
    db.commit()

    # Create project permission for the user for project1
    project_permission = ProjectPermission(
        user_id=test_user.UserId,
        project_id=project1.ProjectId,
        permission=AvailablePermissions.READ_WRITE
    )
    db.add(project_permission)
    db.commit()

    permission_list = create_permission_view_query(db, test_user.UserId)
    if len(permission_list) > 0:
        permission = permission_list[0]
        mocker.patch(
            "db.schemas.landing.services.get_permission_from_view_by_user_id_and_project_name",
            return_value=permission
        )

    # Test if user has read/write level access to project1
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName) == None


def test_user_access_to_specific_project_read_write_no_permission(mocker, test_db):
    db = test_db

    # Create a non-superuser
    test_user = create_mock_user(db, is_superuser=False)

    # Create projects
    project1 = Project(ProjectId=7, ProjectName="Project7")
    project2 = Project(ProjectId=8, ProjectName="Project8")
    db.add(project1)
    db.add(project2)
    db.commit()

    # Create project permission for the user for project1
    project_permission = ProjectPermission(
        user_id=test_user.UserId,
        project_id=project1.ProjectId,
        permission=AvailablePermissions.READ_WRITE
    )
    db.add(project_permission)
    db.commit()

    country = create_mock_country(db, country_id=7, country_code="FR", country_desc="France")

    # Create a group associated with the country
    group = create_mock_group(db, group_id=6, group_code="G6", group_desc="Group 6", country_id=country.CountryId)

    # Create group permission for the user for group
    group_permission = GroupPermission(
        user_id=test_user.UserId,
        group_id=group.GroupId,
        country_id=country.CountryId,
        project_id=project1.ProjectId,
        permission=AvailablePermissions.READ_WRITE
    )
    db.add(group_permission)
    db.commit()


    permission_list = create_permission_view_query(db, test_user.UserId)
    if len(permission_list) > 0:
        permission = permission_list[0]
        mocker.patch(
            "db.schemas.landing.services.get_permission_from_view_by_user_id_and_project_name",
            return_value=permission
        )

    # Test if user has read/write level access to project1
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName) == None


def test_user_access_to_specific_project_admin_granted(mocker, test_db):
    db = test_db

    # Create a non-superuser
    test_user = create_mock_user(db, is_superuser=False)

    # Create projects
    project1 = Project(ProjectId=7, ProjectName="Project7")
    project2 = Project(ProjectId=8, ProjectName="Project8")
    db.add(project1)
    db.add(project2)
    db.commit()

    # Create project permission for the user for project1
    project_permission = ProjectPermission(
        user_id=test_user.UserId,
        project_id=project1.ProjectId,
        permission=AvailablePermissions.ADMIN
    )
    db.add(project_permission)
    db.commit()

    permission_list = create_permission_view_query(db, test_user.UserId)
    if len(permission_list) > 0:
        permission = permission_list[0]
        mocker.patch(
            "db.schemas.landing.services.get_permission_from_view_by_user_id_and_project_name",
            return_value=permission
        )

    # Test if user has read/write level access to project1
    assert get_permission_level_by_user_email(db, test_user.Email, project1.ProjectName) == AvailablePermissions.ADMIN
