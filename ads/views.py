from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from ads.models import Ad, Review
from ads.serializers import AdSerializer, ReviewSerializer


class AdListAPIView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdRetrieveAPIView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdCreateAPIView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def perform_create(self, serializer):
        ad = serializer.save()
        ad.author = self.request.user
        ad.save()


class AdUpdateAPIVIew(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdDestroyAPIView(DestroyAPIView):
    queryset = Ad.objects.all()


class ReviewListAPIVIew(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewRetrieveAPIView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        review = serializer.save()
        review.author = self.request.user
        review.save()


class ReviewUpdateAPIView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDestroyAPIView(DestroyAPIView):
    queryset = Review.objects.all()
