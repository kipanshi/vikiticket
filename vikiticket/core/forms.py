# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from core.models import Client, Seat
from django.shortcuts import get_object_or_404


class OrderForm(forms.ModelForm):
    """
    User order form.
    """
    class Meta:
        model = Client
        exclude = ('event',)

    seats = forms.CharField(max_length=30,
                            widget=forms.HiddenInput(), required=False)
    comment = forms.CharField(label=_(u'Дополнительная информация'),
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 25}), required=False)

    def clean_seats(self):
        """
        Cleaning seats form and also verifying that it's not empty.
        """
        if not self.cleaned_data['seats']:
            raise forms.ValidationError(_(u'Выберите хотя бы одно место для заказа.'))
        data = self.cleaned_data['seats']
        if data[0] != ',' or data[-1] != ',':
            raise forms.ValidationError(_(u'Данные о выбранных местах повреждены.'))
        # Clean from commas
        id_list = data[1:-1].split(',')
        # Get corresponding seats list
        seats = [get_object_or_404(Seat, pk=_to_int(id)) for id in id_list]
        return seats


def _to_int(value):
    """
    Convert string to integer, if
    not successful - raise Django exception.
    """
    try:
        result = int(value)
    except:
        raise forms.ValidationError(_(u'Данные о выбранных местах повреждены.'))
    return result
