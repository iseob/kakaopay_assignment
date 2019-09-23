from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from model_utils import Choices
import csv
from core.models import TimeStampedModel
from kakaopay_assignment.settings import BASE_DIR


class Stat(TimeStampedModel, models.Model):
    DEVICE_NAME_CHOICES = Choices('phone', 'desktop', 'laptop', 'etc', 'pad')
    DEVICE_NAME_MAX_LENGTH = 12

    year = models.IntegerField(db_index=True)
    total_usage_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    device_name = models.CharField(choices=DEVICE_NAME_CHOICES, max_length=DEVICE_NAME_MAX_LENGTH, db_index=True)
    device_usage_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    @classmethod
    def load_initial_data(cls):
        with open(f'{BASE_DIR}/stat_data.csv', newline='') as csv_file:
            data = list(csv.reader(csv_file))
            for each_data in data[1:]:
                year = each_data[0]
                for idx, _type in enumerate(['phone', 'desktop', 'laptop', 'etc', 'pad']):
                    rate_idx = idx + 2
                    if each_data[rate_idx] != '-':
                        cls.objects.create(year=year, total_usage_rate=float(each_data[1]), device_name=_type,
                                           device_usage_rate=float(each_data[rate_idx]))
