import datetime

from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Shop(models.Model):
    name = models.CharField(verbose_name="название", max_length=100)
    address = models.TextField(verbose_name="адрес")
    phone = PhoneNumberField(verbose_name="номер телефона")
    image = models.ImageField(verbose_name="изображение", upload_to="shop_images/", null=True, blank=True)

    class Meta:
        verbose_name = "салон"
        verbose_name_plural = "салоны"

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(verbose_name="имя", max_length=100)
    phone = PhoneNumberField(verbose_name="номер телефона")
    profile_picture = models.ImageField(verbose_name="аватарка", upload_to="user_pictures/", null=True, blank=True)

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return self.name


class Service(models.Model):
    SERVICE_TYPES = [
        ("HS", "Парикмахерские услуги"),
        ("MU", "Макияж"),
        ("NS", "Ногтевой сервис")
    ]
    name = models.CharField(verbose_name="название", max_length=100)
    service_type = models.CharField(verbose_name="тип услуги", max_length=2, choices=SERVICE_TYPES, db_index=True)
    shop = models.ManyToManyField(Shop, verbose_name="салоны", related_name="services")
    image = models.ImageField(verbose_name="изображение", upload_to="service_images/", null=True, blank=True)
    price = models.IntegerField(verbose_name="стоимость", validators=[MinValueValidator(0)])
    is_archived = models.BooleanField()

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "услуги"

    def __str__(self):
        return self.name


class Specialist(models.Model):
    name = models.CharField(verbose_name="имя", max_length=100)
    profile_picture = models.ImageField(verbose_name="аватарка", null=True, blank=True)
    services = models.ManyToManyField(Service, verbose_name="услуги", related_name="services")

    class Meta:
        verbose_name = "специалист"
        verbose_name_plural = "специалисты"

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    TIME_CHOICES = [
        (datetime.time(10, 00), '10:00'),
        (datetime.time(11, 00), '11:00'),
        (datetime.time(12, 00), '12:00'),
        (datetime.time(13, 00), '13:00'),
        (datetime.time(14, 00), '14:00'),
        (datetime.time(15, 00), '15:00'),
        (datetime.time(16, 00), '16:00'),
        (datetime.time(17, 00), '17:00'),
        (datetime.time(18, 00), '18:00'),
    ]
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        verbose_name="специалист",
        related_name="time_slots"
    )
    date = models.DateField(verbose_name="дата")
    time = models.TimeField(verbose_name="время", choices=TIME_CHOICES)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="салон", related_name="time_slots")

    class Meta:
        verbose_name = "временной слот"
        verbose_name_plural = "временные слоты"
        unique_together = ["date", "time", "specialist"]

    def __str__(self):
        return f"{self.shop}, {self.specialist} - {self.date}/{self.time}"


class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="клиент", related_name="appointments")
    time_slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        verbose_name="временной слот",
        related_name="appointment"
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="услуга", related_name="appointments")  # запретить удаление, если есть записи
    price = models.IntegerField(verbose_name="стоимость", validators=[MinValueValidator(0)])
    is_paid = models.BooleanField(verbose_name="запись оплачена", default=False)

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"

    def __str__(self):
        return f"{self.client} - {self.time_slot}"


class Review(models.Model):
    # Возможно, переделать во имя совместимости с фронтэндом
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="клиент", related_name="reviews")
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        verbose_name="специалист",
        related_name="reviews"
    )
    date = models.DateField(verbose_name="дата посещения")
    text = models.TextField(verbose_name="отзыв", blank=True)

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return f"{self.specialist} - {self.date}"
