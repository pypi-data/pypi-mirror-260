from django.core.exceptions import ValidationError
from django.core.signals import request_started
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel
from netbox.models import NestedGroupModel, PrimaryModel
from netbox.models.features import ContactsMixin
from utilities.choices import ChoiceSet
try:
    from netbox_subsystems.models import System, Subsystem
    SYSTEM = True
except:
    SYSTEM = False


class SystemRole(ContactsMixin, NestedGroupModel):
    name = models.CharField(
        verbose_name="название",
        max_length=250,
        unique=True,
        help_text='Укажите имя, которое будет отображаться для этой рооли.'
    )

    system = models.ForeignKey(
        verbose_name="система",
        to=System,
        on_delete=models.CASCADE,
        related_name='role',
        blank=True,
        null=True
    )
    subsystems = models.ManyToManyField(
        Subsystem,
        related_name='roles',
        verbose_name="Подсистема"
    )
    data_composition = models.CharField(
        verbose_name="Состав данных",
        max_length=500,
        blank=True
    )
    upload_interface = models.CharField(
        verbose_name="Интерфейс выгрузки",
        max_length=200,
        blank=True
    )
    upload_format = models.CharField(
        verbose_name="Форма выгрузки",
        max_length=100,
        blank=True
    )
    mapping_security_group = models.CharField(
        verbose_name="Mapping SecurityGroup",
        max_length=1000,
        blank=True
    )
    sed = models.CharField(
        verbose_name="СЭД",
        max_length=500,
        blank=True
    )
    link = models.CharField(
        verbose_name="FSLink",
        max_length=300,
        blank=True
    )
    description = models.CharField(
        verbose_name="Описание",
        max_length=1000,
        blank=True
    )

    slug = models.SlugField(
        verbose_name="короткий URL",
        max_length=100,
        unique=True
    )

    comments = models.TextField(
        verbose_name="комментарий",
        blank=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Роли систем"
        verbose_name = "Роль систем"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_rolesandgroups:systemrole', args=[self.pk])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # self.get_system_if_exists()
        # if self.subsystem and not self.system:
        #     self.system = self.subsystem.system

    @receiver(post_save, sender='netbox_rolesandgroups.SystemRole')
    def get_system_if_exists(sender, instance, created, **kwargs):
        if not created and not instance.system and instance.subsystems:
            # print(instance.subsystems)
            # print(instance.subsystems.split(','))
            # system = System.objects.filter(id__in=[subsystems.system.id for subsystems in instance.subsystems.all()])
            instance.system = [subsystems.system for subsystems in instance.subsystems.all()][0]
            instance.save()
        return


class TechRole(PrimaryModel):
    name = models.CharField(
        verbose_name="название",
        max_length=250,
        unique=True,
        help_text='Укажите имя, которое будет отображаться для этой группы.'
    )
    slug = models.SlugField(
        verbose_name="короткий URL",
        max_length=100,
        unique=True
    )
    roles = models.ManyToManyField(
        SystemRole,
        related_name='techroles',
        verbose_name="Роли"
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Технические роли систем"
        verbose_name = "Техническая роль систем"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_rolesandgroups:techrole', args=[self.pk])
