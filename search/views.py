from django.shortcuts import render
from django.views import View, generic
from rezerwacje.models import Auditorium


class SearchAvaliableAuditoriums(View):

    def get(self, request):
        return render(request, 'search/search-form.html')


class ShowSearchResults(View):

    def database_query(self, request):
        # build database query using GET params:
        filter_params = dict()
        exclude_params = dict()
        if 'date' in request.GET and request.GET['date'] != '':
            exclude_params['reservations__date'] = request.GET['date']
        if 'capacity' in request.GET and request.GET['capacity'] != '':
            filter_params['capacity__gte'] = request.GET['capacity']
        if 'projector' in request.GET and request.GET['projector'] != '':
            filter_params['projector'] = request.GET['projector']
        return Auditorium.objects.exclude(**exclude_params).filter(**filter_params).order_by('capacity')

    def get(self, request):
        auditoriums = self.database_query(request)
        context = {'auditoriums': auditoriums}
        return render(request, 'search/results.html', context)
