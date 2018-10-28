
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    #home and setup
    path('', views.index, name='index'),
    path('control_panel/', views.control_panel, name='control_panel'),
    path('signout', views.signout, name='signout'),
    path('log_in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    #settings
    path('sensor/', views.page_sensor, name='page_sensor'),
    path('venue/', views.page_venue, name='page_venue'),
    path('sensor_data/<int:game_id>/',views.sensor_data, name='sensor_data'),
    #test_urls
    path('data_vis/<int:room_id>/', views.data_vis, name='data_vis'),
    path('live_monitor/<int:game_id>/', views.live_monitoring, name='live_monitor'),
    #ajax functions
    path('api/upload_process/', views.upload_process,name='upload_process'),
    path('api/update_plot/', views.update_plot, name='update_plot'),
    path('api/get_sensor_by_room_id/<int:room_id>/', views.get_sensors_by_room_id, name='get_sensors_by_room_id'),
    path('api/get_room_by_room_id/<int:room_id>/', views.get_room_by_room_id, name='get_room_by_room_id'),
    path('api/game_cur_logs/<int:game_id>/', views.game_cur_logs, name='game_cur_logs'),
    path('admin/', admin.site.urls),
    #reports
    path('reports/room_analysis', views.room_analysis, name='room_analysis'),
    path('reports/room_details_analysis', views.room_details_analysis, name='room_details_analysis'),
    path('reports/sensor_analysis', views.sensor_analysis,name='sensor_analysis'),
    path('reports/trend_analysis', views.trend_analysis, name='trend_analysis'),

    #testinging

    path('sample_marker', views.sample_marker, name='sample_marker')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)