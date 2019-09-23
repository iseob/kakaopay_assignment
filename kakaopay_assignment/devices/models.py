from django.db import models
from model_utils import Choices
import csv

from core.models import TimeStampedModel
from kakaopay_assignment.settings import BASE_DIR


class Device(TimeStampedModel, models.Model):
    DEVICE_ID_MAX_LENGTH = 128
    DEVICE_NAME_CHOICES = Choices('phone', 'desktop', 'laptop', 'etc', 'pad')
    DEVICE_NAME_MAX_LENGTH = 12

    device_id = models.CharField(unique=True, max_length=DEVICE_ID_MAX_LENGTH, db_index=True)
    device_name = models.CharField(choices=DEVICE_NAME_CHOICES, max_length=DEVICE_NAME_MAX_LENGTH, db_index=True)

    class Meta:
        ordering = ['-id']

    @classmethod
    def load_initial_data(cls):
        with open(f'{BASE_DIR}/device_data.csv', newline='') as csv_file:
            data = list(csv.reader(csv_file))
            for each_data in data[1:]:
                cls.objects.create(device_id=each_data[0], device_name=each_data[1])
