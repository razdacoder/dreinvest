from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email, password=password, first_name=first_name, last_name=last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    kyc_verified = models.BooleanField(default=True)
    btc_wallet = models.CharField(max_length=255)
    eth_wallet = models.CharField(max_length=255)
    usdt_wallet = models.CharField(max_length=255)
    ltc_wallet = models.CharField(max_length=255)
    usdc_wallet = models.CharField(max_length=255)
    doge_wallet = models.CharField(max_length=255)
    wallet_balance = models.FloatField(default=0.00)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Transaction(models.Model):
    TRANSACTION_TYPE = (("deposit", "Deposit"), ("withdraw", "Withdraw"))
    ASSET_TYPE = (
        ("btc", "Bitcoin"),
        ("eth", "Ethereum"),
        ("usdt", "USDT"),
        ("ltc", "Litecoin"),
        ("usdc", "USDC"),
        ("doge", "Dogecoin"),
    )

    STATUS = (
        ("pending", "Pending"),
        ("sucessfull", "Successfull"),
        ("failed", "Failed"),
    )
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    asset = models.CharField(max_length=255, choices=ASSET_TYPE)
    status = models.CharField(max_length=255, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
