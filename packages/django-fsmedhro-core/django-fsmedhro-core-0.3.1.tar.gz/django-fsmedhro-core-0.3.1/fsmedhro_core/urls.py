from django.urls import path, include
from . import views, api

app_name = 'fsmedhro_core'

urlpatterns = [
    path('edit/', views.FachschaftUserEdit.as_view(), name='edit'),
    path('api/', include(api)),
    path(
        'kontaktdaten/add/',
        views.KontaktdatenAdd.as_view(),
        name='kontaktdaten_add',
    ),
    path(
        'kontaktdaten/verify/',
        views.KontaktdatenVerify.as_view(),
        name='kontaktdaten_verify',
    ),
    path('kontaktdaten/', views.KontaktdatenList.as_view(), name='kontaktdaten_list'),
    path('', views.FachschaftUserDetail.as_view(), name='detail'),
]
