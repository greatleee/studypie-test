import graphene
from django.db import transaction
from graphene_django import DjangoObjectType

from .models import Board, Post, Comment
from alarms.models import create_alarm
from points.actions import actions
from points.decorators import TriggerPoint


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
    posts_by_board = graphene.List(PostType, board_id=graphene.Int())
    post_by_id = graphene.Field(PostType, post_id=graphene.Int())
    comments_by_post = graphene.Field(CommentType, post_id=graphene.Int())

    def resolve_all_boards(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return Board.objects.all()

    def resolve_posts_by_board(self, info, board_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return Post.objects.filter(board_id=board_id).order_by('created_at')

    def resolve_post_by_id(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return None


class BoardMutation(graphene.Mutation):
    all_boards = graphene.List(BoardType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        if info.context.user.is_anonymous:
            raise Exception('Not logged in!')
        if info.context.user.is_superuser is False:
            raise Exception('Permission denied')
        try:
            Board.objects.create(name=name)
            all_boards = Board.objects.all()
            return BoardMutation(all_boards=all_boards)
        except Exception as e:
            print(e)
            raise Exception('Creating board is failed.')


class CreatePost(graphene.Mutation):
    posts_by_board = graphene.List(PostType, board_id=graphene.Int())

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        board_id = graphene.Int(required=True)

    @TriggerPoint(actions.CREATE_POST)
    def mutate(self, info, title, content, board_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        try:
            Post.objects.create(
                title=title,
                content=content,
                creator=user,
                updater=user,
                board_id=board_id,
            )
            posts_by_board = Post.objects.filter(
                board_id=board_id).order_by('created_at')
            return CreatePost(posts_by_board=posts_by_board)
        except Exception as e:
            print(e)
            raise Exception('Creating Post is failed.')


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=False)
        content = graphene.String(required=False)

    def mutate(self, info, id, title=None, content=None):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        with transaction.atomic():
            try:
                post = Post.objects.get(id=id).select_for_update(nowait=True)
            except Post.DoesNotExist:
                raise Exception('')
            except Exception:
                raise Exception('')

            if user.is_superuser is False and user.id != post.creator.id:
                raise Exception('Permission denied')
            
            try:
                if title:
                    post.title = title
                if content:
                    post.content = content
                if title or content:
                    post.updater = user
                post.save()
                return CreatePost(post=post)
            except Exception as e:
                print(e)
                raise Exception('Updating Post is failed.')


class DeletePost(graphene.Mutation):
    posts_by_board = graphene.List(PostType, board_id=graphene.Int())

    class Arguments:
        id = graphene.Int(required=True)
        board_id = graphene.Int(required=True)

    def mutate(self, info, id, board_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        post = Post.objects.get(id=id)
        if user.is_superuser is False and user.id != post.creator.id:
            raise Exception('Permission denied')

        try:
            post.delete()
            posts_by_board = Post.objects.filter(
                board_id=board_id).order_by('created_at')
            return DeletePost(posts_by_board=posts_by_board)
        except Exception as e:
            print(e)
            raise Exception('Deleting Post is failed.')


class CreateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)

    class Arguments:
        content = graphene.String(required=True)
        post_id = graphene.Int(required=True)

    @TriggerPoint(actions.CREATE_COMMENT)
    def mutate(self, info, content, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        try:
            comment = Comment.objects.create(
                content=content,
                creator=user,
                post_id=post_id,
            )
            create_alarm(user.username + "이/가 \"" + comment.post.title + "\"에 댓글을 남겼습니다.", comment.post.creator)
            return CreateComment(comment=comment)
        except Exception as e:
            print(e)
            raise Exception('Creating comment is failed.')


class Mutation(graphene.ObjectType):
    create_board = BoardMutation.Field()
    create_post = CreatePost.Field()
    delete_post = DeletePost.Field()
    update_post = UpdatePost.Field()
    create_comment = CreateComment.Field()
