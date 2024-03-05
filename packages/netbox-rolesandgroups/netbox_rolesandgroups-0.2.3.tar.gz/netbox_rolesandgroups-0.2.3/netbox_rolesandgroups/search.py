from netbox.search import SearchIndex
from .models import SystemRole, TechRole
from django.conf import settings

# If we run NB 3.4+ register search indexes 
if settings.VERSION >= '3.4.0':
    class SystemRoleIndex(SearchIndex):
        model = SystemRole
        fields = (
            ("name", 100),
            ("upload_interface", 110),
            ("upload_format", 120),
            ("mapping_security_group", 130),
            ("link", 140),
            ('data_composition', 200),
            ("slug", 500),
            ("description", 1000),
            ("comments", 5000),
        )

    class TechRoleIndex(SearchIndex):
        model = TechRole
        fields = (
            ("name", 100),
            ("slug", 500),
            ("comments", 5000),
        )

    # Register indexes
    indexes = [SystemRoleIndex, TechRoleIndex]
