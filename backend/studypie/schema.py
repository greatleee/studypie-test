import graphene

import alarms.schema as alarms_schema
import points.schema as points_schema
import apps.boards.schema as boards_schema
import apps.users.schema as users_schema


class Query(
    alarms_schema.Query,
    boards_schema.Query,
    points_schema.Query,
    users_schema.Query,
    graphene.ObjectType,
):
    pass

class Mutation(
    alarms_schema.Mutation,
    boards_schema.Mutation,
    graphene.ObjectType,
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
