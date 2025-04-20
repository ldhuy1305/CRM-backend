from django.urls import include, re_path
from rest_framework.routers import SimpleRouter

from lead.views import LeadViewSet, LeadSourceViewSet, LeadStatusViewSet, IndustryViewSet

router = SimpleRouter()
router.register(r"leads", LeadViewSet, "leads")
router.register(r"lead-sources", LeadSourceViewSet, "lead_sources")
router.register(r"lead-statuses", LeadStatusViewSet, "lead_statuses")
router.register(r"industries", IndustryViewSet, "industries")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]
