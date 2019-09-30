""" Router for Rest """

from rest_framework import routers
from task.views import ProjectList

router = routers.DefaultRouter()
router.register(r'projects', ProjectList)
