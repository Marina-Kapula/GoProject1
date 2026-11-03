
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

from .models import Week, WorkDay


def home(request):
    weeks = Week.objects.prefetch_related("days").order_by("id")

    saved_weeks = []

    for week in weeks:
        saved_weeks.append({
            "number": week.number,
            "activities": week.activities,
            "days": [
                {
                    "date": day.date.isoformat() if day.date else "",
                    "schedule": day.schedule,
                    "tutor_signature": day.tutor_signature,
                }
                for day in week.days.all()
            ],
        })

    return render(request, "pages/home.html", {
        "saved_weeks": saved_weeks
    })


@csrf_exempt
@require_POST
def save_week(request):
    try:
        data = json.loads(request.body)
        weeks_data = data.get("weeks", [])

        if not weeks_data:
            return JsonResponse(
                {"success": False, "error": "No weeks to save"},
                status=400
            )

        with transaction.atomic():
            Week.objects.all().delete()

            for item in weeks_data:
                week = Week.objects.create(
                    number=int(item.get("number") or 1),
                    activities=item.get("activities", "")
                )

                for day in item.get("days", []):
                    WorkDay.objects.create(
                        week=week,
                        date=day.get("date") or None,
                        schedule=day.get("schedule", ""),
                        tutor_signature=day.get("tutor_signature", "")
                    )

        return JsonResponse({"success": True})

    except Exception as error:
        return JsonResponse(
            {"success": False, "error": str(error)},
            status=400
        )
