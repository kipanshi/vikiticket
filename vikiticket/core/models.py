# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from tinymce import models as tinymce_models
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models import signals

from django.conf import settings

from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

# South introspection for custom tinymce field
if settings.DEBUG:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^tinymce\.models\.HTMLField"])
    add_introspection_rules(
        [], ["^phonenumber_field\.modelfields\.PhoneNumberField"])


SEAT_STATUS_CHOICES = (
    ('F', 'Свободно'),
    ('R', 'Резерв (вписки)'),
    ('B', 'Заказано'),
    ('S', 'Продано'),
    ('N', 'Недоступно для заказа'),
)

ORDER_STATUS_CHOICES = (
    ('R', 'В работе'),
    ('S', 'Завершен'),
)


class Event(models.Model):
    """
    Contains information on the event and binds together
    all necessary parts.
    """
    title = models.CharField(verbose_name=_(u'Название'), max_length=200)
    performer = models.CharField(verbose_name=_(u'Исполнитель'),
                                 max_length=200)
    event_links = tinymce_models.HTMLField(verbose_name=_(u'Ссылки'))
    slug = models.SlugField(_('Слаг'), max_length=40)
    stage_picture = models.TextField(verbose_name=_(u'Схема зала'),
                                     blank=True, null=True)
    css_override = models.TextField(_(u'Доп. CSS стили'),
                                            blank=True)
    press_release = tinymce_models.HTMLField(verbose_name=_(u'Пресс-релиз'))
    special_offer = tinymce_models.HTMLField(
        verbose_name=_(u'Специальное предложение'))
    social_widgets = models.TextField(verbose_name=_(u'Виджеты соцсетей'))

    info = tinymce_models.HTMLField(verbose_name=_(u'Информация о билетах'),)
    stage_name = models.CharField(_(u'Название площадки'), max_length=200)
    stage_address = models.CharField(_(u'Адрес площадки'), max_length=300)
    bottom_info = tinymce_models.HTMLField(
        verbose_name=_(u'Адрес площадки/инфо'))
    date = models.DateTimeField(verbose_name=_(u'Дата проведения'))
    is_published = models.BooleanField(
        _(u'В публичном доступе'), default=False)

    class Meta:
        verbose_name = _(u'Информация о концерте')
        verbose_name_plural = _(u'Информация о концерте')
        ordering = ('-id',)

    def date_arrived(self):
        """ Booking is closed one day before event date. """
        if datetime.datetime.now().date() >= self.date.date():
            return True
        return False

    def past_due(self):
        """ Is event past due or not. Add 2.5 hours for gig time. """
        if datetime.datetime.now() > self.date + datetime.timedelta(hours=2.5):
            return True
        return False

    def __unicode__(self):
        return self.slug


class Page(models.Model):
    slug = models.CharField(_(u'Слаг'), max_length=100, db_index=True)
    title = models.CharField(_(u'Заголовок'), max_length=200)
    content = models.TextField(_(u'Контент'), blank=True)
    ordering = models.IntegerField(_(u'Порядок сортировки'), default=1)
    event = models.ForeignKey(Event, related_name='pages')

    class Meta:
        verbose_name = _(u'Страница VikiTicket')
        verbose_name_plural = _(u'Страницы VikiTicket')
        ordering = ('-ordering',)

    def __unicode__(self):
        return u"%s -- %s" % (self.slug, self.title)

    def get_absolute_url(self):
        return u'%s/%s/' % (self.event.slug, self.slug)


class Client(models.Model):
    """
    Client class.
    """
    name = models.CharField(verbose_name=_(u'Имя'),
                            max_length=100,
                            help_text=_(u'Ваше имя'))
    phone = PhoneNumberField(verbose_name=_(u'Номер телефона'), \
        help_text=_(u'Обязательное поле'))
    email = models.EmailField(
        blank=True, null=True, help_text=_(u'Необязательное поле'))
    create_date = models.DateTimeField(
        verbose_name=_(u'Дата создания'), auto_now_add=True)
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = _(u'Клиент')
        verbose_name_plural = _(u'Клиенты')

    def __unicode__(self):
        return u'%s, %s, %s' % (self.name, self.phone, self.email)


