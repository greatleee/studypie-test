import graphene

import points.schema as points_schema


class Query(
    points_schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query)
