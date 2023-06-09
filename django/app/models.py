from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser



# classes
class UserProfileManager(BaseUserManager):
    """
        کلاس منیجر کاربر
    """
    def create_user(self ,first_name, last_name, mobile_number, password = None):
        """
            برای ذخیره کاربر عادی
        """
        user = self.model(first_name = first_name, last_name = last_name, mobile_number = mobile_number)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, mobile_number, password):
        """
            برای ذخیره کاربر ادمین
        """
        user = self.create_user(first_name, last_name, mobile_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfileModel(AbstractBaseUser , PermissionsMixin):
    """
        مدل کاربر
    """
    first_name = models.CharField(max_length = 25 , null = True, default = None) # نام کاربر
    last_name = models.CharField(max_length = 25 , null = True, default = None) # نام خانوادگی کاربر
    mobile_number = models.CharField(max_length = 11 ,unique = True ,null = True ,validators=[
        RegexValidator(
            regex='^[0][9][0-9]*$',
            message='قالب شماره موبایل رعایت نشده است',
            code='invalid_phone_number'
        ),
    ]) # شماره تماس کاربر
    parking = models.ForeignKey('ParkingModel', on_delete = models.CASCADE, null = True, default = None) # پارکینگ کابر مربوطه

    is_staff = models.BooleanField(default=False) # کابر میتواند پنل ادمین را ببیند
    is_active = models.BooleanField(default=True) # ایا کاربر فعال است
    # کلاس منیجر
    objects = UserProfileManager()

    USERNAME_FIELD = 'mobile_number' # نام کاربری
    REQUIRED_FIELDS = ['first_name', 'last_name'] # فیلد های تکراری

    def __str__(self):

        return str(self.id) + ' - ' + str(self.mobile_number)
    
    
class ParkingModel(models.Model):
    """
        موجودیت پارکینگ
    """
    name = models.CharField(max_length = 25) # نام پارکینگ
    capacity = models.IntegerField(validators = [MinValueValidator(limit_value = 1)]) # ظرفیت پاکینگ
    

class ParkingSpaceFloorModel(models.Model):
    """
        موجودیت طبقه پارکینگ
    """
    name = models.CharField(max_length = 1) # نام طبقه
    parking = models.ForeignKey('ParkingModel', on_delete = models.CASCADE, related_name = 'floors') # پارکینگ مورد نظر
    
    
class ParkingSpaceRowModel(models.Model):
    """
        موجودیت ردیف پارکینگ
    """
    number = models.IntegerField(validators = [MinValueValidator(limit_value = 1)]) # شماره ردیف
    floor = models.ForeignKey('ParkingSpaceFloorModel', on_delete = models.CASCADE, related_name = 'rows') # طبقه مربوطه
    
    
class ParkingSpaceNumberModel(models.Model):
    """
        موجودیت مکان پارک
    """
    number = models.IntegerField(validators = [MinValueValidator(limit_value = 1)]) # شماره مکان پارک
    row = models.ForeignKey('ParkingSpaceRowModel', on_delete = models.CASCADE, related_name = 'numbers') # ردیف پارک
    is_full = models.BooleanField(default = False) # ایا مکان پارک پر است
    
    
class TicketModel(models.Model):
    """
        موجودیت بلیت
    """
    driver_name = models.CharField(max_length = 25) # نام راننده
    driver_national_code = models.CharField(max_length = 10) # شماره ملی راننده
    driver_phone_number = models.CharField(max_length = 11, validators = [
        RegexValidator(
            regex='^[0][9][0-9]*$',
            message='قالب شماره موبایل رعایت نشده است',
            code='invalid_phone_number'
        ),
    ]) # شماره همراه راننده
    plate = models.CharField(max_length = 6, default = 0) # شماره پلاک
    parking_number = models.ForeignKey('ParkingSpaceNumberModel', on_delete = models.CASCADE, related_name = 'tickets') # شماره پارکینگ