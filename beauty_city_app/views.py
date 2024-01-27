from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
    data = {
        'shops': {
            '1': {'name': 'BeautyCity Пушкинская ул. Пушкинская, д. 78А',
                'service_types': {
                    '1': {
                        'name': 'Парикмахерские услуги',
                        'services': {
                            '1': {
                                'name': 'Окрашивание волос 5 000р.',
                            },
                            '2': {
                                'name': 'Укладка волос 1 500р.',
                            },
                        },
                    },
                    '2': {
                        'name': 'Ногтевой сервис',
                        'services': {
                            '3': {
                                'name': 'Маникюр. Классический 1400р.',
                            },
                            '4': {
                                'name': 'Педикюр 1 400р.',
                            },
                            '5': {
                                'name': 'Наращивание ногтей 1500р.',
                            },
                        },
                    },
                    '3': {
                        'name': 'Макияж',
                        'services': {
                            '6': {
                                'name': 'Дневной макияж 1 400р.',
                            },
                            '7': {
                                'name': 'Свадебный макияж 3 000р.',
                            },
                            '8': {
                                'name': 'Вечерний макияж 2 000р.',
                            },
                        },
                    }
                },
            },
            '2': {
                'name': 'BeautyCity Ленина ул. Ленина, д. 211',
                'service_types': {
                    '1': {
                        'name': 'Парикмахерские услуги',
                        'services': {
                            '1': {
                                'name': 'Окрашивание волос 5 000р.',
                            },
                            '2': {
                                'name': 'Укладка волос 1 500р.',
                            },
                        },
                    },
                    '2': {
                        'name': 'Ногтевой сервис',
                        'services': {
                            '3': {
                                'name': 'Маникюр. Классический 1400р.',
                            },
                            '4': {
                                'name': 'Педикюр 1 400р.',
                            },
                            '5': {
                                'name': 'Наращивание ногтей 1500р.',
                            },
                        },
                    },
                    '3': {
                        'name': 'Макияж',
                        'services': {
                            '6': {
                                'name': 'Дневной макияж 1 400р.',
                            },
                            '7': {
                                'name': 'Свадебный макияж 3 000р.',
                            },
                            '8': {
                                'name': 'Вечерний макияж 2 000р.',
                            },
                        },
                    }
                },
            },
            '3': {
                'name': 'BeautyCity Красная ул. Красная, д. 10',
                'service_types': {
                    '1': {
                        'name': 'Парикмахерские услуги',
                        'services': {
                            '1': {
                                'name': 'Окрашивание волос 5 000р.',
                            },
                            '2': {
                                'name': 'Укладка волос 1 500р.',
                            },
                        },
                    },
                    '2': {
                        'name': 'Ногтевой сервис',
                        'services': {
                            '3': {
                                'name': 'Маникюр. Классический 1400р.',
                            },
                            '4': {
                                'name': 'Педикюр 1 400р.',
                            },
                            '5': {
                                'name': 'Наращивание ногтей 1500р.',
                            },
                        },
                    },
                    '3': {
                        'name': 'Макияж',
                        'services': {
                            '6': {
                                'name': 'Дневной макияж 1 400р.',
                            },
                            '7': {
                                'name': 'Свадебный макияж 3 000р.',
                            },
                            '8': {
                                'name': 'Вечерний макияж 2 000р.',
                            },
                        },
                    }
                },
            },
        }
    }

    context['data'] = data
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


def manager(request):
    return render(request, 'admin.html')


@api_view(['GET', 'POST,'])
def get_select_tag_payload(request):
    print(f'{request.GET=}')
    return Response({'status': 'ok',
                     'tag_data': {'1': '2'}},
                    status=status.HTTP_200_OK, )
