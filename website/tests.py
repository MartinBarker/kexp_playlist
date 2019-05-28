from django.test import TestCase
from playlist.models import plays
from playlist.views import index
from django.utils import timezone


class AnimalTestCase(TestCase):
    def setUp(self):
        print("setup")
        
        #Animal.objects.create(name="lion", sound="roar")
        #Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        print("test")
        #lion = Animal.objects.get(name="lion")
        #cat = Animal.objects.get(name="cat")
        #self.assertEqual(lion.speak(), 'The lion says "roar"')
        #self.assertEqual(cat.speak(), 'The cat says "meow"')
