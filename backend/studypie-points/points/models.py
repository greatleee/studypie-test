from django.contrib.auth import get_user_model
from django.db import models

from .actions import action_choices


class PointDefinition(models.Model):
    action = models.SmallIntegerField(unique=True, choices=action_choices)
    point = models.SmallIntegerField(help_text="포인트를 소모해야하는 액션은 음수를 입력해주세요.")
    valid_period = models.SmallIntegerField(
        verbose_name="유효 기간(일)", help_text="포인트를 소모해야하는 액션은 0을 입력해주세요."
    )


class PointIssued(models.Model):
    class Meta:
        ordering = ["-created_at"]

    action = models.SmallIntegerField(choices=action_choices)
    point = models.PositiveSmallIntegerField()
    remained_point = models.PositiveSmallIntegerField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    expire_at = models.DateTimeField(verbose_name="만료일")
    created_at = models.DateTimeField(verbose_name="획득일")


class PointConsumed(models.Model):
    class Meta:
        ordering = ["-created_at"]

    action = models.SmallIntegerField(choices=action_choices)
    point = models.PositiveSmallIntegerField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
