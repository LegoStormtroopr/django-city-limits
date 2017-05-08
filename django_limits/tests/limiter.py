from django.db.models import Q
from django_limits.limiter import Limiter
from .models import Horse, House, Motorcycle, Liquor, Ration


class NutbushLimiter(Limiter):
    rules = {
        House: [
            {
                'limit': 4,
                'message': "A church house gin house, a school house out house"
            },
            {
                'limit': 0,
                'message': "A church house gin house, a school house out house",
                'filterset': ~Q(name__in=['church', 'gin', 'school', 'out'])
            },
        ],
        Motorcycle: {
            'limit': 0,
            'message': "Twenty-five was the speed limit, motorcycle not allowed in it"
        },
        Liquor: {
            'limit': 0,
            'message': "No whiskey for sale, you can't cop no bail",
            'filterset': Q(name='Whiskey')
        },
        Ration: [
            {
                'limit': 2,
                'message': "Salt pork and molasses is all you get in jail",
                'filterset': Q(name='Salt pork') | Q(name='Molasses')
            },
            {
                'limit': 0,
                'message': "Salt pork and molasses is all you get in jail",
                'filterset': ~(Q(name='Salt pork') | Q(name='Molasses'))
            },
        ],
        Horse: {
            'limit': 1,
            'message': "One horse town you have to watch"
        }
    }

    def get_filterset(self, rule):
        base = super(NutbushLimiter, self).get_filterset(rule)
        if base:
            return Q(base & Q(city__name='Nutbush'))
        else:
            return Q(city__name='Nutbush')
