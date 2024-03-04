from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


telefon_regex = RegexValidator(
    regex=r"^\+\d{9,15}$",
    message="Telefonnummer muss von folgendem Format sein: '+4938149444614'. "
    "Es sind bis zu 15 Ziffern erlaubt."
)


class Studienabschnitt(models.Model):
    """
    z.B. "1. Semester", "2. Semester", "Physikum", "STEX", "PJ", ...
    """
    bezeichnung = models.CharField(max_length=100)
    sortierung = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "Studienabschnitt/Semester"
        verbose_name_plural = "Studienabschnitte/Semester"
        ordering = ["sortierung"]


class Studiengang(models.Model):
    """
    z.B. "Humanmedizin", "Zahnmedizin", ...
    """
    bezeichnung = models.CharField(max_length=100, unique=True)
    studienabschnitt = models.ManyToManyField(
        Studienabschnitt,
        blank=True,
        related_name="studiengang"
    )

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "Studiengang"
        verbose_name_plural = "Studiengänge"
        ordering = ["bezeichnung"]


class Gender(models.Model):
    bezeichnung = models.CharField(max_length=100)
    # z.B. "in" für "weiblich" -> "Studentin"
    endung = models.CharField(
        max_length=8,
        blank=True,
    )

    def __str__(self):
        return self.bezeichnung

    class Meta:
        verbose_name = "Gender/Geschlecht"
        verbose_name_plural = "Gender/Geschlechter"
        ordering = ["bezeichnung"]


class FachschaftUser(models.Model):
    """
    Extends django.contrib.auth.models.User
    FachschaftUser = "Student:innen allgemein"
    """
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="fachschaftuser",
    )
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    studienabschnitt = models.ForeignKey(
        Studienabschnitt,
        on_delete=models.PROTECT,
    )
    studiengang = models.ForeignKey(
        Studiengang,
        on_delete=models.PROTECT,
    )
    nickname = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        """
        returns "[Vorname] [Nachname]"
        """
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Student:in"
        verbose_name_plural = "Student:innen"
        ordering = ["nickname"]


class Kontaktdaten(models.Model):
    """
    Die Kontaktdaten werden vom fachschaftUser ausgelagert, weil auch historische
    Kontaktdaten erfasst werden müssen. Wenn jemand die Kontaktdaten verifizieren
    lässt, dann ein Buch ausleiht und dann die Kontaktdaten ändert, dann weiß niemand
    mehr, wie das Buch wieder eingetrieben werden kann.
    """
    fachschaftuser = models.ForeignKey(
        FachschaftUser,
        on_delete=models.CASCADE,
        related_name="kontaktdaten",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="erzeugt",
    )
    """
    Die Adresse ist einfach nur ein Textfeld, weil es von Menschen manuell überprüft
    werden soll. Daher spalten wir das nicht extra auf.
    """
    adresse = models.TextField()
    telefonnummer = models.CharField(
        max_length=16,
        default="",
        validators=[telefon_regex],
        verbose_name="Telefonnummer",
        help_text=(
            "Telefonnummer muss von folgendem Format sein: '+4938149444614'. "
            "Es sind bis zu 15 Ziffern erlaubt."
        ),
    )
    gecheckt_von = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="überprüft von",
    )
    gecheckt_datum = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="überprüft am",
    )

    class Meta:
        verbose_name = "Kontaktdaten"
        verbose_name_plural = "Kontaktdaten"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.fachschaftuser} {self.created}"

    def ist_verifiziert(self):
        return all([self.gecheckt_von, self.gecheckt_datum])
