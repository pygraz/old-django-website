from django.views.generic import TemplateView

from . import contents


class MyContentsView(TemplateView):
    """
    This view renders all custom content created or editable by the current
    user.
    """

    template_name = "accounts/my_contents.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["contents"] = [c for c in contents.get_all(self.request, self.request.user) if c.has_content]
        return data
