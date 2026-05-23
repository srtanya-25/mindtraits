"""
api/urls.py — single aggregator for /api/v1/* endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from accounts.views import (
    RegisterView, LoginView, LogoutView, RefreshView, MeView,
)

# ViewSet routing (DefaultRouter) 
router = DefaultRouter()
router.register("responses", views.UserResponseViewSet, basename="responses")

urlpatterns = [
    # Authentication (HTTP-only cookie JWT)
    path("register/", RegisterView.as_view(), name="register"),
    path("login/",    LoginView.as_view(),    name="login"),
    path("logout/",   LogoutView.as_view(),   name="logout"),
    path("refresh/",  RefreshView.as_view(),  name="refresh"),
    path("me/",       MeView.as_view(),       name="me"),

    # SimpleJWT built-in views (bearer-token flow — useful for Postman)
    path("token/",         TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(),    name="token_refresh"),

    # Auth check (used by AuthProvider on app load)
    path("dashboard-protected/", views.DashboardProtectedView.as_view(), name="dashboard-protected"),

    # Questions (function-based + generic class-based) 
    path("questions/",          views.QuestionListView.as_view(), name="questions"),
    path("questions-fn/",       views.questions_api_view,         name="questions-fn"),
    path("questions/<int:pk>/", views.question_detail,            name="question-detail"),

    # Responses
    # NOTE: the explicit submit route MUST come before the router include,
    # otherwise the router's responses/<pk>/ detail route captures
    # responses/submit/ (pk="submit") and rejects POST with 405.
    path("responses/submit/", views.SubmitResponsesView.as_view(), name="submit-responses"),
    path("", include(router.urls)),

    #  ML pipeline + results
    path("analyze/", views.AnalyzeView.as_view(),               name="analyze"),
    path("result/",  views.LatestResultView.as_view(),          name="latest-result"),
    path("results/", views.PersonalityResultListView.as_view(), name="result-history"),
]
