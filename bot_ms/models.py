from django.db import models


class BotUser(models.Model):
    telegram_id = models.BigIntegerField()

    name = models.CharField(max_length=40)
    mail_flag = models.BooleanField(null=True)
    send_mail = models.BooleanField(default=False)
    contract_points = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    how_to_pay = models.IntegerField(default=0)
    contacts = models.IntegerField(default=0)
    objects = models.Manager()
