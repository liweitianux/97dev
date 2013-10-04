# -*- coding: utf-8 -*-

"""
A management command which deletes expired accounts (e.g.,
accounts which signed up but never activated) from the database.

Calls ``Account.objects.delete_expired_accounts()'',
which contains the actual logic for determining which
accounts are deleted.
"""

from django.core.management.base import NoArgsCommand

from accounts.models import Account


class Command(NoArgsCommand):
    help = "Delete expired accounts from the database"

    def handle_noargs(self, **options):
        Account.objects.delete_expired_accounts()

