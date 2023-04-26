from django.shortcuts import render
from django.views.generic import View, ListView
from django.views.generic.edit import ModelFormMixin

from core.models import File, Lines

from core.process import Process

# Create your views here.


class LinesView(ListView):
    model = Lines
    template_name = 'index.html'

class SaveFileView(ModelFormMixin, View):
    model = File
    fields = ['file']
    template_name = 'import_file.html'
    
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            instance = form.save()
            Process(instance).main()
            return render(request, 'sucesso.html')
        else:
            return render(request, self.template_name, {'form': form})