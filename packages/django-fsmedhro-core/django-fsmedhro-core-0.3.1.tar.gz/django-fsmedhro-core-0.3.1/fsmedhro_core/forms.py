from django.contrib.auth.models import User
from django import forms

from .models import (
    FachschaftUser,
    Kontaktdaten,
)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class FachschaftUserForm(forms.ModelForm):
    class Meta:
        model = FachschaftUser
        fields = [
            'nickname',
            'studiengang',
            'studienabschnitt',
            'gender',
        ]


class KontaktdatenForm(forms.ModelForm):
    class Meta:
        model = Kontaktdaten
        fields = [
            "fachschaftuser",
            "adresse",
            "telefonnummer",
        ]
        widgets = {
            "fachschaftuser": forms.HiddenInput(),
            "adresse": forms.Textarea(attrs={"rows": 3, "cols": 60}),
        }
