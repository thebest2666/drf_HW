import json

from django.core.management import BaseCommand

from config.settings import BASE_DIR
from payment.serializers import PaymentSerializer



class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(BASE_DIR / 'default_data/payment_data.json') as file:
            data = json.load(file)
        payment = data['payment']

        for i in payment:
            serialize = PaymentSerializer(data=i)
            if serialize.is_valid(raise_exception=True):
                serialize.save()
            else:
                print(f"Payment #{i['id']} not saved")