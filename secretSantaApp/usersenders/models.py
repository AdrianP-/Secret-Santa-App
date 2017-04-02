from __future__ import unicode_literals
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _

import random
from collections import deque


class BaseUserSenderManager(models.Manager):

    def get_by_group(self, group):
        return self.filter(**{self.model.GROUP_FIELD: group})

    def get_by_name(self, name):
        return self.get(**{self.model.NAME_FIELD: name})

    def _create_sender_user(self, name, age, group, **extra_fields):
        user = self.model(name=name, age=age, group=group, **extra_fields)
        user.save(using=self._db)
        return user

class UserSenderManager(BaseUserSenderManager):
    use_in_migrations = True

    def pairup(self, people):
        """ Given a list of people, assign each one a secret santa partner
        from the list and return the pairings as a dict. Implemented to always
        create a perfect cycle

        from: http://stackoverflow.com/questions/273567/secret-santa-algorithm
        """
        random.shuffle(people)
        partners = deque(people)
        partners.rotate()
        return dict(zip(people, partners))

    def make_giftees(self, group):
        """
        :param group: The group to make the pairing
        :return: the dict of secret-santa pairing
        """
        listUsers = self.get_by_group(group)
        return self.pairup(list(listUsers))

    def save_giftees(self, giftees):
        """
        It's necessary to persist the value of "send_to" of every user
        :param giftees: the dict of secret-santa pairing
        """
        for user in giftees:
            user.send_to = giftees[user].name
            user.save()


    def get_giftee(self, user):
        """
        This service provide a pairing of whole group. If a user hasn't "send_to" value, that means the algorithm needs to be run.
        :param user: The user to get the
        :return: the receiver name
        """
        if user.isEmpty_send_to():
            giftees = self.make_giftees(user.group)
            self.save_giftees(giftees)
            user.send_to = giftees[user].name
            return user.send_to
        else:
            return user.send_to

class UserSender(models.Model):
    name = models.CharField(
        _('name'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'and @/./+/-/_ characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    age = models.IntegerField(_("Age"))
    group = models.CharField(_("Group"), max_length=255)
    send_to = models.CharField(_("Send_to"), max_length=255)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    objects = UserSenderManager()

    GROUP_FIELD = 'group'
    NAME_FIELD = 'name'

    def isEmpty_send_to(self):
        if self.send_to:
            return False
        else:
            return True

    def __str__(self):
        return self.name + " - " + str(self.age)

    class Meta:
        verbose_name = _("UserSender")
        verbose_name_plural = _("UserSenders")


