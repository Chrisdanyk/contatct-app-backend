from contact.views import ContactAPIView, GetUpdateDeleteContactView
from django.urls import path

urlpatterns = [
    path('', ContactAPIView.as_view(), name='contacts'),
    path('<int:id>', GetUpdateDeleteContactView.as_view(), name='contact'),
]
