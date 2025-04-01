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
    


    # def post (self,request):
    #     employee = request.user
    #     task_id = request.get('id')
    #     print(f'task_id {task_id}')
    #     tasks = Task.objects.filter(id=task_id,assigned_to=employee)
        
        
    #     print(f"TaskEmployee POST method user :{employee} and task status is {tasks.status}")
    #     data = request.data
    #     print(f"status posted {employee} : {data}")
    #     serializer = TaskSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()

    #     Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
    def post(self, request):
        manager = request.user  # Get authenticated user
        print(manager)
        if manager.role != "manager":  # Ensure user is a manager
            return Response(
                {"error": "Only managers can assign tasks."},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data
        
        assigned_to_id = data.get("assigned_to")  # Employee ID
        task_title = data.get("title")

        if not assigned_to_id or not task_title:
            return Response(
                {"error": "Missing required fields: 'assigned_to' and 'title'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            assigned_to = get_user_model().objects.get(id=assigned_to_id)  # Get employee
            if assigned_to.role != "employee":  # Ensure assigned user is an employee
                return Response(
                    {"error": "Task can only be assigned to employees."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except get_user_model().DoesNotExist:
            return Response(
                {"error": "Assigned employee not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize and save task
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            
            serializer.save(assigned_to=assigned_to,created_by=manager)  # Assign task to employee
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

