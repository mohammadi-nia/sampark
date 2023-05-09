from django.contrib import admin
from app import models



admin.site.register(models.ParkingModel)
admin.site.register(models.ParkingSpaceFloorModel)
admin.site.register(models.ParkingSpaceRowModel)
admin.site.register(models.ParkingSpaceNumberModel)
admin.site.register(models.TicketModel)
admin.site.register(models.UserProfileModel)