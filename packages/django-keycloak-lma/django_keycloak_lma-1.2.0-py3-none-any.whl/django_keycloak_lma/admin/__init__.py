from django.contrib import admin

from django_keycloak_lma.admin.realm import RealmAdmin
from django_keycloak_lma.admin.server import ServerAdmin
from django_keycloak_lma.models import Server, Realm

admin.site.register(Realm, RealmAdmin)
admin.site.register(Server, ServerAdmin)
