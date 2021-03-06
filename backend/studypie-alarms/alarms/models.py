from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer


class Alarm(models.Model):
    message = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


def create_alarm(message, post_creator):
    Alarm.objects.create(message=message, user=post_creator)


@receiver(post_save, sender=Alarm)
def create_alarm_event_listener(sender, instance, created, **kwargs):
    if not created:
        return
    user = instance.user
    group_name = "alarm_" + str(user.id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name, {
            "type": "notify_alarm",
            "id": instance.id,
            "message": instance.message,
        }
    )

