import logging

from datetime import datetime

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail, EmailMessage
from django.forms.models import model_to_dict
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .forms import FachschaftUserForm, KontaktdatenForm
from .models import Studienabschnitt, Studiengang, Gender, FachschaftUser, Kontaktdaten


logger = logging.getLogger(__name__)


class FachschaftUserEdit(LoginRequiredMixin, View):
    template_name = "fsmedhro_core/user_edit.html"
    form_class = FachschaftUserForm

    def get(self, request):
        # FachschaftUser bereits vorhanden?
        if hasattr(request.user, 'fachschaftuser'):
            fu_form = self.form_class(instance=request.user.fachschaftuser)
        else:
            fu_form = self.form_class()

        context = {
            "fu_form": fu_form,
            "next": request.GET.get(REDIRECT_FIELD_NAME, ""),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        if hasattr(request.user, 'fachschaftuser'):
            fu_form = self.form_class(
                data=request.POST,
                instance=request.user.fachschaftuser,
            )
        else:
            fu_form = self.form_class(
                data=request.POST,
            )

        if fu_form.is_valid():
            fachschaftuser = fu_form.save(commit=False)
            fachschaftuser.user = request.user
            fachschaftuser.save()

            # TODO: redirect zu next, falls vorhanden

            return redirect("fsmedhro_core:detail")
        else:
            context = {
                "fu_form": fu_form,
            }
            return render(request, self.template_name, context)


class FachschaftUserDetail(LoginRequiredMixin, View):
    template_name = "fsmedhro_core/user_detail.html"

    def get(self, request):
        if not hasattr(request.user, 'fachschaftuser'):
            return redirect("fsmedhro_core:edit")

        fachschaftuser = request.user.fachschaftuser

        context = {
            "fachschaftuser": fachschaftuser,
            "aktuelle_kontaktdaten": fachschaftuser.kontaktdaten.first(),
            "kontaktdaten": fachschaftuser.kontaktdaten.all(),
        }

        return render(request, self.template_name, context)


class KontaktdatenList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = Kontaktdaten.objects.select_related('fachschaftuser__user').filter(gecheckt_von=None)
    context_object_name = 'kontaktdaten'
    template_name = 'fsmedhro_core/kontaktdaten_list.html'

    def test_func(self):
        return self.request.user.has_perm('fsmedhro_core.change_kontaktdaten')


class KontaktdatenVerify(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.has_perm('fsmedhro_core.change_kontaktdaten')

    def post(self, request):
        print(request.POST)
        k_id = request.POST.get('kontaktdaten_id', None)
        k = get_object_or_404(Kontaktdaten, pk=k_id)

        k.gecheckt_von = request.user
        k.gecheckt_datum = datetime.now()
        k.save()

        return redirect('fsmedhro_core:kontaktdaten_list')


class KontaktdatenAdd(LoginRequiredMixin, View):
    template_name = "fsmedhro_core/kontaktdaten_add.html"
    form_class = KontaktdatenForm

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'fachschaftuser'):
            return redirect("fsmedhro_core:edit")
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            "kontaktdaten_form": self.form_class(),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        kontaktdaten_form = self.form_class(data=request.POST)

        if kontaktdaten_form.is_valid():
            kontaktdaten = kontaktdaten_form.save(commit=False)
            kontaktdaten.save()

            return redirect("fsmedhro_core:detail")
        else:
            context = {
                "kontaktdaten_form": kontaktdaten_form,
            }

            return render(request, self.template_name, context)


class Rundmail(UserPassesTestMixin, View):
    template_name = "fsmedhro_core/rundmail.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self):
        context = {
            "studienabschnitte": Studienabschnitt.objects.all(),
            "studiengaenge": Studiengang.objects.all(),
            "gender": Gender.objects.all(),
        }
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        context = self.get_context_data()
        errors = []

        studiengaenge = list(map(int, request.POST.getlist("studiengang", [])))
        context["gew_studiengaenge"] = studiengaenge
        if not studiengaenge:
            errors.append("Es wurde kein Studiengang ausgewählt.")

        studienabschnitte = list(map(int, request.POST.getlist("studienabschnitt", [])))
        context["gew_studienabschnitte"] = studienabschnitte
        if not studienabschnitte:
            errors.append("Es wurde kein Studienabschnitt ausgewählt.")

        gender = list(map(int, request.POST.getlist("gender", [])))
        context["gew_gender"] = gender
        if not gender:
            errors.append("Es wurde kein Geschlecht ausgewählt.")

        betreff = request.POST.get("email_subject", "")
        context["betreff"] = betreff
        if not betreff:
            errors.append("Der Betreff fehlt.")

        text = request.POST.get("email_text", "")
        context["text"] = text
        if not text:
            errors.append("Der Text fehlt.")

        send_testmail = bool(request.POST.get("send_testmail", False))

        if errors:
            context["errors"] = errors
            return render(request, "fsmedhro_core/rundmail.html", context)
        elif send_testmail:
            anzahl_verschickt = send_mail(
                subject=betreff,
                message=text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            logger.info(
                f"{request.user} verschickte Testmail\n" +
                f"{betreff=}\n" +
                f"{text=}"
            )
            context["testmail_verschickt"] = True
            context["anzahl_verschickt"] = anzahl_verschickt

            return render(request, self.template_name, context)
        else:
            empfaenger = FachschaftUser.objects.filter(
                studiengang__in=studiengaenge,
                studienabschnitt__in=studienabschnitte,
                gender__in=gender,
            ).order_by("user__email")
            empfaenger_adressen = [empf.user.email for empf in empfaenger]

            mails = EmailMessage(
                subject=betreff,
                body=text,
                bcc=empfaenger_adressen,
            )

            mails.send()
            logger.info(
                f"{request.user} verschickte Rundmail\n" +
                f"{betreff=}\n" +
                f"{text=}\n" +
                f"an" +
                ", ".join(empfaenger_adressen)
            )

            context["anzahl_verschickt"] = len(empfaenger)

            sicherheitsnachricht = (
                f"Die folgende Nachricht:\n\n" +
                f"Betreff: {betreff}\n" +
                f"Text:\n" +
                f"{text}\n\n" +
                f"wurde von {request.user} "
                f"an {len(empfaenger)} Personen verschickt:\n\n" +
                "\n".join(empfaenger_adressen)
            )
            send_mail(
                subject="Rundmail verschickt: " + betreff,
                message=sicherheitsnachricht,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            return render(request, self.template_name, context)
