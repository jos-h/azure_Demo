from rest_framework import routers

from app.views import UserViewSet

router = routers.SimpleRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = router.urls
