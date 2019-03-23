# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class DICT(models.Model):
    CODE = models.CharField(max_length=64)
    PASSWORD = models.CharField(max_length=64)
