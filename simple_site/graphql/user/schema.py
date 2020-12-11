import graphene
from .models import User
from djongo import models
from .resolvers import resolve_users
from graphene_django import DjangoObjectType
from ..utils.auth import get_user_id_from_info
from .mutations import (
    SignUp,
    Login,
    RefreshToken,
)
from graphene_django.converter import convert_django_field


@convert_django_field.register(models.ObjectIdField)
def convert_objectId_to_str(*_args):
    return graphene.ID()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        convert_choices_to_enum = False


class UserQueries(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(root, info):
        get_user_id_from_info(info)
        return resolve_users(root, info)


class UserMutations(graphene.ObjectType):
    sign_up = SignUp.Field()
    login = Login.Field()
    refresh_token = RefreshToken.Field()
