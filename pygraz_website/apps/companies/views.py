from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import Http404

from guardian.shortcuts import assign_perm

from . import models
from . import forms
from . import emails


class ListCompaniesView(ListView):
    model = models.Company
    queryset = models.Company.objects.filter(approved=True)

    def get_context_data(self, **kwargs):
        data = super(ListCompaniesView, self).get_context_data(**kwargs)
        if hasattr(self.request, 'user') and self.request.user.is_authenticated():
            data['unapproved_companies'] = self.request.user.companies.filter(
                approved=False)
        return data


class CompanyDetailsView(DetailView):
    model = models.Company
    
    def get_context_data(self, **kwargs):
        data = super(CompanyDetailsView, self).get_context_data(**kwargs)
        # Make sure that the company is approved or editable by the current
        # user.
        data['approved'] = self.object.approved
        data['is_editor'] = self.request.user.has_perm('change_company', self.object)
        if not self.object.approved and not data['is_editor']:
            raise Http404("Company not found")
        return data


class SubmitCompanyView(CreateView):
    """
    Before a company appears on the website, it has to be approved by an admin.
    Hence this view only creates an unapproved company object.
    """
    model = models.Company
    form_class = forms.CompanySubmissionForm

    def form_valid(self, form):
        result = super(SubmitCompanyView, self).form_valid(form)
        self.object.editors.add(self.request.user)
        assign_perm('change_company', self.request.user, self.object)
        emails.notify_admins_for_approval(self.object)
        return result


class UpdateCompanyView(UpdateView):
    """
    An update view available to every "editor" or a company.
    """
    model = models.Company
    form_class = forms.CompanySubmissionForm

    def get_object(self, **kwargs):
        obj = super(UpdateCompanyView, self).get_object(**kwargs)
        if not self.request.user.has_perm('change_company', obj):
            raise Http404("Company not found")
        return obj
