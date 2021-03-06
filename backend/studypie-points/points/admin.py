import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum
from django.db.models.functions import (
    TruncDay,
    ExtractYear,
    ExtractWeek,
    TruncMonth,
    TruncWeek,
)
from django.http import JsonResponse, Http404
from django.urls import path

from .models import PointDefinition, PointIssued, PointConsumed


@admin.register(PointDefinition)
class PointDefinitionAdmin(admin.ModelAdmin):
    pass


@admin.register(PointIssued)
class PointIssuedAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "point",
        "remained_point",
        "expire_at",
        "created_at",
        "user",
    )

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = self.chart_daily()

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        # NOTE! Our custom urls have to go before the default urls, because they
        # default ones match anything.
        return extra_urls + urls

    def chart_data_endpoint(self, request):
        unit = request.GET.get("unit", None)
        if unit == "daily" or unit == None:
            chart_data = self.chart_daily()
        elif unit == "weekly":
            chart_data = self.chart_weekly()
        elif unit == "monthly":
            chart_data = self.chart_monthly()
        else:
            return Http404()
        return JsonResponse(list(chart_data), safe=False)

    def chart_daily(self):
        return (
            PointIssued.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Sum("point"))
            .order_by("-date")
        )

    def chart_weekly(self):
        return (
            PointIssued.objects.annotate(date=TruncWeek("created_at"))
            .values("date")
            .annotate(y=Sum("point"))
            .order_by("-date")
        )

    def chart_monthly(self):
        return (
            PointIssued.objects.annotate(date=TruncMonth("created_at"))
            .values("date")
            .annotate(y=Sum("point"))
            .order_by("-date")
        )

admin.site.register(PointConsumed)
