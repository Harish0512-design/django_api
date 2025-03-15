from django.contrib import admin
from app.models import Invoice, Payment, Profile, Subscription, SubscriptionPlan


# Register your models here.
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Subscription)
admin.site.register(Profile)
admin.site.register(SubscriptionPlan)
