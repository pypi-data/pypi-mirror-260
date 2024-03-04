from django.contrib.auth.models import User
from django.urls import path

from rest_framework import serializers, generics
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import PermissionDenied

from .models import Kontaktdaten, FachschaftUser
from .apps import app_name as parent_app_name

app_name = 'api'

# Serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
        ]


class FachschaftUserSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name=f'{parent_app_name}:{app_name}:user-detail',
        lookup_field='id',
    )
    class Meta:
        model = FachschaftUser
        fields = [
            'id',
            'nickname',
            'user',
        ]


class KontaktdatenSerializer(serializers.HyperlinkedModelSerializer):
    fachschaftuser = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name=f'{parent_app_name}:{app_name}:fachschaftuser-detail',
        lookup_field='id',
    )
    gecheckt_von = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name=f'{parent_app_name}:{app_name}:user-detail',
        lookup_field='id',
    )
    class Meta:
        model = Kontaktdaten
        fields = [
            'fachschaftuser',
            'created',
            'adresse',
            'telefonnummer',
            'gecheckt_von',
            'gecheckt_datum',
        ]


# Views

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class FachschaftUserDetail(generics.RetrieveAPIView):
    queryset = FachschaftUser.objects.all()
    serializer_class = FachschaftUserSerializer
    lookup_field = 'id'


class KontaktdatenListByFachschaftUser(APIView):
    permission_classes = [DjangoModelPermissions]
    queryset = Kontaktdaten.objects.all()

    def get(self, request, id, format=None):
        """
        Die normalen DjangoModelPermissions funktionieren nicht gut genug (jeder darf
        lesen), daher können wir die DjangoModelPermissions-Klasse ableiten oder
        einfach so checken, ob man die richtigen Permissions hat:

        (ohne permission_classes geht's aber auch nicht, daher ist das hier der
        einfachste Weg)
        """
        if not (request.user.has_perm(f'{parent_app_name}.view_kontaktdaten') or
            request.user.has_perm('{parent_app_name}.change_kontaktdaten')):
            raise PermissionDenied()
        else:
            kontaktdaten = Kontaktdaten.objects.filter(fachschaftuser=id)
            serializer = KontaktdatenSerializer(
                kontaktdaten,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)


# URLs

urlpatterns = format_suffix_patterns([
    path("fachschaftuser/<int:id>/", FachschaftUserDetail.as_view(), name="fachschaftuser-detail"),
    path("kontaktdaten/<int:id>/", KontaktdatenListByFachschaftUser.as_view(), name="kontaktdaten-detail"),
    path("user/<int:id>/", UserDetail.as_view(), name="user-detail"),
])
