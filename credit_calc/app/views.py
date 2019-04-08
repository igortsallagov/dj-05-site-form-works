from django.views.generic import TemplateView
from django.shortcuts import render

from .forms import CalcForm


class CalcView(TemplateView):
    template_name = "app/calc.html"

    def get(self, request, *args, **kwargs):
        form = CalcForm(self.request.GET)
        if form.is_valid():
            initial_fee = int(self.request.GET.get('initial_fee'))
            rate = float(self.request.GET.get('rate'))
            months_count = int(self.request.GET.get('months_count'))
            total = round(initial_fee * (1 + rate * months_count / 1200))
            monthly_payment = round(initial_fee/months_count + initial_fee * rate / 100 / 12, 2)
            return render(request, self.template_name,
                          {'form': form, 'total': total, 'monthly_payment': monthly_payment})
        else:
            return render(request, self.template_name, {'form': form})
