import datetime
import celery
from celery import Task
from django.utils import timezone
from utils.constants import PlanStatusEnum
from django.db.models import Q

from utils.push_notifications import FireBaseActions


@celery.task
def clear_notification_scheduler():
    from notifications.models import NotificationsScheduler, Notification
    time_now = timezone.now()
    five_minutes_before = time_now - datetime.timedelta(minutes=5)
    five_minutes_after = time_now + datetime.timedelta(minutes=5)
    scheduled_jobs = NotificationsScheduler.objects.filter(
        scheduled_time__gte=five_minutes_before, scheduled_time__lt=five_minutes_after,
        patient_plan__plan_status=PlanStatusEnum.ACTIVE.value,
        patient_plan__notification_heading__isnull=False, patient_plan__notification_body__isnull=False
    ).exclude(Q(patient_plan__notification_heading="") | Q(patient_plan__notification_body=""))
    for job in scheduled_jobs:
        patient_plan = job.patient_plan
        user = patient_plan.patient
        fcm_token = user.fcm_token
        notification = Notification.objects.create(user_id=user.id, patient_plan=patient_plan,
                                                   notification_title=patient_plan.notification_heading,
                                                   notification_body=patient_plan.notification_body)
        data = dict()
        data["title"] = notification.notification_title
        data["body"] = notification.notification_body
        data['notification_id'] = str(notification.id)
        FireBaseActions.send_message(user_tokens=[fcm_token], data=data)
        job.last_triggered_on = timezone.now()
        if job.fetch_scheduled_time():
            job.scheduled_time = job.fetch_scheduled_time()
        job.save()
