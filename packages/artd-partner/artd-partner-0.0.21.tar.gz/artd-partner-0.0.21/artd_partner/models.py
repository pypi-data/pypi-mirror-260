from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from artd_location.models import City


class PartnerBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField("status", default=True)

    class Meta:
        abstract = True


class Partner(PartnerBaseModel):
    """Model definition for Partner."""

    partner_slug = models.SlugField(
        _("Slug"),
        help_text=_("Slug of headquarter"),
        max_length=150,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Name of partner"),
        max_length=150,
    )
    dni = models.CharField(
        _("Dni"),
        help_text=_("DNI of partner"),
        max_length=20,
    )
    email = models.EmailField(
        _("Email"),
        help_text=_("Email of partner"),
        max_length=254,
    )
    city = models.ForeignKey(
        City,
        verbose_name=_("City"),
        help_text=_("City of partner"),
        on_delete=models.CASCADE,
    )
    address = models.CharField(
        _("Address"),
        help_text=_("Address of partner"),
        max_length=250,
    )

    class Meta:
        """Meta definition for Partner."""

        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    def __str__(self):
        """Unicode representation of Partner."""
        return self.name


class Headquarter(PartnerBaseModel):
    """Model definition for Headquarter."""

    name = models.CharField(
        _("Name"),
        help_text=_("Name of headquarter"),
        max_length=150,
    )
    address = models.CharField(
        _("Address"),
        help_text=_("Address of headquarter"),
        max_length=250,
    )
    city = models.ForeignKey(
        City,
        verbose_name=_("City"),
        help_text=_("City of headquarter"),
        on_delete=models.CASCADE,
    )
    phone = models.CharField(
        _("phone"),
        help_text=_("Phone of headquarter"),
        max_length=20,
    )
    partner = models.ForeignKey(
        Partner,
        verbose_name=_("partner"),
        help_text=_("Partner of headquarter"),
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta definition for Headquarter."""

        verbose_name = _("Headquarter")
        verbose_name_plural = _("Headquarters")

    def __str__(self):
        """Unicode representation of Headquarter."""
        return self.name


class Position(PartnerBaseModel):
    """Model definition for Position."""

    name = models.CharField(
        _("Name"),
        help_text=_("Name of position"),
        max_length=150,
    )

    class Meta:
        """Meta definition for Position."""

        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

    def __str__(self):
        """Unicode representation of Position."""
        return self.name


class Coworker(PartnerBaseModel):
    """Model definition for Coworker."""

    first_name = models.CharField(
        _("First name"),
        help_text=_("First name of coworker"),
        max_length=150,
    )
    last_name = models.CharField(
        _("Last name"),
        help_text=_("Last name of coworker"),
        max_length=150,
    )
    dni = models.CharField(
        _("Dni"),
        help_text=_("DNI of coworker"),
        max_length=20,
    )
    email = models.EmailField(
        _("email"),
        help_text=_("Email of coworker"),
        max_length=254,
    )
    phone = models.CharField(
        _("Phone"),
        help_text=_("Phone of coworker"),
        max_length=20,
    )
    headquarter = models.ForeignKey(
        Headquarter,
        verbose_name=_("Headquarter"),
        help_text=_("Headquarter of coworker"),
        on_delete=models.CASCADE,
    )
    position = models.ForeignKey(
        Position,
        verbose_name=_("Position"),
        help_text=_("Position of coworker"),
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta definition for Coworker."""

        verbose_name = _("Coworker")
        verbose_name_plural = _("Coworkers")

    def __str__(self):
        """Unicode representation of Coworker."""
        return self.first_name + " " + self.last_name
