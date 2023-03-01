from django.contrib.auth.base_user import BaseUserManager
from accounts.entities.query_mixin import UserQueryMixin
from utils.constants import RoleEnum


class UserManager(BaseUserManager, UserQueryMixin):

    def _create_user(self, password, phone_number, staff=None, **extra_fields):
        try:
            if staff:
                user = self.model(is_staff=True, phone_number=phone_number, is_superuser=True,
                                  role=RoleEnum.DOCTOR.value, **extra_fields)
                user.set_password(password)
                user.save()
                return user
        except Exception as e:
            print(e.args[0])

    def create_superuser(self, password, phone_number, **extra_fields):
        staff = True
        return self._create_user(password, phone_number, staff, **extra_fields)
