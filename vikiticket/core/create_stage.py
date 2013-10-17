from core.models import *

ev = Event.objects.get(pk=1)
st = Stage.objects.get(pk=10)
pr = Placement.objects.get(pk=1)

[Placement.objects.create(name=u'А%s' % (i + 1), event=ev, stage=st) for i in xrange(5)]
[Placement.objects.create(name=u'Б%s' % (i + 1), event=ev, stage=st) for i in xrange(5)]
[Placement.objects.create(name=u'В%s' % (i + 1), event=ev, stage=st) for i in xrange(8)]

[Row.objects.create(placement=pr, event=ev, number=(i + 1)) for i in xrange(16)]

[[Row.objects.get_or_create(placement=pl, event=ev, number=(i + 1)) for i in xrange(1)] for pl in Placement.objects.filter(name__contains=u'А')]
[[Row.objects.get_or_create(placement=pl, event=ev, number=(i + 1)) for i in xrange(1)] for pl in Placement.objects.filter(name__contains=u'Б')]
[[Row.objects.get_or_create(placement=pl, event=ev, number=(i + 1)) for i in xrange(1)] for pl in Placement.objects.filter(name__contains=u'В')]

from core.models import *
ev = Event.objects.get(pk=1)
price_category=PriceCategory.objects.get(pk=1)
[[[Seat.objects.get_or_create(price_category=price_category, row=row, event=ev, number=int(i + 1)) for i in xrange(2)] for row in pl.rows.all()] for pl in Placement.objects.filter(name__contains=u'А')]
