from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from beauty_city_app.models import Appointment
from django.utils import timezone


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
            } for i in range(1,7)
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
    # Пример значений для заполнения шаблона
    context = {
        'shops': [
            {
                'name': 'BeautyCity Пушкинская',
                'address': 'ул. Пушкинская, д. 78А',
            },
            {
                'name': 'BeautyCity Ленина',
                'address': 'ул. Ленина, д. 211',
            },
            {
                'name': 'BeautyCity Красная',
                'address': 'ул. Красная, д. 10',
            },
        ],
        'service_types': [
            {
                'name': 'Парикмахерские услуги',
                'services': [
                    {
                        'name': 'Окрашивание волос',
                        'price': 5000,
                    },
                    {
                        'name': 'Укладка волос',
                        'price': 1500,
                    },
                ],
            },
            {
                'name': 'Ногтевой сервис',
                'services': [
                    {
                        'name': 'Маникюр. Классический',
                        'price': 1400,
                    },
                    {
                        'name': 'Педикюр',
                        'price': 1400,
                    },
                    {
                        'name': 'Наращивание ногтей',
                        'price': 1500,
                    },
                ],
            },
            {
                'name': 'Макияж',
                'services': [
                    {
                        'name': 'Дневной макияж',
                        'price': 1400,
                    },
                    {
                        'name': 'Свадебный макияж',
                        'price': 3000,
                    },
                    {
                        'name': 'Вечерний макияж',
                        'price': 2000,
                    },
                ],
            }
        ],
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
    # Пример значений для заполнения шаблона
    context = {
        'order': {
            'id': 32985,
            'shop': {
                'name': 'BeautyCity Пушкинская,',
                'address': 'ул. Пушкинская, д. 78А'
            },
            'service': {
                'name': 'Дневной макияж', 'price': 750,
                'time': '16:30', 'date': '18 ноября',
            },
            'specialist': {
                'name': 'Елена Грибнова',
                'photo': '/static/img/masters/avatar/vizajist1.svg'
            }

        }
    }
    return render(request, 'serviceFinally.html', context['order'])


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
