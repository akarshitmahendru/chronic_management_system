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


PATIENT_ATTRIBUTES = (
    (1, 'Blood Pressure'),
    (2, 'Heart Rate'),
    (3, 'Blood Sugar Level'),
    (4, 'Weight')
)


class PatientAttributes(ChronicToolEnum):
    BP = 1
    HEAR_RATE = 2
    SUGAR_LEVEL = 3
    WEIGHT = 4


PLAN_FREQUENCY = (
    (1, 'Day'),
    (2, 'Hours'),
    (3, 'Minutes')
)


class PlanFrequencyEnum(ChronicToolEnum):
    DAY = 1
    HOURS = 2
    MINUTES = 3


class PlanEnum(ChronicToolEnum):
    MEDICATIONS = 1
    DIET = 2
    EXERCISE = 3
    MONITORING = 4
    OTHERS = 5


PATIENT_PLAN = (
    (1, 'Medications'),
    (2, 'Diet'),
    (3, 'Exercise'),
    (4, 'Monitoring'),
    (5, 'Others')
)


class PlanStatusEnum(ChronicToolEnum):
    ACTIVE = 1
    PAUSE_REMINDERS = 2
    INACTIVE = 3


PLAN_STATUS = (
    (1, 'Active'),
    (2, 'Pause Reminders'),
    (3, 'Inactive')
)


class NotificationStatusEnum(ChronicToolEnum):
    READ = 1
    IGNORED = 2
    NO_ACTION = 3


NOTIFICATION_STATUS = (
    (1, 'Read'),
    (2, 'Ignored'),
    (3, 'No Action')
)
