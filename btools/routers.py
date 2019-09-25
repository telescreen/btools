""" Router for Rest """

from rest_framework import routers
from task.views import ProjectViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
