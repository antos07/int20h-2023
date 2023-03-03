from django.views.generic import TemplateView


class HelloWorldView(TemplateView):
    template_name = 'test_app/hello_world.html'
