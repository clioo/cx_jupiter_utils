from sqlalchemy import Enum
from lib.constants import AvailablePermissions


PermissionTypes = Enum(AvailablePermissions.READ, AvailablePermissions.READ_WRITE, AvailablePermissions.ADMIN, name='permission_types')