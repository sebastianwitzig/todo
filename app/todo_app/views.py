from rest_framework import serializers, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters

from todo_app.models import ToDo
from todo_app.enumerations import Status


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        exclude = ['user', ]


class TodoFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', method='filter_search')
    description = filters.CharFilter(
            field_name='description', method='filter_search')
    due_date = filters.DateFilter(field_name='due_date')
    state = filters.ChoiceFilter(
            field_name='state', choices=Status.get_tuple())

    def filter_search(self, queryset: 'QuerySet', name, value) -> 'QuerySet':
        search_filter = {f'{name}__icontains': value}
        return queryset.filter(**search_filter)


class OwnerMixin(object):
    def get_queryset(self) -> 'QuerySet':
        user = self.request.user
        queryset = super(OwnerMixin, self).get_queryset()
        return queryset.filter(
            user=user,
        )


class ToDoViewSet(OwnerMixin, viewsets.ModelViewSet):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = TodoFilter
    ordering_fields = '__all__'

    def perform_create(self, serializer: serializers.Serializer):
        serializer.save(user=self.request.user)
