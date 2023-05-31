from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rasa_action.urls')),
    path('', include('apnamd_ai.urls'))
]