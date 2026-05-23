"""
api/views.py
============
Aggregator views for MindTraits, written with DRF mixins / generics / viewsets
so the same endpoints can be served two ways:

  - Function-based view  (@api_view)        ->  for teaching / debugging
  - Class-based APIView                     ->  manual GET/POST handling
  - mixins.ListModelMixin etc.              ->  reusable behaviour
  - generics.ListCreateAPIView etc.         ->  one-liners
  - viewsets.ModelViewSet                   ->  full CRUD + DefaultRouter

The actual ML pipeline + auth-check endpoints stay as APIView (no model behind
them), but the Question / UserResponse / PersonalityResult resources are
exposed as proper REST resources here.
"""
from django.http import Http404
from rest_framework import status, mixins, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from personality.models import Question, UserResponse, PersonalityResult
from personality.serializers import (
    QuestionSerializer,
    UserResponseSerializer,
    PersonalityResultSerializer,
)
from personality.services import run_analysis_pipeline
from .paginations import QuestionPagination


# 1. Function-based view (kept for reference)
@api_view(["GET", "POST"])
def questions_api_view(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(QuestionSerializer(question).data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 2. Mixins + GenericAPIView (commented-out, kept for reference)
 
"""
class QuestionMixinView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    queryset = Question.objects.all()           # must be `queryset`
    serializer_class = QuestionSerializer       # must be `serializer_class`

    def get(self, request):
        return self.list(request)               # from ListModelMixin

    def post(self, request):
        return self.create(request)             # from CreateModelMixin
"""


# 3. Generics (concise — used in production)
class QuestionListView(generics.ListAPIView):
    """GET /api/v1/questions/ — paginated, filterable, searchable."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    pagination_class = QuestionPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["trait"]
    search_fields = ["text"]
    ordering_fields = ["order", "id", "trait"]


class PersonalityResultListView(generics.ListAPIView):
    """GET /api/v1/results/ — list current user's result history."""
    serializer_class = PersonalityResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PersonalityResult.objects.filter(user=self.request.user).order_by("-created_at")


class LatestResultView(generics.RetrieveAPIView):
    """GET /api/v1/result/ — latest result for the authenticated user."""
    serializer_class = PersonalityResultSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return PersonalityResult.objects.filter(user=self.request.user).latest("created_at")
        except PersonalityResult.DoesNotExist:
            raise Http404("No result found. Please complete the test.")


# 4. ViewSet + DefaultRouter
class UserResponseViewSet(viewsets.ModelViewSet):
    """
    Full CRUD on the current user's responses.
    Wired through a DefaultRouter in urls.py.
    """
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["question", "score"]
    ordering_fields = ["created_at", "score"]

    def get_queryset(self):
        return UserResponse.objects.filter(user=self.request.user)


# 5. Action endpoints (no model — kept as APIView)
class SubmitResponsesView(APIView):
    """POST /api/v1/responses/submit/ — bulk submit all answers + response times."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        responses_data = request.data.get("responses", [])
        if not responses_data:
            return Response({"error": "No responses provided."}, status=400)

        saved, errors = [], []
        for item in responses_data:
            serializer = UserResponseSerializer(data=item, context={"request": request})
            if serializer.is_valid():
                saved.append(serializer.save())
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"errors": errors}, status=400)

        return Response({"saved": len(saved), "message": "Responses saved successfully."})


class AnalyzeView(APIView):
    """POST /api/v1/analyze/ — run the full ML + insights pipeline."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            result = run_analysis_pipeline(request.user)
            return Response(PersonalityResultSerializer(result).data, status=200)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


class DashboardProtectedView(APIView):
    """GET /api/v1/dashboard-protected/ — auth check used by AuthProvider."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Welcome, {request.user.username}!",
            "user": {"id": request.user.id, "username": request.user.username},
        })
