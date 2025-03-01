from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson, Subscribe
from materials.validators import NoLinkValidator


class CourseSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            return obj.subscribes.filter(user=request.user).exists()

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [NoLinkValidator()]

class CourseDetailSerializer(ModelSerializer):

    number_of_lessons_in_the_course = SerializerMethodField()
    lessons = LessonSerializer(many=True)

    def get_number_of_lessons_in_the_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('title', 'description', 'number_of_lessons_in_the_course', 'lessons')


class SubscribeSerializer(ModelSerializer):
    """
    Сериализатор для подписок
    """
    class Meta:
        model = Subscribe
        fields = '__all__'
