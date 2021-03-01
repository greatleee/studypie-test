import graphene

import apps.boards.schema as boards_schema
import apps.users.schema as users_schema


class Query(
    boards_schema.Query,
    users_schema.Query,
    graphene.ObjectType,
):
    pass

class Mutation(
    boards_schema.Mutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
