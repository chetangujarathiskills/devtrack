import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Reporter,
    Issue,
    CriticalIssue,
    LowPriorityIssue
)


@csrf_exempt
def reporters(request):

    # =========================
    # CREATE REPORTER
    # =========================

    if request.method == "POST":

        try:
            data = json.loads(request.body)

            reporter = Reporter(
                data["id"],
                data["name"],
                data["email"],
                data["team"]
            )

            reporter.validate()

        except KeyError as e:
            return JsonResponse(
                {"error": f"Missing field: {e.args[0]}"},
                status=400
            )

        except ValueError as e:
            return JsonResponse(
                {"error": str(e)},
                status=400
            )

        with open("reporters.json", "r") as f:
            reporters_data = json.load(f)

        reporters_data.append(reporter.to_dict())

        with open("reporters.json", "w") as f:
            json.dump(
                reporters_data,
                f,
                indent=4
            )

        return JsonResponse(
            reporter.to_dict(),
            status=201
        )

    # =========================
    # GET REPORTERS
    # =========================

    elif request.method == "GET":

        with open("reporters.json", "r") as f:
            reporters_data = json.load(f)

        reporter_id = request.GET.get("id")

        # GET /api/reporters/?id=1
        if reporter_id:

            try:
                reporter_id = int(reporter_id)

            except ValueError:
                return JsonResponse(
                    {"error": "ID must be an integer"},
                    status=400
                )

            for reporter in reporters_data:

                if reporter["id"] == reporter_id:
                    return JsonResponse(
                        reporter,
                        status=200
                    )

            return JsonResponse(
                {"error": "Reporter not found"},
                status=404
            )

        # GET /api/reporters/
        return JsonResponse(
            reporters_data,
            safe=False,
            status=200
        )

    # =========================
    # OTHER METHODS
    # =========================

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )


@csrf_exempt
def issues(request):

    # =========================
    # CREATE ISSUE
    # =========================

    if request.method == "POST":

        try:
            data = json.loads(request.body)

            priority = data["priority"]

            # Choose the correct class
            if priority == "critical":

                issue = CriticalIssue(
                    data["id"],
                    data["title"],
                    data["description"],
                    data["status"],
                    data["priority"],
                    data["reporter_id"]
                )

            elif priority == "low":

                issue = LowPriorityIssue(
                    data["id"],
                    data["title"],
                    data["description"],
                    data["status"],
                    data["priority"],
                    data["reporter_id"]
                )

            else:

                issue = Issue(
                    data["id"],
                    data["title"],
                    data["description"],
                    data["status"],
                    data["priority"],
                    data["reporter_id"]
                )

            # Validate object
            issue.validate()

        except KeyError as e:

            return JsonResponse(
                {"error": f"Missing field: {e.args[0]}"},
                status=400
            )

        except ValueError as e:

            return JsonResponse(
                {"error": str(e)},
                status=400
            )

        # Read existing issues
        with open("issues.json", "r") as f:
            issues_data = json.load(f)

        # Add new issue
        issues_data.append(issue.to_dict())

        # Save to JSON
        with open("issues.json", "w") as f:
            json.dump(
                issues_data,
                f,
                indent=4
            )

        # Prepare response
        response_data = issue.to_dict()

        response_data["message"] = issue.describe()

        return JsonResponse(
            response_data,
            status=201
        )

    # =========================
    # GET ISSUES
    # =========================

    elif request.method == "GET":

        with open("issues.json", "r") as f:
            issues_data = json.load(f)

        issue_id = request.GET.get("id")
        status_filter = request.GET.get("status")

        # GET /api/issues/?id=1
        if issue_id:

            try:
                issue_id = int(issue_id)

            except ValueError:

                return JsonResponse(
                    {"error": "ID must be an integer"},
                    status=400
                )

            for issue in issues_data:

                if issue["id"] == issue_id:

                    response_data = issue.copy()

                    # Recreate correct object so describe()
                    # works correctly
                    if issue["priority"] == "critical":

                        issue_object = CriticalIssue(
                            issue["id"],
                            issue["title"],
                            issue["description"],
                            issue["status"],
                            issue["priority"],
                            issue["reporter_id"]
                        )

                    elif issue["priority"] == "low":

                        issue_object = LowPriorityIssue(
                            issue["id"],
                            issue["title"],
                            issue["description"],
                            issue["status"],
                            issue["priority"],
                            issue["reporter_id"]
                        )

                    else:

                        issue_object = Issue(
                            issue["id"],
                            issue["title"],
                            issue["description"],
                            issue["status"],
                            issue["priority"],
                            issue["reporter_id"]
                        )

                    response_data["message"] = issue_object.describe()

                    return JsonResponse(
                        response_data,
                        status=200
                    )

            return JsonResponse(
                {"error": "Issue not found"},
                status=404
            )

        # GET /api/issues/?status=open
        if status_filter:

            filtered_issues = []

            for issue in issues_data:

                if issue["status"] == status_filter:
                    filtered_issues.append(issue)

            return JsonResponse(
                filtered_issues,
                safe=False,
                status=200
            )

        # GET /api/issues/
        return JsonResponse(
            issues_data,
            safe=False,
            status=200
        )

    # =========================
    # OTHER METHODS
    # =========================

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )