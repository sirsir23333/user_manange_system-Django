from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your CustomUserManager here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, firstName, lastName, role, company, designation, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName,
            role=role,
            company=company,
            designation=designation,
            **extra_fields
        )

        user.set_password(password)
        # ensure that the password is hashed, it is called when the user register. Called by serializer.save() in view.
        user.save(using=self._db)
        return user

    def create_user(self, email, password, firstName, lastName, role, company, designation, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, firstName, lastName, role, company, designation, **extra_fields)

    def create_superuser(self, email, password, firstName, lastName, role, company, designation, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, firstName, lastName, role, company, designation, **extra_fields)


# Create your User Model here.
''' Customized User model, because i want to use the methods in it, but i also want to
add in and delete some of the fields. I also override save() method to let ADMIN equivalent
to staff user. Notice that even though we customize User Model, we do not need to define ID field as
it is define in other method. Same as for password, we also need not to define for the same reason.
'''


class User(AbstractBaseUser, PermissionsMixin):
    # Abstractbaseuser has password, last_login, is_active by default
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    # db_index=True: This indicates that the email field should be indexed in the database to improve performance when querying by email.
    role_choices = [
        ('ADMIN', 'Admin'),
        ('MEMBER', 'Member'),
        ('TECHNICIAN', 'Technician')
    ]
    role = models.CharField(max_length=32, choices=role_choices, null=False, blank=False)
    firstName = models.CharField(max_length=240)
    lastName = models.CharField(max_length=255)

    company = models.CharField(max_length=250, null=True, blank=True)
    designation = models.CharField(max_length=250, null=True, blank=True)

    is_staff = models.BooleanField(default=False)  # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=True)  # must needed, otherwise you won't be able to loginto django-admin.
    is_superuser = models.BooleanField(default=False)  # this field we inherit from PermissionsMixin.

    def save(self, *args, **kwargs):
        if self.role == 'ADMIN':
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)
        # to ensure the parent class AbstractBaseUser's is also called

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # instead of username being the login field, we use email
    REQUIRED_FIELDS = ['firstName', 'lastName', 'role', 'company', 'designation']
    # what needs to be input when register, some can leave blank as set above

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
