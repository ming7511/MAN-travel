from django.urls import path
from .views import kimi_chat_view,get_weather_for_trip,get_photo,kimi_chat_view_style,add_place_activity,get_trip_activities,update_activity,delete_activity,create_trip,set_trip_days

urlpatterns = [
    path('AiCreateUrls/', kimi_chat_view, name='url创建'),
    path('Weather/', get_weather_for_trip, name='天气预报'),
    path('GetPhoto/', get_photo, name='获取图片'),
    path('AiCreateStyles/', kimi_chat_view_style, name='根据风格创建'),
    path('add_place_activity/', add_place_activity, name='add_place_activity'),
    path('get_trip_activities/', get_trip_activities, name='get_trip_activities'),
    path('update_activity/', update_activity, name='update_activity'),
    path('delete_activity/', delete_activity, name='delete_activity'),
    path('create_trip/', create_trip, name='create_trip'),
    path('set_trip_days/',set_trip_days, name='set_trip_days'),

]