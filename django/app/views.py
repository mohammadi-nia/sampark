from app import models, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated


# functions
@api_view(http_method_names = 'get')
# @permission_classes(permission_classes=[IsAuthenticated])
def get_parking_full_spaces_number(request):
    """
        ای پی ای دریافت تعداد مکان های پر در پارکینگ
    """
    try:
        full_parking_spaces = models.ParkingSpaceNumberModel.objects.filter(is_full = False) # پارکینگ هایی که خالی هستند
        return Response(data = {'count':len(full_parking_spaces)}, status = status.HTTP_200_OK)
    except:
        return Response(data={'detail':'مشکلی پیش امده است'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(http_method_names = 'post')
# @permission_classes(permission_classes=[IsAuthenticated])
def create_ticket(request):
    """
        ای پی ای ساخت بلیت
    """
    ticket_data = serializers.CreateTicketSerializer(data = request.data) # داده های دریافتی از کلاینت
    ticket_data.is_valid(raise_exception = True)
    ticket_valid_data = ticket_data.validated_data # داده های ارزیابی شده
    
    try:
        parking_spaces = models.ParkingSpaceNumberModel.objects.filter(
                is_full = False,
                number = ticket_valid_data['parking_number'],
                row__number = ticket_valid_data['parking_row'],
                row__floor__name = ticket_valid_data['parking_floor'],
            ) # مکان پارک های خالی
        # اگر مکان پارک خالی وجود ندارد
        if not parking_spaces:
            return Response(data={'detail':'مکان پارکی با این مشخصات یافت نشد یا این مکان پارک پر است'}, status = status.HTTP_400_BAD_REQUEST)
        
        # تغییر حالت مکان پارک
        parking_space = serializers.ParkingSpaceNumberSerializer(instance = parking_spaces.first()) # مکان پارک
        parking_space.is_full = True # پر بودن مکان پارک
        # ذخیره مکان پارک
        parking_space.save()
        
        # حذف و تغییر بعضی داده ها
        ticket_valid_data.pop('parking_row')
        ticket_valid_data.pop('parking_floor')
        ticket_valid_data['parking_number'] = parking_space.id
        
    except:
        return Response(data={'detail':'مشکلی پیش امده است'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    ticket = serializers.TicketSerializer(data = ticket_valid_data) # بلیت
    ticket.is_valid(raise_exception = True)
    
    try:
        # ذخیره بلیت
        ticket.save()
        return Response(data = ticket_data.validated_data, status = status.HTTP_201_CREATED)
    except:
        return Response(data={'detail':'مشکلی پیش امده است'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(http_method_names = 'post')
# @permission_classes(permission_classes=[IsAuthenticated])
def search(request):
    """
        ای پی ای جستجو
    """
    srz_data = serializers.SearchSerializer(data = request.data) # داده های دریافتی از کلاینت
    srz_data.is_valid(raise_exception = True)
    q = srz_data.validated_data['q'] # مقدار جستجو
    
    try:
        tickets = models.TicketModel.objects.all() # همه بلیت ها
        
        valid_tickets = tickets.filter(driver_national_code__icontains = q) # بلیت هایی با مشخصات مورد ارزیابی
        # بررسی مقدار سرچ در شماره تلفن است
        if not valid_tickets:
            valid_tickets = tickets.filter(driver_phone_number__icontains = q)
        # بررسی مقدار سرچ در نام است
        if not valid_tickets:
            valid_tickets = tickets.filter(driver_name__icontains = q)
        # بررسی اینکه مقدار سرچ در پلاک است
        if not valid_tickets:
            valid_tickets = tickets.filter(plate__icontains = q)
        # اگر هنوز مقداری پیدا نشده است
        if not valid_tickets:
            return Response(data={'detail':'خودرویی با این مشخصات در پارکینگ نیست'}, status = status.HTTP_400_BAD_REQUEST)
        
        ticket = valid_tickets.first() # بلیت
        
        ticket_srz_data = serializers.TicketSerializer(instance = ticket).data # داده های بلیت
        
        return_data = ticket_srz_data # داده های بازگشتی
        
        # اضافه کردن داده هایی به داده های بازگشتی 
        return_data['parking_floor'] = ticket.parking_number.row.floor.name
        return_data['parking_row'] = ticket.parking_number.row.number
        return_data['parking_number'] = ticket.parking_number.number
        
        return Response(data = return_data, status = status.HTTP_200_OK)
        
    except:
        return Response(data={'detail':'مشکلی پیش امده است'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# @api_view(http_method_names = 'delete')
# # @permission_classes(permission_classes=[IsAuthenticated])
# def delete_ticket(request, pk):
    