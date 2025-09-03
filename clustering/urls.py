from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our new viewsets with it.
router = DefaultRouter()
router.register(r"proposals", views.ClusterProposalViewSet, basename="proposal")
router.register(r"final-clusters", views.FinalClusterViewSet, basename="final-cluster")
router.register(
    r"defining-forces", views.DefiningForceViewSet, basename="defining-force"
)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
