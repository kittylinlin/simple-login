from graphene_federation import build_schema
from .user.schema import UserQueries, UserMutations


class Query(
    UserQueries,
):
    pass


class Mutation(
    UserMutations,
):
    pass


schema = build_schema(Query, mutation=Mutation)
