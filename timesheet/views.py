from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView 
from .models import TimesheetModel
from django.contrib.auth.mixins import (
    LoginRequiredMixin, # To restrict view access to only logged in users
    UserPassesTestMixin # To restrict access
)


class TimesheetListView(LoginRequiredMixin, ListView):
    template_name = 'timesheet/overview_timesheet.html'
    model = TimesheetModel
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super(TimesheetListView, self).get_queryset()
        return super(TimesheetListView, self).get_queryset().filter(author=self.request.user)


# Creating an article using 'article_new.html'
class TimesheetCreateView(LoginRequiredMixin, CreateView): 
    model = TimesheetModel
    template_name = 'timesheet/create.html'
    fields = ('hours', 'description',)
    
    # set current author automatically
    def form_valid(self, form): 
        form.instance.author = self.request.user
        return super().form_valid(form)