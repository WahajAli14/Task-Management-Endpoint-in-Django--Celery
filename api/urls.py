# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    CommentViewSet,
    DocumentViewSet,
    LogOutView,
    ProfileViewSet,
    ProjectViewSet,
    RegisterView,
    RunSampleTaskView,
    TaskViewSet,
)

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)
router.register(r"projects", ProjectViewSet)
router.register(r"tasks", TaskViewSet)
router.register(r"documents", DocumentViewSet)
router.register(r"comments", CommentViewSet)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("run-task/", RunSampleTaskView.as_view(), name="run_task"),
    path("", include(router.urls)),
]
