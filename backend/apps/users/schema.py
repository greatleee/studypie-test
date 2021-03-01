import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ['password']


class Query(graphene.ObjectType):
  cur_user_info = graphene.Field(UserType)

  def resolve_cur_user_info(self, info):
    user = info.context.user
    if user.is_anonymous:
      raise Exception('Not logged in!')
    return user
