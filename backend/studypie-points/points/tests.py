import pytest

from django.db.models import Sum

from .actions import actions
from .decorators import _issue_or_consume_points
from .models import PointDefinition, PointIssued, PointConsumed


def test__issue_or_consume_points(admin_user):
    PointDefinition.objects.create(
        action=actions.CREATE_POST,
        point=-50,
        valid_period=30,
    )
    PointDefinition.objects.create(
        action=actions.CREATE_COMMENT,
        point=100,
        valid_period=30,
    )

    _issue_or_consume_points(actions.CREATE_COMMENT, admin_user)
    point = PointIssued.objects.filter(user=admin_user).first()
    assert point.remained_point == 100

    _issue_or_consume_points(actions.CREATE_POST, admin_user)
    point = PointIssued.objects.filter(user=admin_user).first()
    assert point.remained_point == 50

    _issue_or_consume_points(actions.CREATE_POST, admin_user)
    point = PointIssued.objects.filter(user=admin_user).first()
    assert point.remained_point == 0

    try:
        _issue_or_consume_points(actions.CREATE_POST, admin_user)
    except Exception as e:
        assert str(e) == 'Lack of points'

    point_def = PointDefinition.objects.get(action=actions.CREATE_COMMENT)
    point_def.point = 25
    point_def.save()

    for i in range(2):
        _issue_or_consume_points(actions.CREATE_COMMENT, admin_user)
    result = PointIssued.objects.filter(user=admin_user).aggregate(Sum('remained_point'))
    assert result['remained_point__sum'] == 50

    _issue_or_consume_points(actions.CREATE_POST, admin_user)
    result = PointIssued.objects.filter(user=admin_user).aggregate(Sum('remained_point'))
    assert result['remained_point__sum'] == 0
