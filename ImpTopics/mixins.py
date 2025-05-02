# mixins.py
from django.shortcuts import get_object_or_404

class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):
                filter_kwargs[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
