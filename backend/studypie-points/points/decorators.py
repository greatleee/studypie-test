from datetime import timedelta
from random import randint

from django.db import transaction
from django.utils import timezone

from .actions import actions
from .models import PointDefinition, PointIssued, PointConsumed


class TriggerPoint(object):

    def __init__(self, action):
        self.action = action

    def __call__(self, func):
        d_self = self
        def wrapper(*args, **kwargs):
            if d_self.action in actions:
                user = d_self.get_user(args)
                if user.is_anonymous:
                    raise Exception("Not authorized")
                _issue_or_consume_points(d_self.action, user) 
            else:
                raise Exception("Not supported action")
            return func(*args, **kwargs)
        return wrapper

    def get_user(self, args):
        info = args[1]
        if not info.context:
            raise Exception("Use this decorator only for mutation")
        return info.context.user


def _issue_or_consume_points(action, user):
    point_def = PointDefinition.objects.get(action=action)
    now = timezone.now()
    if point_def.point >= 0:
        PointIssued.objects.create(
            action=action,
            point=point_def.point, 
            remained_point=point_def.point,
            user=user,
            expire_at=now + \
                timedelta(days=point_def.valid_period),
            created_at=now,
        )
    else:
        with transaction.atomic():
            subtract_point = abs(point_def.point)
            point_issued_queryset = PointIssued.objects.filter(
                remained_point__gt=0,
                expire_at__gte=now,
                user=user,
            ).select_for_update(nowait=True).order_by('expire_at')
            for point in point_issued_queryset:
                if point.remained_point >= subtract_point:
                    point.remained_point -= subtract_point
                    subtract_point -= subtract_point
                else:
                    subtract_point -= point.remained_point
                    point.remained_point -= \
                        point.remained_point
                point.save()
                if subtract_point == 0:
                    break
            if subtract_point != 0:
                raise Exception('Lack of points')
            PointConsumed.objects.create(
                action=action,
                point=abs(point_def.point),
                user=user,
            )
