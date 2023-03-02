import datetime
import celery
from celery import Task
from django.utils import timezone
from utils.constants import PlanStatusEnum


@celery.task
def clear_notification_scheduler():
    from notifications.models import NotificationsScheduler, Notification
    time_now = timezone.now()
    five_minutes_before = time_now - datetime.timedelta(minutes=5)
    five_minutes_after = time_now + datetime.timedelta(minutes=5)
    scheduled_jobs = NotificationsScheduler.objects.filter(scheduled_time__gte=five_minutes_before,
                                                           scheduled_time__lt=five_minutes_after,
                                                           patient_plan__plan_status=PlanStatusEnum.ACTIVE.value)
    for job in scheduled_jobs:
        patient_plan = job.patient_plan
        user_id = patient_plan.patient_id

        Notification.objects.create(user_id=user_id, patient_plan=patient_plan,
                                    notification_title=patient_plan.notification_heading,
                                    notification_body=patient_plan.notification_body)
        job.last_triggered_on = timezone.now()
        if job.fetch_scheduled_time():
            job.scheduled_time = job.fetch_scheduled_time()
        job.save()




