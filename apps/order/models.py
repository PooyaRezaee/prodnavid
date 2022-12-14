from django.db import models
from apps.accounts.models import User
from apps.beat.models import Beat

class Order(models.Model):
    order_code = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    beat = models.ForeignKey(Beat,on_delete=models.SET_DEFAULT,default=models.RESTRICT,related_name='order')
    sended = models.BooleanField(default=False)
    recived = models.BooleanField(null=True)
    price = models.PositiveIntegerField()
    report = models.CharField(max_length=256,blank=True,null=True)
    payment = models.OneToOneField('Payment',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def status_payment(self):
        status = None
        color = None
        match self.payment.status:
            case 'P':
                status = "Paid"
                color = 'success'
            case 'W':
                status = "Waiting"
                color = 'warning'
            case 'C':
                status = "Cancelled"
                color = 'danger'
        
        return (status,color)


class Payment(models.Model):
    STATUS_PAYMENT = [
        ('P','paid'),
        ('W','Waiting'),
        ('C','Cancelled'),
    ]

    status = models.CharField(max_length=1,choices=STATUS_PAYMENT,default='W')
    link = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.DateTimeField(blank=True,null=True)