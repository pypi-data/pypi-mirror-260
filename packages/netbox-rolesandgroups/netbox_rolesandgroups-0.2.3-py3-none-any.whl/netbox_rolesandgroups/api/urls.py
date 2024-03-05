from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_rolesandgroups'

router = NetBoxRouter()
router.register('systemrole', views.SystemRoleViewSet)
router.register('techrole', views.TechRoleViewSet)

urlpatterns = router.urls
