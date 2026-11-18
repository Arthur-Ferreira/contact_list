from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r"^[0-9+()\-]+$",
    message="Phone may contain only digits, +, ( ) and -.",
)


class Contact(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, validators=[phone_validator])
    email = models.EmailField()

    class Meta:
        ordering = ["name", "id"]

    def clean_fields(self, exclude=None):
        self.name = (self.name or "").strip()
        self.phone = (self.phone or "").strip()
        self.email = (self.email or "").strip()
        super().clean_fields(exclude)

    def __str__(self):
        return self.name