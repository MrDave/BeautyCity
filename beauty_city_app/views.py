from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from beauty_city_app.models import Appointment
from django.utils import timezone
from django.db.models import Count

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from beauty_city_app.models import Appointment, Service, Shop, Specialist, Client


def index(request):
    # Пример значений для заполнения шаблона

    shops = Shop.objects.all()
    services = Service.objects.all()
    specialists = Specialist.objects.annotate(review_count=Count('reviews'))

    context = {
        'shops': shops,
        'services': services,
        'specialists': specialists,
        'reviews': [
            {
                'name': 'Светлана Г.',
                'text': 'Отличное место для красоты, очень доброжелательный и отзывчивый персонал, девочки заботливые, аккуратные и большие профессионалы. Посещаю салон с самого начала, но он не теряет своей привлекательности, как в обслуживании.',
                'date': '12 ноября 2022',
            } if i % 2 else
            {
                'name': 'Ольга Н.',
                'text': 'Мне всё лень было отзыв писать, но вот "руки дошли". Несколько раз здесь стриглась, мастера звали, кажется, Катя. Все было отлично, приятная молодая женщина и по стрижке вопросов не было)',
                'date': '5 ноября 2022',
            }
            for i in range(8)
        ]
    }
    return render(request, 'index.html', context)


def service(request):
    shops = [(pk, f'{name} {address}') for pk, name, address
             in Shop.objects.values_list('pk', 'name', 'address')]
    shops.insert(0, ('0', 'Любой салон'))
    # Заглушка для выбора таймслотов
    context = {
        'shops': shops,
        'timeslots': {
            'morning': [
                '10:00', '10:30',
            ],
            'day': [
                '12:00', '12:30', '15:00', '16:30',
            ],
            'evening': [
                '17:00', '18:30', '19:00',
            ]
        }
    }
    return render(request, 'service.html', context)


def service_final(request):
    shops_queryset = Shop.objects.values('pk', 'name', 'address', )
    shop = get_object_or_404(shops_queryset, pk=request.GET.get('shop'))
    services_queryset = Service.objects.values('pk', 'name', 'price', )
    service = get_object_or_404(services_queryset,
                                pk=request.GET.get('service'))
    # Пример значений для заполнения шаблона
    context = {
        'id': '?????',
        'shop': shop,
        'service': service,
        'timeslot': {
            'time': '16:30', 'date': '18 ноября',
        },
        'specialist': {
            'name': 'Елена Грибнова',
            'photo': '/static/img/masters/avatar/vizajist1.svg'
        }
    }
    print(context)
    return render(request, 'serviceFinally.html', context)


def notes(request):
    current_datetime = timezone.now()
    username = request.GET.get('username')
    phone = request.GET.get('phone')

    client = get_object_or_404(Client, name=username, phone=phone)

    all_appointments = client.appointments.all()
    total_paid_amount = all_appointments.filter(is_paid=False).aggregate(Sum('price'))['price__sum'] or 0

    upcoming_appointments = client.appointments.filter(
        time_slot__date__gte=current_datetime.date()
    ).order_by('time_slot__date', 'time_slot__time')

    past_appointments = client.appointments.filter(
        time_slot__date__lt=current_datetime.date()
    ).order_by('-time_slot__date', '-time_slot__time')

    context = {
        'client': client,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'total_paid_amount': total_paid_amount,
    }

    return render(request, 'notes.html', context)


@login_required
def manager(request):
    current_month = timezone.now().month
    current_year = timezone.now().year

    total_appointment = Appointment.objects.filter(time_slot__date__month=current_month).count()
    paid_appointment = Appointment.objects.filter(is_paid=True, time_slot__date__month=current_month).count()
    paid_price = Appointment.objects.filter(is_paid=True, time_slot__date__month=current_month).aggregate(Sum('price'))['price__sum']
    total_appointment_yearly = Appointment.objects.filter(time_slot__date__year=current_year).count()

    if not total_appointment:
        total_appointment = 0
    if not paid_appointment:
        paid_appointment = 0
    if not paid_price:
        paid_price = 0
    if not total_appointment_yearly:
        total_appointment_yearly = 0

    if total_appointment:
        paid_percentage = (paid_appointment / total_appointment) * 100
    else:
        paid_percentage = 0

    context = {
        'total_appointment': total_appointment,
        'paid_appointment': paid_appointment,
        'paid_percentage': paid_percentage,
        'paid_price': paid_price,
        'total_appointment_yearly': total_appointment_yearly,
    }

    return render(request, 'admin.html', context)
    
    
@api_view(['GET', 'POST,'])
def get_select_tag_payload(request):
    print(f'{request.GET=}')

    shop = request.GET.get('shop')
    if not shop:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    service_type = request.GET.get('service_type')
    if not service_type:
        return Response({'service_types':
                         list(map(list, Service.SERVICE_TYPES))})
    service = request.GET.get('service')
    if not service:
        return Response({'services':
                         list(map(list, Service.objects
                                  .filter(service_type=service_type)
                                  .values_list('pk', 'name')))})
    specialist = request.GET.get('specialist')
    if not specialist:
        return Response({
            'specialists': [{
                'pk': '4', 'name': 'Мария Максимова',
            }, {
                'pk': '5', 'name': 'Анастасия Сергеева',
            },]
        })
    return Response(status=status.HTTP_400_BAD_REQUEST)
