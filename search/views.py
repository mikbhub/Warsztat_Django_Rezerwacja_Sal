from django.shortcuts import HttpResponse, reverse, render
from django.views.decorators.csrf import csrf_exempt
from django.views import View, generic
from django.utils.decorators import method_decorator
from rezerwacje.models import Auditorium


class SearchAvaliableAuditoriums(View):

    def get(self, request):
        return render(request, 'search/search-form.html')


class ShowSearchResults(View):

    def get(self, request):

        # build database query using GET params:
        filter_params = dict()
        exclude_params = dict()

        if 'date' in request.GET and request.GET['date'] != '':
            exclude_params['reservations__date'] = request.GET['date']

        if 'capacity' in request.GET and request.GET['capacity'] != '':
            filter_params['capacity__gte'] = request.GET['capacity']

        if 'projector' in request.GET and request.GET['projector'] != '':
            filter_params['projector'] = request.GET['projector']

        auditoriums = Auditorium.objects.exclude(**exclude_params).filter(**filter_params).order_by('capacity')

        context = {'auditoriums': auditoriums}

        return render(request, 'search/results.html', context)

        # if len(auditoriums) == 0:
        #     return HttpResponse('Brak wolnych sal dla podanych kryteriów wyszukiwania')
        # else:
        #     auditoriums = '<br>'.join('{name}, Capacity: {capacity}. {reservation_link}'.format(
        #             name=auditorium.name,
        #             capacity=auditorium.capacity,
        #             reservation_link='<a href="{}">Reserve</a>'.format(reverse('reserve', kwargs={'id_':auditorium.pk}))
        #         ) for auditorium in auditoriums)
        #     return HttpResponse(
        #         f"""
        #         Available auditoriums:<br>
        #         {auditoriums}
        #         """
        #     )
