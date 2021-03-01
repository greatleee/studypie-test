import graphene

import apps.users.schema as users_schema


class Query(users_schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
