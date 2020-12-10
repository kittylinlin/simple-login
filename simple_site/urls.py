from django.urls import include, path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
