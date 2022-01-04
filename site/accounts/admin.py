"""Registers accounts related models to the admin page."""

from django.contrib import admin
from . import models

# @admin.register(models.CommPrefs)
# class CommPrefsAdmin(admin.ModelAdmin):
#     """Admin page setup for the ``CommsPref`` table."""
#     list_display = ('id', 'user', 'blogs', 'newsletters', 'terms_last_agreed')
#     list_display_link = ('id',)
#     filter_by = ('blogs', 'newsletters', 'terms_last_agreed')
