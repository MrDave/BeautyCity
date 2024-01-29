from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from beauty_city_app.models import Appointment, Service, Shop, Specialist, Client, TimeSlot, Review


def index(request):
    # Пример значений для заполнения шаблона

    shops = Shop.objects.all()
    services = Service.objects.all()
    specialists = Specialist.objects.annotate(review_count=Count('reviews'))
    reviews = Review.objects.all()

    context = {
        'shops': shops,
        'services': services,
        'specialists': specialists,
        'reviews': reviews,
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
        selected_specialist = get_object_or_404(Specialist, pk=specialist_id)
        specialist = {'pk': selected_specialist.pk,
                      'name': selected_specialist.name,
                      'photo': selected_specialist.profile_picture.url, }

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
    current_datetime = timezone.now()
    username = request.GET.get('username')
    phone = request.GET.get('phone')

    shop_id = int(request.GET.get('shop'))
    specialist_id = int(request.GET.get('specialist'))
    service_id = int(request.GET.get('service'))

    slot_date = request.GET.get('date')
    slot_time = request.GET.get('time')

    # client = get_object_or_404(Client, name=username, phone=phone)
    client, created = Client.objects.get_or_create(
        phone=phone,
        defaults={
            "name": username
        }
    )
    if specialist_id:
        time_slot = TimeSlot.objects.get(specialist=specialist_id, date=slot_date, time=slot_time)
    elif shop_id:
        time_slot = TimeSlot.objects.filter(shop=shop_id, date=slot_date, time=slot_time).first()
    else:
        time_slot = TimeSlot.objects.filter(date=slot_date, time=slot_time).first()

    beauty_service = Service.objects.get(id=service_id)
    new_appointment = Appointment.objects.create(
        client=client,
        time_slot=time_slot,
        service=beauty_service,
        price=beauty_service.price
    )
    appointments = Appointment.objects.filter(client=client)
    total_to_pay_amount = appointments.filter(is_paid=False).aggregate(Sum('price'))['price__sum'] or 0

    upcoming_appointments = appointments.filter(
        time_slot__date__gte=current_datetime.date()
    ).order_by('time_slot__date', 'time_slot__time')

    past_appointments = appointments.filter(
        time_slot__date__lt=current_datetime.date()
    ).order_by('-time_slot__date', '-time_slot__time')

    context = {
        'client': client,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'total_paid_amount': total_to_pay_amount,
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
def get_services(request):
    service_type = request.GET.get('service_type', '')
    if service_type == '':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    services =  (Service.objects.filter(service_type=service_type)
                        .values_list('pk', 'name', 'price', ))
    return Response({'services': [[pk, f'{name} - {price} р.']
                                   for pk, name, price in services]})


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
    morning_slots = (free_slots.filter(date=selected_date)
                     .filter(time__lt="12:00").values_list('time', flat=True)
                     .distinct())
    afternoon_slots = (free_slots.filter(date=selected_date)
                       .filter(time__range=("12:00", "16:59"))
                       .values_list('time', flat=True).distinct())
    evening_slots = (free_slots.filter(date=selected_date)
                     .filter(time__gte="17:00").values_list('time', flat=True)
                     .distinct())
    context = {
        "morning": morning_slots,
        "afternoon": afternoon_slots,
        "evening": evening_slots,
    }
    return Response(context)