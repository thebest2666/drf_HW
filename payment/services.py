import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY

def create_product(name):
    """
    Создание продукта
    """

    return stripe.Product.create(name=name)


def create_price(product_name, amount):
    """
    Создание цены на продукт
    """

    return stripe.Price.create(
      currency="rub",
      unit_amount=int(amount * 100),
      product_data={"name": product_name},
    )

def create_stripe_sessions(price):
    """
    Создание сессии на Stripe
    """

    return stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/',
        line_items=[
            {
                'price': price.get('id'),
                'quantity': 1,
            },
        ],
        mode='payment',
    )
