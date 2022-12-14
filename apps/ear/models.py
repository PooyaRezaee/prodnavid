from django.db import models

class IpLog(models.Model):
    ip_addr = models.CharField(max_length=20)
    route = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_addr
    
class BlockListIp(models.Model):
    ip = models.CharField(max_length=20)

    def __str__(self):
        return self.ip