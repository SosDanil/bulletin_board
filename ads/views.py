from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from ads.models import Ad, Review
from ads.pagination import AdsPagination
from ads.serializers import AdSerializer, ReviewSerializer
from users.permissions import IsAuthor, IsAdministrator

DENIED_MESSAGE = 'Только автор или администратор может работать с объектом'


class AdListAPIView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title',)
    pagination_class = AdsPagination
    permission_classes = (AllowAny,)


class AdRetrieveAPIView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,)


class AdCreateAPIView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        ad = serializer.save()
        ad.author = self.request.user
        ad.save()


class AdUpdateAPIVIew(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsAuthor | IsAdministrator, IsAuthenticated)

    def permission_denied(self, request, message=DENIED_MESSAGE, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=DENIED_MESSAGE)


class AdDestroyAPIView(DestroyAPIView):
    queryset = Ad.objects.all()
    permission_classes = (IsAuthor | IsAdministrator, IsAuthenticated)

    def permission_denied(self, request, message=DENIED_MESSAGE, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=DENIED_MESSAGE)


class ReviewListAPIVIew(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)


class ReviewRetrieveAPIView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthor | IsAdministrator, IsAuthenticated)

    def permission_denied(self, request, message=DENIED_MESSAGE, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=DENIED_MESSAGE)


class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        review = serializer.save()
        review.author = self.request.user
        review.save()


class ReviewUpdateAPIView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthor | IsAdministrator, IsAuthenticated)

    def permission_denied(self, request, message=DENIED_MESSAGE, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=DENIED_MESSAGE)


class ReviewDestroyAPIView(DestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = (IsAuthor | IsAdministrator, IsAuthenticated)

    def permission_denied(self, request, message=DENIED_MESSAGE, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=DENIED_MESSAGE)
