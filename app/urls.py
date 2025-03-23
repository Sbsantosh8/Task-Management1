from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CustomTokenObtainPairView
from .views import TaskEmployeeView
from rest_framework.authtoken.views import obtain_auth_token  # DRF built-in token view


router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "api/login/", CustomTokenObtainPairView.as_view(), name="api_token_auth"
    ),  # Default DRF token endpoint
    path("tasks/assigned/", TaskEmployeeView.as_view(), name="task-by-employee"),
]
