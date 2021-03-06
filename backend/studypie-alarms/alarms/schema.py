import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

from .models import Alarm


class AlarmType(DjangoObjectType):
    class Meta:
        model = Alarm
        interfaces = (relay.Node,)  # make sure you add this
        fields = "__all__"


class AlarmConnection(relay.Connection):
    class Meta:
        node = AlarmType


class Query(graphene.ObjectType):
    alarms = relay.ConnectionField(AlarmConnection)
    alarms_not_checked = relay.ConnectionField(AlarmConnection)

    def resolve_alarms(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return Alarm.objects.filter(user=user)

    def resolve_alarms_not_checked(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return Alarm.objects.filter(user=user, is_checked=False)


class SetAlarmIsCheckedMutation(relay.ClientIDMutation):
    alarm = graphene.Field(AlarmType)

    class Input:
        id = graphene.ID()

    def mutate_and_get_payload(self, info, id):
        try:
            obj_id = int(id)
        except Exception:
            obj_id = from_global_id(id)[1]
        alarm = Alarm.objects.get(id=obj_id)
        alarm.is_checked = True
        alarm.save()
        return SetAlarmIsCheckedMutation(alarm=alarm)


class Mutation(graphene.ObjectType):
    set_alarm_is_checked = SetAlarmIsCheckedMutation.Field()
