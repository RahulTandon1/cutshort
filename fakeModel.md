```python3
from django.db import models

# Create your models here.


class Link(models.Model):
    shortLink = models.CharField(
        'shortened url given by user',
        max_length=200,
        unique=True,
        primary_key=True)
    longLink = models.CharField('long url', max_length=350)

    def __str__(self):
        return str({"shortlink": self.shortLink, 'longLink': self.longLink})
```
