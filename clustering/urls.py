from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router to automatically generate URLs for our ViewSets
router = DefaultRouter()

# Register each ViewSet with the router, defining its URL prefix
router.register(r"proposals", views.ClusterProposalViewSet, basename="proposal")
router.register(r"final-clusters", views.FinalClusterViewSet, basename="finalcluster")
router.register(
    r"defining-forces", views.DefiningForceViewSet, basename="definingforce"
)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
