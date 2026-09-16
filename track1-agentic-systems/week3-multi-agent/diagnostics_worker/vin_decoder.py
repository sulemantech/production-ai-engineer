import requests


VPIC_BASE_URL = "https://vpic.nhtsa.dot.gov"


def decode_vin_code(vin: str) -> dict:
    """
    Decode a VIN code and return vehicle information.

    Always returns the same response structure regardless of
    success, warning, or failure.
    """
    result = {
        "vin": vin,
        "make": None,
        "model": None,
        "year": None,
        "vehicle_type": None,
        "body_class": None,
        "engine_cylinders": None,
        "fuel_type_primary": None,
        "plant_city": None,
        "decode_error": None,
        "decode_warning": None,
    }

    try:
        url = f"{VPIC_BASE_URL}/api/vehicles/decodevinvalues/{vin}"

        response = requests.get(
            url,
            params={"format": "json"},
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        results = data.get("Results", [])

        if not results:
            result["decode_error"] = (
                "No vehicle information found for this VIN."
            )
            return result

        item = results[0]

        # The important validation:
        # If Make is empty, the API didn't provide usable vehicle data.
        if not item.get("Make"):
            result["decode_error"] = (
                item.get("ErrorText")
                or "VIN could not be decoded."
            )
            return result

        # We have usable vehicle data, so keep it even if vPIC
        # reports a warning such as a checksum mismatch.
        result.update({
            "make": item.get("Make"),
            "model": item.get("Model"),
            "year": item.get("ModelYear"),
            "vehicle_type": item.get("VehicleType"),
            "body_class": item.get("BodyClass"),
            "engine_cylinders": item.get("EngineCylinders"),
            "fuel_type_primary": item.get("FuelTypePrimary"),
            "plant_city": item.get("PlantCity"),
        })

        error_code = item.get("ErrorCode")
        error_text = item.get("ErrorText")

        if error_code and error_code != "0":
            result["decode_warning"] = error_text

        return result

    except requests.exceptions.RequestException as e:
        result["decode_error"] = str(e)
        return result