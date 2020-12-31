import jwt
import bcrypt
import graphene
from .models import User
from bson import ObjectId
from django.conf import settings
from datetime import datetime, timedelta
from django.db.utils import DatabaseError
from django.core.exceptions import ObjectDoesNotExist


class SignUp(graphene.Mutation):
    class Arguments:
        account = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, account, password):
        encoded_password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt()).decode('utf-8')
        try:
            User(account=account, password=hashed_password).save()
        except DatabaseError:
            raise Exception('Account is already in use.')
        except Exception as e:
            print(e)
            raise Exception('Internal server error')
        return SignUp(ok=True)


class Login(graphene.Mutation):
    class Arguments:
        account = graphene.String(required=True)
        password = graphene.String(required=True)

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, root, info, account, password):
        try:
            user = User.objects.get(account=account)
        except ObjectDoesNotExist:
            raise Exception('Incorrect account or password')
        except Exception as e:
            print(e)
            raise Exception('Internal server error')

        encoded_password = password.encode('utf-8')
        encoded_user_password = user.password.encode('utf-8')
        if bcrypt.checkpw(encoded_password, encoded_user_password) is False:
            raise Exception('Incorrect account or password')

        if user.status != User.ACTIVE_STATUS:
            raise Exception('Your account is not active.')

        user.last_login_time = datetime.utcnow()
        try:
            user.save()
        except Exception as e:
            print(e)
            raise Exception('Internal server error')

        jwt_secret = settings.JWT["SECRET"]
        jwt_issuer = settings.JWT["ISSUER"]
        jwt_audience = settings.JWT["AUDIENCE"]
        utc_now = datetime.utcnow()
        payload = {
            'iss': jwt_issuer,
            'sub': str(user._id),
            'aud': jwt_audience,
            'exp': utc_now + timedelta(hours=1),
            'nbf': utc_now,
            'iat': utc_now
        }

        access_token = jwt.encode(payload, "9ff54167-4a8b-4bb4-80c1-69779b13c14b", algorithm='HS256').decode('utf-8')

        payload['exp'] = utc_now + timedelta(days=30)
        refresh_token = jwt.encode(payload, jwt_secret, algorithm='HS256').decode('utf-8')

        return Login(access_token=access_token, refresh_token=refresh_token)


class RefreshToken(graphene.Mutation):
    class Arguments:
        refresh_token = graphene.String(required=True)

    access_token = graphene.String()

    @classmethod
    def mutate(cls, root, info, refresh_token):
        jwt_secret = settings.JWT["SECRET"]
        jwt_issuer = settings.JWT["ISSUER"]
        jwt_audience = settings.JWT["AUDIENCE"]
        try:
            user_data = jwt.decode(refresh_token, jwt_secret, issuer=jwt_issuer, audience=jwt_audience)
        except Exception as e:
            raise e

        user_id = user_data.get('sub')
        if not ObjectId.is_valid(user_id):
            raise Exception('Invalid refresh token')

        try:
            user = User.objects.get(_id=ObjectId(user_id))
        except ObjectDoesNotExist:
            raise Exception('Invalid refresh token')
        except Exception as e:
            raise e

        utc_now = datetime.utcnow()
        payload = {
            'iss': jwt_issuer,
            'sub': user_id,
            'aud': jwt_audience,
            'exp': utc_now + timedelta(minutes=15),
            'nbf': utc_now,
            'iat': utc_now
        }

        access_token = jwt.encode(payload, jwt_secret, algorithm='HS256').decode('utf-8')
        return RefreshToken(access_token=access_token)
