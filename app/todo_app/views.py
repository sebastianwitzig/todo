from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from todo_app.models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        exclude = ['user', ]


class OwnerMixin(object):
    def get_queryset(self):
        user = self.request.user
        queryset = super(OwnerMixin, self).get_queryset()
        return queryset.filter(
            user=user,
        )


class ToDoViewSet(OwnerMixin, viewsets.ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer: serializers.Serializer):
        serializer.save(user=self.request.user)
