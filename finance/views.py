from django.views.generic import CreateView, TemplateView


class ProjectionView(TemplateView, CreateView):
    template_name = 'finance/projection.html'

