from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Profile(BaseModel):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=55)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"


class SubscriptionPlan(BaseModel):
    BILLING_CYCLE_CHOICES = (
        ("Monthly", "Monthly"),
        ("Quarterly", "Querterly"),
        ("Yearly", "Yearly"),
    )
    name = models.CharField(max_length=45, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=15, choices=BILLING_CYCLE_CHOICES)
    trail_period_days = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - BillingCycle: {self.billing_cycle} - Trail: {self.trail_period_days} days"


class Subscription(BaseModel):
    SUBSCRIPTION_STATUS_CHOICES = (
        ("Active", "Active"),
        ("Canceled", "Canceled"),
        ("Expired", "Expired"),
        ("Paused", "Paused"),
    )
    profile_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    plan_id = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=SUBSCRIPTION_STATUS_CHOICES)
    is_auto_renew = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.profile_id} - {self.plan_id} - {self.status}"


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("Success", "Success"),
        ("Failed", "Failed"),
        ("Pending", "Pending"),
    )
    PAYMENT_METHOD_CHOICES = (
        ("CreditCard", "CreditCard"),
        ("PayPal", "PayPal"),
        ("Gpay", "Gpay"),
        ("PhonePe", "PhonePe"),
        ("DebitCard", "DebitCard"),
    )
    profile_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    subscription_id = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    payment_status = models.CharField(max_length=25, choices=PAYMENT_STATUS_CHOICES)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=455, unique=True)
    payment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class Invoice(models.Model):
    INVOICE_STATUS_CHOICES = (
        ("Paid", "Paid"),
        ("Unpaid", "Unpaid"),
        ("Overdue", "Overdue"),
    )
    profile_id = models.ForeignKey(Profile, on_delete=models.PROTECT)
    subscription_id = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    invoice_number = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=INVOICE_STATUS_CHOICES)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
