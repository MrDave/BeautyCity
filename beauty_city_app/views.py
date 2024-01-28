from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from beauty_city_app.models import (Appointment, Service, Shop, Specialist,
                                    TimeSlot)


def index(request):
    # Пример значений для заполнения шаблона
    context = {
        'shops': [
            {
                'name': 'BeautyCity Пушкинская',
                'address': 'ул. Пушкинская, д. 78А',
                'photo': '/static/img/salons/salon1.svg',
                'works_at': 'с 10:00 до 20:00  без выходных',
            },
            {
                'name': 'BeautyCity Ленина',
                'address': 'ул. Ленина, д. 211',
                'photo': '/static/img/salons/salon2.svg',
                'works_at': 'с 10:00 до 20:00  без выходных',
            },
            {
                'name': 'BeautyCity Красная',
                'address': 'ул. Красная, д. 10',
                'photo': '/static/img/salons/salon3.svg',
                'works_at': 'с 10:00 до 20:00  без выходных',
            },
        ],
        'services': [
            {
                'name': 'Дневной макияж',
                'price': '1400',
                'photo': '/static/img/services/service1.svg',
            },
            {
                'name': 'Маникюр. Классический. Гель',
                'price': '2000',
                'photo': '/static/img/services/service2.svg',
            },
            {
                'name': 'Укладка волос',
                'price': '1500',
                'photo': '/static/img/services/service3.svg',
            },
            {
                'name': 'Укладка волос',
                'price': '3000',
                'photo': '/static/img/services/service4.svg',
            },
            {
                'name': 'Педикюр',
                'price': '1000',
                'photo': '/static/img/services/service5.svg',
            },
            {
                'name': 'Окрашивание волос',
                'price': '5000',
                'photo': '/static/img/services/service6.svg',
            },
        ],
        'specialists': [
            {
                'name': 'Елизавета Лапина',
                'reviews': 24,
                'services': 'Ногтевой сервис, Макияж',
                'experience': '3 г. 10 мес.',
                'photo': f'/static/img/masters/master{i}.svg',
            } for i in range(1, 7)
        ],
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
    service_types = list(map(list, Service.SERVICE_TYPES))
    # Заглушка для выбора таймслотов
    context = {
        'shops': shops,
        'service_types': service_types,
        'timeslots': {'morning': [], 'day': [], 'evening': [], },
    }
    return render(request, 'service.html', context)


def service_final(request):
    shop_id = request.GET.get('shop', '0')
    service_id = request.GET.get('service', '0')
    specialist_id = request.GET.get('specialist', '0')
    selected_date = request.GET.get('date', '')
    selected_time = request.GET.get('time', '')

    if shop_id == '0':
        shop = {'pk': '0', 'name': 'Любой салон', 'address': ''}
    else:
        shops_queryset = Shop.objects.values('pk', 'name', 'address', )
        shop = get_object_or_404(shops_queryset, pk=shop_id)
    services_queryset = Service.objects.values('pk', 'name', 'price', )
    service = get_object_or_404(services_queryset, pk=service_id)
    date_repr = '{:%d %b %Y}'.format(datetime
                                     .strptime(selected_date, '%Y-%m-%d'))
    if specialist_id == '0':
        specialist = {'pk': '0', 'name': 'Любой специалист', 
                      'photo': '/static/img/masters/avatar/all.svg', }
    else:
        specialist_queryset = Specialist.objects.values('pk', 'name',
                                                        'profile_picture', )
        specialist = get_object_or_404(specialist_queryset, pk=specialist_id)
    # Пример значений для заполнения шаблона
    context = {
        'id': '?????',
        'shop':  shop,
        'service': service,
        'timeslot': {
            'time': selected_time,
            'date_repr': date_repr,
            'date': selected_date,
        },
        'specialist': specialist,
    }
    print(context)
    return render(request, 'serviceFinally.html', context)


def notes(request):
    return render(request, 'notes.html')


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
def get_services(request):
    service_type = request.GET.get('service_type', '')
    if service_type == '':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response({'services': list(map(list, Service.objects
                                 .filter(service_type=service_type)
                                 .values_list('pk', 'name')))})


@api_view(['GET', 'POST,'])
def get_specialists(request):
    shop = request.GET.get('shop', '')
    service = request.GET.get('service', '')
    free_slots = (TimeSlot.objects.filter(appointment__isnull=True)
                  .prefetch_related("specialist"))
    service_specialists = Specialist.objects.filter(services=service)
    if shop != '0':
        free_slots = free_slots.filter(shop__id=shop)
    specialists = (free_slots.filter(specialist__in=service_specialists)
                             .distinct()
                             .values_list('specialist', 'specialist__name'))
    specialists_serialized = list(map(list, specialists))
    specialists_serialized.insert(0, [0, 'Любой специалист'])
    return Response({'specialists': specialists_serialized})


@api_view(['GET', 'POST,'])
def get_free_timeslots(request):
    shop_id = int(request.GET.get('shop', '0'))
    service_id = int(request.GET.get('service', '0'))
    specialist_id = int(request.GET.get('specialist', '0'))
    selected_date = request.GET.get('date', f'{date.today()}')
    free_slots = (TimeSlot.objects.filter(appointment__isnull=True)
                  .prefetch_related("specialist"))
    service_specialists = Specialist.objects.filter(services=service_id)
    if shop_id:
        free_slots = free_slots.filter(shop__id=shop_id)
    if not specialist_id:
        free_slots = free_slots.filter(specialist__in=service_specialists)
    else:
        free_slots = free_slots.filter(specialist__id=specialist_id)
    morning_slots = free_slots.filter(date=selected_date).filter(time__lt="12:00").values_list('time', flat=True).distinct()
    afternoon_slots = free_slots.filter(date=selected_date).filter(time__range=("12:00", "16:59")).values_list('time', flat=True).distinct()
    evening_slots = free_slots.filter(date=selected_date).filter(time__gte="17:00").values_list('time', flat=True).distinct()
    context = {
        "morning": morning_slots,
        "afternoon": afternoon_slots,
        "evening": evening_slots,
    }
    return Response(context)
