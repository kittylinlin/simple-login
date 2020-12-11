from djongo import models


class Status(models.TextChoices):
    ACTIVE = 'active'
    PENDING = 'pending'


class Role(models.TextChoices):
    NORMAL = 'normal'
    ADMIN = 'admin'


class User(models.Model):
    ACTIVE_STATUS = 'active'
    PENDING_STATUS = 'pending'
    STATUS_CHOICES = (
        (ACTIVE_STATUS, 'active'),
        (PENDING_STATUS, 'pending'),
    )

    NORMAL_ROLE = 'normal'
    ADMIN_ROLE = 'admin'
    ROLE_CHOICES = (
        (NORMAL_ROLE, 'normal'),
        (ADMIN_ROLE, 'admin'),
    )

    _id = models.ObjectIdField()
    account = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=ACTIVE_STATUS)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default=NORMAL_ROLE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    last_login_time = models.DateTimeField()

    class Meta:
        db_table = 'users'
