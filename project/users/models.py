from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                name="unique_email"
            )]

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)


class UserEnrollment(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
