import os
import binascii
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from todo_app.enumerations import Status


@receiver(post_save, sender=User)
def user_access_token_creation(sender, instance: User, **kwargs):
    """
    Args:
       sender:      The model class.
       instance:    User object
    """
    # create AccessToken for new users
    if kwargs['created']:
        Token.objects.create(user=instance)


class ToDo(models.Model):

    user = models.ForeignKey(
        User,
        related_name='todos',
        on_delete=models.CASCADE,
    )

    title = models.TextField()

    description = models.TextField(
        null=True,
        blank=True,
    )

    state = models.IntegerField(
        choices=Status.get_tuple(),
        default=Status.TODO,
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f'{self.title}'
