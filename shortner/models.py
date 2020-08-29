from django.db import models

# Create your models here.


class Link(models.Model):
    shortlink = models.CharField(
        'shortened url given by user',
        max_length=200,
        unique=True,
        primary_key=True)
    longlink = models.CharField('long url', max_length=350)

    def __str__(self):
        return str({"shortlink": self.shortlink, 'longlink': self.longlink})

    def getDict(self):
        return {
            "shortlink": self.shortlink,
            "longlink": self.longlink
        }
