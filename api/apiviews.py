from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import *

class CourseListAPI(APIView):

    def get(self, request):
        queryset = Course.objects.all()
        print(queryset)
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)