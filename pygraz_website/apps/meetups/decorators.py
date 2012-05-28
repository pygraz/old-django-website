from django.http import HttpResponseForbidden


def allow_only_staff_or_author_during_submission(method):
    def _func(self, request, *args, **kwargs):
        user = request.user
        self.kwargs = kwargs
        obj = self.get_object()
        if user.is_superuser or user.is_staff or obj.speaker is not None and user == obj.speaker:
            return method(self, request, *args, **kwargs)
        return HttpResponseForbidden()
    return _func
