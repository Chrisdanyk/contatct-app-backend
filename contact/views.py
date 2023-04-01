from rest_framework import generics, response, status, filters
from contact.models import Contact
from contact.serializers import ContactSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from helpers.pagination import CustomPageNumberPagination


class ContactAPIView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = [
        'id', 'first_name', 'last_name', 'phone_number', 'is_favourite']
    search_fields = [
        'id', 'last_name', 'last_name', 'phone_number', 'is_favourite']
    ordering_fields = [
        'id', 'last_name', 'last_name', 'phone_number', 'owner']
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        self.check_permissions(self.request)
        contact = serializer.save(owner=self.request.user)
        return contact

    def get_queryset(self):
        return super().get_queryset().select_related(
            'owner').filter(owner=self.request.user)


class GetUpdateDeleteContactView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        contact = Contact.objects.select_related('owner').filter(
            id=self.kwargs["id"], owner=self.request.user).first()
        if not contact:
            return response.Response(
                {
                    "error": "Contact not Found"
                    },
                status=status.HTTP_404_NOT_FOUND
                )
        if contact.owner is not self.request.user:
            return PermissionDenied()
        serializer = ContactSerializer(contact)
        return response.Response(
            {"message": "success",
             "data": serializer.data},
            status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        contact = Contact.objects.select_related('owner').filter(
            id=self.kwargs["id"], owner=self.request.user).first()
        if not contact:
            return response.Response(
                {
                    "error": "Contact not Found"
                    },
                status=status.HTTP_404_NOT_FOUND
                )
        if contact.owner is not self.request.user:
            return PermissionDenied()
        contact.delete()
        return response.Response({"message": "Contact deleted successfuly"},
                                 status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = Contact.objects.select_related('owner').filter(
            id=self.kwargs["id"], owner=self.request.user).first()
        if instance.owner is not self.request.user:
            return PermissionDenied()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(
            {
                "message": "Contact updated successfuly",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
