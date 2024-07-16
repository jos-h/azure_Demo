import logging

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.serializers import UserSerializer

logger = logging.getLogger("azure_logger")

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            user = User.objects.filter(email=data["email"]).first()
            if user:
                logger.debug(f"User with email {data['email']} already exists!!!")
                return Response(
                    {"message": f"User with email {data['email']} already exists!!!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info(f"User with email {data['email']} created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.debug(msg=str(e))
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
