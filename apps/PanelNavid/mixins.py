from django.http import Http404


class IsAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404

    