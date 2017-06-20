from django.shortcuts import render
from django.views import View
# Create your views here.


class SchemeQueryView(View):

    """
    宣传方案查询
    """

    def get(self, request):
        return render(request, 'Scheme_query.html', {})

