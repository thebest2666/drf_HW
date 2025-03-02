from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
from payment.serializers import PaymentSerializer
from payment.services import create_product, create_price, create_stripe_sessions


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_lesson', 'paid_course', 'payment_type',)
    ordering_fields = ('date',)


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(users=self.request.user)
        if serializer.instance.course:
            name = serializer.instance.course.title
        else:
            name = serializer.instance.lesson.title
        strike_product = create_product(name)
        price = serializer.instance.cost
        price_id = create_price(strike_product.id, name, price)
        session = create_stripe_sessions(price_id.id)
        serializer.instance.session_id = session.id
        serializer.instance.payment_link = session.url
        serializer.save()