from django.db import models
import random
import string


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        print(self.generate_random_string())
        # Save the original name before saving the model instance
        self.name = self.name
        self.path = self.generate_random_string(15)
        super().save(*args, **kwargs)

    def generate_random_string(self, length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
