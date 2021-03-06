import graphene
from django.db.models import Sum
from django.utils import timezone
from graphene import relay
from graphene_django import DjangoObjectType

from .models import PointIssued, PointConsumed


class PointIssuedType(DjangoObjectType):
    class Meta:
        model = PointIssued
        interfaces = (relay.Node,)  # make sure you add this
        fields = "__all__"


class PointIssuedConnection(relay.Connection):
    class Meta:
        node = PointIssuedType


class PointConsumedType(DjangoObjectType):
    class Meta:
        model = PointConsumed
        interfaces = (relay.Node,)  # make sure you add this
        fields = "__all__"


class PointConsumedConnection(relay.Connection):
    class Meta:
        node = PointConsumedType


class Query(graphene.ObjectType):
    total_remained_point = graphene.Int()
    points_issued = relay.ConnectionField(PointIssuedConnection)
    points_expired = relay.ConnectionField(PointIssuedConnection)
    points_consumed = relay.ConnectionField(PointConsumedConnection)

    def resolve_total_remained_point(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        now = timezone.now()
        result = PointIssued.objects.filter(
            remained_point__gt=0, expire_at__gte=now, user=user
        ).aggregate(Sum("remained_point"))
        return result["remained_point__sum"]

    def resolve_points_issued(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return PointIssued.objects.filter(user=user)

    def resolve_points_expired(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        now = timezone.now()
        return PointIssued.objects.filter(expire_at__lte=now, user=user)

    def resolve_points_consumed(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return PointConsumed.objects.filter(user=user)
