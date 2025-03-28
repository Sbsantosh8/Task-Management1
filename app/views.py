from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdminOrManager, IsTaskOwnerOrManager
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def llist(self, request, *args, **kwargs):
        print(f"User: {request.user}")  # Check if user is authenticated
        print(f"Role: {getattr(request.user, 'role', None)}")  # Check if role exists
        return super().list(request, *args, **kwargs)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsTaskOwnerOrManager


# class TaskEmployeeView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated, IsTaskOwnerOrManager]

#     def get(self, request):
#         # Fetch tasks assigned to the authenticated user
#         tasks = Task.objects.filter(assigned_to=request.user)

#         # Serialize tasks
#         serializer = TaskSerializer(tasks, many=True)

#         # Return response with serialized data
#         return Response(serializer.data, status=status.HTTP_200_OK)


from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class CustomTokenObtainPairView(TokenObtainPairView):
    serializers_class = CustomTokenObtainPairSerializer


from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsTaskOwnerOrManager


class TaskEmployeeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsTaskOwnerOrManager]

    def get(self, request):
        employee = request.user  # Get logged-in user
        print(f"TaskEmployeeView ..... [user :{employee} ]")

        # Fetch only tasks assigned to this employee
        tasks = Task.objects.filter(assigned_to=employee)

        # Serialize tasks
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


    def post (self,request):
        employee = request.user
        task_id = request.get('id')
        print(f'task_id {task_id}')
        tasks = Task.objects.filter(id=task_id,assigned_to=employee)
        
        
        print(f"TaskEmployee POST method user :{employee} and task status is {tasks.status}")
        data = request.data
        print(f"status posted {employee} : {data}")
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        Response(serializer.data,status=status.HTTP_201_CREATED)

        

