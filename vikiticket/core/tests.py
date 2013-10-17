"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import datetime

from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse


TEST_EVENT = 'test_event'
TEST_STAGE = 'test_stage'
TEST_PLACEMENT = 'test_placement'

class ModelsTest(TestCase):
    def test_create_new_event(self):
        """
        Tests creation of new event with
        all stuff and basic stage.
        """
        from core.models import Event, Page, Stage, Placement, \
            Row, Seat, PriceCategory
        from core.models import SEAT_STATUS_CHOICES

        event = Event.objects.create(title=TEST_EVENT,
                                     performer=TEST_EVENT,
                                     event_links=TEST_EVENT,
                                     slug=TEST_EVENT,
                                     css_override=TEST_EVENT,
                                     press_release=TEST_EVENT,
                                     special_offer=TEST_EVENT,
                                     social_widgets=TEST_EVENT,
                                     info=TEST_EVENT,
                                     stage_name=TEST_EVENT,
                                     stage_address=TEST_EVENT,
                                     bottom_info=TEST_EVENT,
                                     date=datetime.now(),
                                     is_published=True
                                     )
        # Assert VikiTicket Pages was auto-created
        [self.assertIn((page.slug, page.title, page.ordering),
                       settings.VIKITICKET_PAGES)
            for page in Page.objects.filter(event=event)]

        # Test ordering page
        url = reverse('order_view', args=[event.slug])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200,
                         'Failed with code %s and response %s' % \
                        (response.status_code, response))
            
    def test_event_publishing(self):
        """ Test functionality of ``event.is_published()`` method. """
        # TODO: Need to write this test
        pass

