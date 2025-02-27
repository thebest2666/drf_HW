from rest_framework import generics, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscribe
from materials.paginators import MaterialsPagination
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscribeSerializer
from users.permissions import IsModerator, IsAuthor


class CourseViewSet(ModelViewSet):
    """
    CRUD для курсов
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in 'update':
            permission_classes = [IsAdminUser | IsAuthor | IsModerator]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser | IsAuthor]
        elif self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(CreateAPIView):
    """
    Создание урока
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """
    Просмотр уроков
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Просмотр данных об уроке
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser | IsAuthor | IsModerator]


class LessonUpdateAPIView(UpdateAPIView):
    """
    Изменение данных об уроке
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser | IsAuthor | IsModerator]



class LessonDestroyAPIView(DestroyAPIView):
    """
    Удаление данных об уроке
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser | IsAuthor]


class SubscribeAPIView(generics.CreateAPIView):
    """
    Подписка на курс
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer

    def post(self,request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, id=course_id)
        check = Subscribe.objects.filter(user=user, course=course).exists()
        if check:
            Subscribe.objects.filter(user=user, course=course).delete()
            message = 'Подписка удалена'
            st = status.HTTP_204_NO_CONTENT
        else:
            Subscribe.objects.create(user=user, course=course)
            message = 'Подписка создана'
            st = status.HTTP_201_CREATED
        return Response({'message': message}, status=st)
