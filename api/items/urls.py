from rest_framework.routers import DefaultRouter

from .views import ItemViewSet

router = DefaultRouter()

router.register(r"items", ItemViewSet, basename="items-api")


urlpatterns = router.urls
