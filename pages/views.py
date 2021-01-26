from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from stocks.models import Portfolio, Position

# Create your views here.
class HomePage(TemplateView):
    template_name = 'home.html'

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        data = Position.objects.filter(portfolio__owner=user)
        sum = 0
        for position in data:
            sum += float(position.display_market_value())
        context["portfolios"] = Portfolio.objects.filter(owner=user).order_by('name')
        context["positions"] = data
        context["total"] = int(round(sum,0))
        return context
    
    