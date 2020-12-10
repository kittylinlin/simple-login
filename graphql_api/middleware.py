import jwt
from bson import ObjectId
from django.conf import settings


class JWTAuthorizationMiddleware(object):
    def __init__(self):
        pass

    def resolve(self, next, root, info, **args):
        authorization = info.context.headers.get('Authorization')
        if authorization is None:
            return next(root, info, **args)

        access_token = authorization.split('Bearer ')[1]
        if access_token is None:
            return next(root, info, **args)

        jwt_secret = settings.JWT["SECRET"]
        jwt_issuer = settings.JWT["ISSUER"]
        jwt_audience = settings.JWT["AUDIENCE"]
        try:
            user_data = jwt.decode(access_token, jwt_secret, issuer=jwt_issuer, audience=jwt_audience)
        except Exception as e:
            raise e

        user_id = user_data.get('sub')
        if not ObjectId.is_valid(user_id):
            raise Exception('Invalid refresh token')

        info.context.user_id = user_id

        return next(root, info, **args)