class PriceCategory(models.Model):
    """
    Price category for seats.
    """
    color = models.CharField(verbose_name=_(u'Цвет'), max_length=100)
    price = models.IntegerField(verbose_name=_(u'Цена'))
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = _(u'Ценовая категория')
        verbose_name_plural = _(u'Ценовые категории')

    def __unicode__(self):
        return u'%s, %s' % (self.color, self.price)


class Stage(models.Model):
    """
    Stage.
    """
    name = models.CharField(verbose_name=_(u'Площадка'), max_length=100)
    event = models.ForeignKey(Event, related_name='stages')

    class Meta:
        verbose_name = _(u'Площадка')
        verbose_name_plural = _(u'Площадки')

    def add_placement(self, names):
        """ Add more placements in a stage. """
        if not hasattr(names, '__iter__'):
            names = (names,)
        return [Placement.objects.create(event=self.event,
                                         stage=self,
                                         name=name)
                for name in names]

    def delete_placement(self, names):
        """ Delete placements in a stage. """
        if not hasattr(names, '__iter__'):
            names = (names,)
        return [Placement.objects.filter(event=self.event,
                                         stage=self,
                                         name=name)[0].delete()
                for name in names]

    def __unicode__(self):
        return u'%s' % self.name


class Placement(models.Model):
    """
    Placement inside the stage.
    """
    name = models.CharField(verbose_name=_(u'Расположение'), max_length=100)
    stage = models.ForeignKey(
        Stage, verbose_name=_(u'Площадка'), related_name='placements')
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = _(u'Расположение')
        verbose_name_plural = _(u'Расположения')

    @property
    def first_letter(self):
        """ First letter of placement. """
        return self.name[0]

    def add_row(self, count=None):
        """ Add one more row in a placement. """
        try:
            new_row_number = self.rows.latest('number').number + 1
        except ObjectDoesNotExist:
            new_row_number = self.rows.count() + 1

        if count:
            return [Row.objects.create(event=self.event, placement=self,
                                      number=new_row_number + increment)
                    for increment in xrange(count)]
        return Row.objects.create(event=self.event, placement=self,
                                  number=new_row_number)

    def delete_row(self, count=None):
        """ Delete rows from the end. """
        if count:
            [self.rows.latest('number').delete()
             for dummy in xrange(count)]
        else:
            self.rows.latest('number').delete()

    def __unicode__(self):
        return u'%s' % self.name


class Row(models.Model):
    """
    Row inside placement.
    """
    placement = models.ForeignKey(
        Placement, verbose_name=_(u'Расположение'), related_name='rows')
    number = models.IntegerField(verbose_name=_(u'Номер'))
    prefix = models.CharField(verbose_name=_(u'Специальное название'),
                              max_length=72, blank=True, null=True)
    suffix = models.CharField(verbose_name=_(u'Добавка к номеру (суффикс)'),
                              max_length=72, blank=True, null=True)
    event = models.ForeignKey(Event)

    class Meta:
        verbose_name = _(u'Ряд')
        verbose_name_plural = _(u'Ряды')

    @property
    def seat_count(self):
        """ Number of seats in a row. """
        return self.seats.count()

    def add_seat(self, count=None):
        """ Add one more seat in a row. """
        try:
            new_seat_number = self.seats.latest('number').number + 1
            price_category = self.seats.latest('pk').price_category
        except ObjectDoesNotExist:
            new_seat_number = self.seats.count() + 1
            price_category = PriceCategory.objects.all()[0]

        if count:
            return [Seat.objects.create(event=self.event, row=self,
                                   price_category=price_category,
                                   number=new_seat_number + increment)
                    for increment in xrange(count)]
        return Seat.objects.create(event=self.event, row=self,
                                   price_category=price_category,
                                   number=new_seat_number)

    def delete_seat(self, count=None):
        """ Delete seats from the end. """
        if count:
            [self.seats.latest('number').delete()
             for dummy in xrange(count)]
        else:
            self.seats.latest('number').delete()

    def __unicode__(self):
        prefix = self.prefix if self.prefix else _(u'Ряд')
        suffix = self.suffix if self.suffix else ''
        return u'%s, %s %s%s' % (self.placement, prefix, self.number, suffix)


