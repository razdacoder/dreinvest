from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT", "USDT"),
        ("LTC", "Litecoin"),
        ("USDC", "USDC"),
        ("DOGE", "Dogecoin"),
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
    status = models.CharField(max_length=255, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} Transaction made by {self.user.first_name} of ${self.amount} {self.asset}"


class Proof(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    file = models.FileField(upload_to="proofs/")

    def __str__(self):
        return f"Proof of {self.transaction.user.first_name} Transaction"


class Investment(models.Model):
    INVESTMENT_PLAN = (
        ("basic", "Basic Plan"),
        ("standard", "Standard Plan"),
        ("professionl", "Professional Plan"),
        ("expert", "Expert Plan"),
        ("executive", "Executice Plan"),
    )

    ASSET_TYPE = (
        ("BTC", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("USDT", "USDT"),
        ("LTC", "Litecoin"),
        ("USDC", "USDC"),
        ("DOGE", "Dogecoin"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=255, choices=INVESTMENT_PLAN)
    asset = models.CharField(max_length=255, choices=ASSET_TYPE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Investment of ${self.amount} for {self.get_plan_display()}"


@receiver(post_save, sender=Transaction)
def status_changed(sender, instance, created, **kwargs):
    if not created:
        obj = Transaction.objects.get(pk=instance.pk)
        if obj.status == "sucessfull" and obj.type == "deposit":
            obj.user.wallet_balance += obj.amount
        elif obj.status == "sucessfull" and obj.type == "withdraw":
            obj.user.wallet_balance -= obj.amount
        obj.user.save()
