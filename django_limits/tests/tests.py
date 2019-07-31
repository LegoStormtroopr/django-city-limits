from django.test import TestCase
from django_limits.tests import models
from django_limits.exceptions import LimitExceeded


class LimitsTestCase(TestCase):
    def setUp(self):
        self.nutbush = models.City.objects.create(name='Nutbush')
        self.princeton = models.City.objects.create(name='New Jersey')

    def test_horse_limits(self):
        my_horse = models.Horse.objects.create(name='bessie', city=self.nutbush)
        with self.assertRaises(LimitExceeded):
            # Its a one horse town!
            models.Horse.objects.create(name='bessie', city=self.nutbush)

        models.Horse.objects.create(name='goldie', city=self.princeton)

        my_horse.name = "seabiscuit"
        my_horse.save()
        
        my_horse.refresh_from_db()
        
        self.assertEqual(my_horse.name, "seabiscuit")

    def test_house_limits(self):
        models.House.objects.create(name='church', city=self.nutbush)
        models.House.objects.create(name='gin', city=self.nutbush)
        models.House.objects.create(name='school', city=self.nutbush)
        models.House.objects.create(name='out', city=self.nutbush)

        with self.assertRaises(LimitExceeded):
            # Maximum of 4 valid houses in Nutbush!
            models.House.objects.create(name='dog', city=self.nutbush)

         # Dr. House can be in princeton
        dr = models.House.objects.create(name='Doctor Gregory', city=self.princeton)

        with self.assertRaises(LimitExceeded):
            # No Dr. House cannot move to Nutbush!
            dr.city = self.nutbush
            dr.save()

    def test_motorcycle_limits(self):
        with self.assertRaises(LimitExceeded):
            # No motorcycles in Nutbush!
            models.Motorcycle.objects.create(name="Harley Davidson", city=self.nutbush)

        # Dr House can ride a hog, but only in Princeton
        models.Motorcycle.objects.create(name="Harley Davidson", city=self.princeton)

    def test_ration_limits(self):
        models.Ration.objects.create(name='Salt pork', city=self.nutbush)
        seconds = models.Ration.objects.create(name='Salt pork', city=self.nutbush)

        with self.assertRaises(LimitExceeded):
            # You've already had too much!
            models.Ration.objects.create(name='Molasses', city=self.nutbush)

        seconds.delete()
        models.Ration.objects.create(name='Molasses', city=self.nutbush)

        with self.assertRaises(LimitExceeded):
            # No more molasses
            models.Ration.objects.create(name='Molasses', city=self.nutbush)
