from api.v1.roles import RoleByNameView, RoleView, roles
from api.v1.sessions import SessionByOAuth, SessionView, sessions
from api.v1.users import SubscribeView, UserView, users
from apps.api import path

urlpatterns = [
    path('/sessions', sessions, SessionView),
    path('/sessions/<string:provider_name>', sessions, SessionByOAuth),
    path('/roles', roles, RoleView),
    path('/roles/<string:role_name>', roles, RoleByNameView),
    path('/users', users, UserView),
    path('/users/<uuid:user_pk>/subscribe', users, SubscribeView),
]
