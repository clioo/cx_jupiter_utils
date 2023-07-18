vista:

CREATE VIEW PermissionView AS
SELECT 
    webservice.[UserTbl].UserId,
    webservice.[UserTbl].Email,
    webservice.[UserTbl].IsSuperUser,
    Project.ProjectName,
    ProjectPermission.project_id AS ProjectPermissionProjectId,
    ProjectPermission.permission AS ProjectPermissionPermission,
    CountryCat.CountryCode,
    CountryPermission.country_id AS CountryPermissionCountryId,
    CountryPermission.permission AS CountryPermissionPermission,
    GroupTbl.GroupCode,
    GroupPermission.group_id AS GroupPermissionGroupId,
    GroupPermission.project_id AS GroupPermissionProjectId,
    GroupPermission.permission AS GroupPermissionPermission,
    SubGroupTbl.SubGroupCode,
    SubGroupPermission.subgroup_id AS SubGroupPermissionSubgroupId,
    SubGroupPermission.group_id AS SubGroupPermissionGroupId,
    SubGroupPermission.project_id AS SubGroupPermissionProjectId,
    SubGroupPermission.permission AS SubGroupPermissionPermission
FROM
    webservice.[UserTbl]
LEFT JOIN
    ProjectPermission ON webservice.[UserTbl].UserId = ProjectPermission.user_id
LEFT JOIN
    Project ON ProjectPermission.project_id = Project.ProjectId
LEFT JOIN
    CountryPermission ON webservice.[UserTbl].UserId = CountryPermission.user_id
LEFT JOIN
    CountryCat ON CountryPermission.country_id = CountryCat.CountryId
LEFT JOIN
    GroupPermission ON webservice.[UserTbl].UserId = GroupPermission.user_id
LEFT JOIN
    GroupTbl ON GroupPermission.group_id = GroupTbl.GroupId
LEFT JOIN
    SubGroupPermission ON webservice.[UserTbl].UserId = SubGroupPermission.user_id
LEFT JOIN
    SubGroupTbl ON SubGroupPermission.subgroup_id = SubGroupTbl.SubGroupId;