class Tag(models.Model):
    """
    Tag for seat.
    """
    name = models.CharField(verbose_name=_(u'Имя'), max_length=100)
    color = models.CharField(
        verbose_name=_(u'Цвет'), max_length=10, null=True, blank=True)
    create_date = models.DateTimeField(
        verbose_name=_(u'Дата создания'), auto_now_add=True)
    event = models.ForeignKey(Event, related_name='tags')

    class Meta:
        verbose_name = _(u'Тэг')
        verbose_name_plural = _(u'Тэги')

    def __unicode__(self):
        return u'%s' % (self.name)


class Order(models.Model):
    """
    Order for client.
    """
    client = models.ForeignKey(Client, verbose_name=_(u'Клиент'),
                               related_name='orders')
    status = models.CharField(verbose_name=_(u'Статус'), max_length=1,
                              choices=ORDER_STATUS_CHOICES,
                              default=ORDER_STATUS_CHOICES[0])
    create_date = models.DateTimeField(
        verbose_name=_(u'Дата создания'), auto_now_add=True)
    update_date = models.DateTimeField(
        verbose_name=_(u'Дата последнего изменения'),
        auto_now_add=True, auto_now=True)
    close_date = models.DateTimeField(
        verbose_name=_(u'Дата завершения'), null=True, blank=True)
    comment = models.CharField(
        verbose_name=_(u'Дополнительная информация'),
        max_length=200, null=True, blank=True)
    event = models.ForeignKey(Event, related_name='orders')

    class Meta:
        verbose_name = _(u'Заказ')
        verbose_name_plural = _(u'Заказы')

    @property
    def total_price(self):
        """ Total price of the order. """
        return sum([seat.price_category.price for seat in self.seats.all()])

    def __unicode__(self):
        return u'№ %s: %s, %s, Total: %s, %s' % (self.id,
                                self.client,
                                self.create_date.strftime('%b %d, %H:%M'),
                                self.total_price,
                                self.status)


class Seat(models.Model):
    """
    Seat class, represents single seat.
    """
    status = models.CharField(verbose_name=_(u'Статус'), max_length=1,
                              choices=SEAT_STATUS_CHOICES,
                              default=SEAT_STATUS_CHOICES[0][0])
    price_category = models.ForeignKey(PriceCategory,
                                       verbose_name=_(u'Ценовая категория'),
                                       blank=True, null=True,
                                       on_delete=models.SET_NULL)
    tag = models.ForeignKey(Tag, verbose_name=_(u'Тэг'),
                            blank=True, null=True, related_name='seats',
                            on_delete=models.SET_NULL)
    comment = models.CharField(verbose_name=_(u'Дополнительная информация'),
                               max_length=100, blank=True, null=True)
    row = models.ForeignKey(Row, verbose_name=_(u'Ряд'), related_name='seats')
    number = models.IntegerField(verbose_name=_(u'Номер'))
    order = models.ForeignKey(Order, verbose_name=_(u'Заказ'), blank=True,
                              null=True, related_name='seats',
                              on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, related_name='seats')

    class Meta:
        verbose_name = _(u'Место')
        verbose_name_plural = _(u'Места')

    def colored_number(self):
        return '<div style="float:left; width: 20px;"><b>%s</b></div>' \
            '<div style="height:16px;width:16px;' \
            'background:%s;float:left;"></div>' % \
            (self.number, str(self.price_category.color).lower())
    colored_number.allow_tags = True

    def order_pretty(self):
        return u'%s, Total: %s, %s, <br/>%s, %s, %s' % (self.order.client.name,
                            self.order.total_price,
                            self.order.create_date.strftime('%b %d, %H:%M'),
                            self.order.client.phone,
                            self.order.client.email,
                            self.order.status)
    order_pretty.allow_tags = True

    def __unicode__(self):
        return u'%s, %s %s' % (self.row, _(u'Место'), self.number)


