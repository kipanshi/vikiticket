# -*- coding: utf-8 -*-
import logging

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views.generic.base import TemplateResponseMixin
from django.template.context import RequestContext
from django.http import Http404
from django.contrib.auth.models import User

from core.models import Event, Client, Order, ORDER_STATUS_CHOICES, \
    SEAT_STATUS_CHOICES, Page, Stage
from core.forms import OrderForm


class EventPublishedMixin(TemplateResponseMixin):
    """
    Mixin for making an event published.
    """
    def render_to_response(self, context):
        is_published = context['event'].is_published
        if not is_published:
            if not self.request.user.is_staff:
                raise Http404
        return super(EventPublishedMixin,
                     self).render_to_response(context)


class PageView(EventPublishedMixin, TemplateView):
    """
    Event pages view.
    """
    template_name = "core/event_page.html"
    context_object_name = 'page'

    def get_context_data(self, **kwargs):
        """
        Update context.
        """
        event = get_object_or_404(Event, slug=self.kwargs['event_slug'])
        slug = self.kwargs.get('slug')
        page = get_object_or_404(Page, event=event, slug=slug)
        # Call parent's context
        context = super(PageView, self).get_context_data(**kwargs)
        context.update({
            'event': event,
            'page': page,
        })
        return context


class OrderView(EventPublishedMixin, FormView):
    """
    Main buy view.
    """
    template_name = "core/event_order.html"
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        """
        Update context.
        """
        event = get_object_or_404(Event, slug=self.kwargs['slug'])
        # Call parent's context
        context = super(OrderView, self).get_context_data(**kwargs)
        context.update({
            'event': event,
            'stage': Stage.objects.get(event=event),
        })
        return context

    def form_valid(self, form):
        """
        Logic for valid form.
        """
        context = self.get_context_data(form=form)
        context.update({
            'seats': form.cleaned_data['seats'],
            'name': form.cleaned_data['name'],
            'phone': form.cleaned_data['phone'],
            'email': form.cleaned_data['email'],
            'comment': form.cleaned_data['comment']
        })

        action = self.request.GET.get('action')
        if action == 'preview':
            self.template_name = "core/event_order_preview.html"
            return self.render_to_response(context)
        elif action == 'confirm':
            # Now we can create an order
            client, created = Client.objects.get_or_create(
                               name=form.cleaned_data['name'],
                               phone=form.cleaned_data['phone'],
                               email=form.cleaned_data['email'],
                               event=context['event']
            )
            client.save()

            order = Order(
                          client=client,
                          status=ORDER_STATUS_CHOICES[0][0],
                          comment=form.cleaned_data['comment'],
                          event=context['event']
            )
            order.save()

            for seat in form.cleaned_data['seats']:
                # Check for seat status
                if seat.status == SEAT_STATUS_CHOICES[0][0]:
                    seat.order = order
                    seat.save()
                else:
                    order.delete()
                    self.template_name = 'core/event_order.html'
                    return self.render_to_response(context)

            # Send email to managers that order has been created.
            # We put it into try clause
            logger = logging.getLogger('orders')
            handler = logging.FileHandler('var/orders.log')
            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            try:
                subject = u'Новый заказ - № %s: %s заказал %s билетов.' % \
                        (order.id, order.client, len(order.seats.all()))
                message = render_to_string('core/email/new_order.txt',
                                           {'order': order})
                recipients = [u.email for u
                              in User.objects.filter(is_staff=True)
                              if u.profile.event == context['event']]
                send_mail(subject, message, 'vikiticket@gmail.com', recipients,
                               fail_silently=False)
                # Log about success
                logger.info(subject)
            except Exception, e:
                # Log error and order ID
                logger.error('Error during managers send mail: %s : %s' % \
                             (e, subject))

            self.template_name = "core/event_order_success.html"
            return self.render_to_response(context)
        # Render main template
        return self.render_to_response(context)

    def get_initial(self):
        """
        Get form initial data.
        """
        return {}


def custom_404_view(request):
        return render_to_response(
            "404.html",
            {'event': request.user.profile.event},
            context_instance=RequestContext(request)
            )


def custom_500_view(request):
        return render_to_response(
            "500.html",
            {'event': request.user.profile.event},
            context_instance=RequestContext(request)
            )
