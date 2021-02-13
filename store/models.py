from django.db import models
import datetime



class Categary(models.Model):
    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_categary():
        return Categary.objects.all()


    def __str__(self):
        return self.name



class Products(models.Model):
    name= models.CharField(max_length=50)
    price= models.IntegerField(default=0)
    categary= models.ForeignKey(Categary,on_delete=models.CASCADE ,default=1)
    description= models.TextField()
    image=models.ImageField(upload_to='products')

    @staticmethod
    def get_all_product_by_id(ids):
        return Products.objects.filter(id__in = ids)

    @staticmethod
    def get_all_product():
        return Products.objects.all()

    @staticmethod
    def get_all_product_by_catery_id(Categary_id):
        if Categary_id:
            return Products.objects.filter(categary=Categary_id)
        else:
            return Products.get_all_product()



class Custmer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    c_password =models.CharField(max_length=500)


    def register(self):
        self.save()



    @staticmethod
    def get_email_for_check(email):
        #return Custmer.objects.get(email=email)
        try:
            return Custmer.objects.get(email=email)
        except:
            return False




    #if email exist
    def isExist(self):
        if Custmer.objects.filter(email=self.email):
            return True
        return False



class Order(models.Model):
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Custmer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default = False)



    def orderplace(self):
        return self.save()


    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order\
            .objects\
            .filter(customer = customer_id)\
    .order_by('-date')