class UserProfile(models.Model):
    """
    Store user permissions to access events.
    """
    user = models.OneToOneField(User, related_name='profile',
        verbose_name=_('user'))

    event = models.ForeignKey(
        Event, verbose_name=_(u'Событие'), blank=True, null=True,
        related_name='profiles',
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _(u'Профиль пользователя')
        verbose_name_plural = _(u'Профили пользователя')

    def __unicode__(self):
        label = self.user.get_full_name() or self.user.username
        return u'%s (%s)' % (label, self.event)


# Signal functions
@receiver(signals.pre_save, sender=Order)
def auto_set_order_close_date(instance, **kwargs):
    """
    Automatically set close date for the order.
    """
    # Check for order status
    if instance.status == ORDER_STATUS_CHOICES[1][0]:
        # Set close date to now
        instance.close_date = datetime.datetime.now()
    if instance.status == ORDER_STATUS_CHOICES[0][0]:
        # Set close date to None if made running again
        instance.close_date = None


@receiver(signals.post_save, sender=Order)
def auto_set_seat_status_order_succeed(instance, **kwargs):
    """
    Automatically set seat status if order is assigned to it.
    """
    seats = instance.seats.all()
    # Check for order status
    if instance.status == ORDER_STATUS_CHOICES[1][0]:
        # Loop and save
        for seat in seats:
            seat.status = SEAT_STATUS_CHOICES[3][0]
            seat.save()
    if instance.status == ORDER_STATUS_CHOICES[0][0]:
        # Loop and save
        for seat in seats:
            seat.status = SEAT_STATUS_CHOICES[2][0]
            seat.save()


@receiver(signals.pre_save, sender=Seat)
def auto_set_seat_status(instance, **kwargs):
    """
    Automatically set seat status to ``Free`` if
    order is deleted.
    """
    if instance.order:
        # Check for order status
        if instance.order.status == ORDER_STATUS_CHOICES[0][0]:
            status = SEAT_STATUS_CHOICES[2][0]
        elif instance.order.status == ORDER_STATUS_CHOICES[1][0]:
            status = SEAT_STATUS_CHOICES[3][0]
        # Set status
        instance.status = status


@receiver(signals.pre_delete, sender=Order)
def auto_set_seat_free(instance, **kwargs):
    """
    Automatically set seat status to ``Free``
    if order is deleted.
    """
    for seat in instance.seats.all():
        seat.order = None
        seat.status = SEAT_STATUS_CHOICES[0][0]
        seat.save()


# Signal functions
@receiver(signals.post_save, sender=User)
def auto_create_user_profile(instance, **kwargs):
    """
    Auto create new user profile instance after user creation.
    """
    if kwargs['created']:
        UserProfile.objects.get_or_create(user=instance)


def auto_create_default_stage(event):
    """ Create default stage. """
    rows, seats, placement_name, color, price = settings.VIKITICKET_STAGE
    stage = Stage.objects.create(name=event.stage_name, event=event)
    placement = Placement.objects.create(name=placement_name,
                                         stage=stage,
                                         event=event)
    price_category = PriceCategory.objects.create(color=color,
                                                  price=price,
                                                  event=event)
    # Create rows and seats
    for num in xrange(rows):
        row = Row.objects.create(placement=placement,
                                 number=num + 1, event=event)
        for number in xrange(seats):
            Seat.objects.create(row=row, number=number + 1,
                                price_category=price_category,
                                status=SEAT_STATUS_CHOICES[0][0],
                                event=event)


@receiver(signals.post_save,
          sender=Event,
          dispatch_uid='core.models.auto_create_pages_on_event_created')
def auto_create_on_event_created(instance, **kwargs):
    """
    Automatically create default pages and stage for event when it is created.
    """
    if 'created' in kwargs:
        if kwargs['created']:
            # Create VikiTicket Pages
            for slug, title, ordering in settings.VIKITICKET_PAGES:
                Page.objects.create(slug=slug, title=title, ordering=ordering,
                                    event=instance, content=instance.title)
            # Create stage
            auto_create_default_stage(event=instance)
