from django.views.generic import ListView, TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'
