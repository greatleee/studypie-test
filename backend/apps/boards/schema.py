import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import Board, Post, Comment


class BoardType(DjangoObjectType):
    class Meta:
        model = Board


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    all_boards = graphene.List(BoardType)

    def resolve_all_boards(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return Board.objects.all()


class BoardMutation(graphene.Mutation):
    all_boards = graphene.List(BoardType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        if info.context.user.is_anonymous:
            raise Exception('Not logged in!')
        if info.context.user.is_superuser is False:
            raise GraphQLError('Permission denied', status=403)
        try:
            Board.objects.create(name=name)
            all_boards = Board.objects.all()
            return BoardMutation(all_boards=all_boards)
        except Exception:
            raise Exception('Creating board is failed.')


class Mutation(graphene.ObjectType):
    create_board = BoardMutation.Field()
