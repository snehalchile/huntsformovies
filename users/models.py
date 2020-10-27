from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone

class AppUserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password,
                     is_staff, is_admin, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_admin=is_admin, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class AppUser(AbstractBaseUser):
    first_name = models.CharField(max_length=128, blank=False, null=True)
    last_name = models.CharField(max_length=128, blank=True, default='', null=True)
    mobile_no = models.CharField(max_length=10, blank=True, default='', null=True)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False, null=False, default='random')
    is_staff = models.BooleanField(default=False, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_agreed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)    

    class Meta:
        db_table = 'auth_user'

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['']

    objects = AppUserManager()

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

