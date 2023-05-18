from django.core.management.base import BaseCommand
from django.db import transaction

from currencies.models import Currency
from currencies.vat_comply_api import VATComplyAPI


class Command(BaseCommand):
    help = "Fetches currencies from VATComply API and adds them to the database if not present"

    def handle(self, *args, **options):
        api = VATComplyAPI()
        response = api.get_currencies()

        if response is not None:
            with transaction.atomic():
                for currency in response:
                    Currency.objects.update_or_create(code=currency.code, defaults=currency.dict())

            self.stdout.write(self.style.SUCCESS("Currencies fetched and added successfully."))

        else:
            self.stdout.write(self.style.ERROR("Couldn't fetch currencies, please try again later."))
