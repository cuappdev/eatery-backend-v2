from django.urls import path
from eatery.views import EateryViewSet, EateryViewSetSimple

eateries_list = EateryViewSet.as_view({
    'get':'list',
    'post': 'create'
})

eatery_list = EateryViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy'
})

urlpatterns = [
    path("", eateries_list, name='eateries-list'),
    path("<int:pk>/", eatery_list, name='eatery-list'),
    path("simple/", EateryViewSetSimple.as_view({'get':'list'}), name='eateries-simple'),
]