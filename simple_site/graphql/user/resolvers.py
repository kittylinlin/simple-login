import graphene
from .models import User


def resolve_users(root, info):
    return User.objects.all()
