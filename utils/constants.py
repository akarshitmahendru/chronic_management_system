from enum import Enum


class ChronicToolEnum(Enum):
    @classmethod
    def values(cls):
        return [member.value for member in cls]


INVALID_CREDENTIALS_ERROR = "Your credentials do not match."
NON_REGISTERED_ACCOUNT = "User does not exists."

ROLES = (
    (1, 'Doctor'),
    (2, 'Patient')
)


class RoleEnum(ChronicToolEnum):
    DOCTOR = 1
    PATIENT = 2


SEX = (
    (1, 'Male'),
    (2, 'Female'),
    (3, 'Other')
)


class SexEnum(ChronicToolEnum):
    MALE = 1
    FEMALE = 2
    OTHER = 3
