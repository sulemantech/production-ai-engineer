import requests


NHTSA_BASE_URL = "https://api.nhtsa.gov"


def fetch_recalls(make: str, model: str, year: int) -> dict:
    try:
        response = requests.get(
            f"{NHTSA_BASE_URL}/recalls/recallsByVehicle",
            params={
                "make": make,
                "model": model,
                "modelYear": year,
            },
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        recalls = [
            {
                "campaign_number": item.get("NHTSACampaignNumber"),
                "component": item.get("Component"),
                "summary": item.get("Summary"),
                "consequence": item.get("Consequence"),
                "remedy": item.get("Remedy"),
                "report_date": item.get("ReportReceivedDate"),
            }
            for item in data.get("results", [])
        ]

        return {
            "make": make,
            "model": model,
            "year": year,
            "count": len(recalls),
            "recalls": recalls,
            "recalls_error": None,
        }

    except requests.RequestException as e:
        return {
            "make": make,
            "model": model,
            "year": year,
            "count": 0,
            "recalls": [],
            "recalls_error": str(e),
        }
    
def fetch_complaints(make: str, model: str, year: int) -> dict:
    """
    Fetch complaint information for a given vehicle make, model, and year.
    """
    try:
        response = requests.get(
            f"{NHTSA_BASE_URL}/complaints/complaintsByVehicle",
            params={
                "make": make,
                "model": model,
                "modelYear": year,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.Timeout:
        return {
            "make": make,
            "model": model,
            "year": year,
            "count": 0,
            "complaints": [],
            "complaints_error": "NHTSA API request timed out.",
        }

    except requests.exceptions.RequestException as exc:
        return {
            "make": make,
            "model": model,
            "year": year,
            "count": 0,
            "complaints": [],
            "complaints_error": (
                f"Unable to fetch complaint data from NHTSA: {exc}"
            ),
        }

    complaints = [
        {
            "odi_number": item.get("odiNumber"),
            "component": item.get("components"),
            "summary": item.get("summary"),
            "crash": item.get("crash"),
            "fire": item.get("fire"),
            "injuries": item.get("numberOfInjuries"),
            "deaths": item.get("numberOfDeaths"),
            "date": item.get("dateOfIncident"),
        }
        for item in data.get("results", [])
    ]

    return {
        "make": make,
        "model": model,
        "year": year,
        "count": len(complaints),
        "complaints": complaints,
        "complaints_error": None,
    }

def search_vehicle_issues(make: str, model: str, year: int) -> dict:
    """
    Search for vehicle issues (recalls and complaints)
    for a given make, model, and year.
    """
    recall_result = fetch_recalls(make, model, year)
    complaint_result = fetch_complaints(make, model, year)

    return {
        "vehicle": {
            "make": make,
            "model": model,
            "year": year,
        },
        "recalls": recall_result["recalls"],
        "recalls_error": recall_result["recalls_error"],
        "complaints": complaint_result["complaints"],
        "complaints_error": complaint_result["complaints_error"],
    }