
from pathlib import Path

from typing import Any

import yaml

def search_by_symptom(query: str) -> list[dict[str, Any]]:
    """
    Search for DTC entries that match a given symptom.

    Args:
        query (str): The symptom to search for.

    Returns:
        list[dict[str, Any]]: A list of DTC entries that match the symptom.
    """
    #TODO: Every file under data/generic should be searched for the symptom query. The search should be case-insensitive and should match any part of the symptom string.
    data_dir = Path(__file__).resolve().parent / Path("data/generic")
    dtc_entries = []
    for data_file in data_dir.glob("*.yaml"):
        data = load_dtc_data(data_file)
        for dtc_entry in data:
            symptoms = dtc_entry.get("symptoms", [])
            for symptom in symptoms:
                if query.lower() in symptom.get("en", "").lower():
                    dtc_entries.append(normalize_dtc(dtc_entry))
                    break  # No need to check other symptoms for this DTC entry

    # This is a placeholder implementation - you would need to implement the actual search logic
    return dtc_entries[:5]

def load_dtc_data(path:Path)-> list[dict[str, Any]]:
    """
    Load the DTC data from a YAML file.

    Args:
        path (Path): The path to the YAML file.

    Returns:
        list[dict]: The list of DTC entries.
    """
    with path.open("r",encoding="utf-8") as file:
        data = yaml.safe_load(file)
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of DTC entries, but got {type(data)}")
    
    return data

def get_data_file(dtc_code:str)->Path:
    """
    Get the data file name for a given DTC code.

    Args:
        dtc_code (str): The DTC code.

    Returns:
        str: The name of the data file.
    """
    dtc_prefix = dtc_code[:2]

    family_map ={
        "P0": "P0xxx_enriched.yaml",
        "P2": "P2xxx_enriched.yaml",
        "P3": "P3xxx_enriched.yaml",
        "B0": "B0xxx_enriched.yaml",
        "C0": "C0xxx_enriched.yaml",
        "U0": "U0xxx_enriched.yaml",
        "U3": "U3xxx_enriched.yaml"
    }

    data_file = family_map.get(dtc_prefix, "")
    if not data_file:
        raise ValueError(f"Invalid DTC code: {dtc_code}")
    return Path(__file__).resolve().parent / Path("data/generic") /  data_file

def find_dtc(dtc_code: str) -> dict[str, Any] | None:
    """
    Find the DTC entry for a given DTC code.

    Args:
        dtc_code (str): The DTC code to look up.

    Returns:
        dict[str, Any] | None: The DTC entry if found, otherwise None.
    """
    data_path = get_data_file(dtc_code)
    if not data_path:
        raise ValueError(f"Invalid DTC code: {dtc_code}")

    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    data = load_dtc_data(data_path)
    for dtc_entry in data:
        if dtc_entry.get("code") == dtc_code:
            return dtc_entry
    return None

def normalize_dtc(dtc_entry: dict[str, Any]) -> dict[str, Any]:
    """
    Convert a raw DTC entry into the application's standard output format.

    Args:
        dtc_entry: Raw DTC entry loaded from the OBDeX YAML data.

    Returns:
        The normalized DTC entry.
    """
    code = dtc_entry.get("code", "").strip().upper()

    common_causes = [
        {
            "id": cause.get("id"),
            "likelihood": cause.get("likelihood"),
            "label": cause.get("label", {}).get("en"),
        }
        for cause in dtc_entry.get("common_causes", [])
    ]

    symptoms = [
        symptom.get("en")
        for symptom in dtc_entry.get("symptoms", [])
    ]

    return {
        "code": code,
        "category": dtc_entry.get("category"),
        "title": dtc_entry.get("title", {}).get("en"),
        "description": dtc_entry.get("description", {}).get("en"),
        "affected_components": dtc_entry.get(
            "affected_components",
            [],
        ),
        "common_causes": common_causes,
        "symptoms": symptoms,
        "repair": dtc_entry.get(
            "repair",
            {},
        ),
        "flags": dtc_entry.get(
            "flags",
            {},
        ),
        "references": dtc_entry.get(
            "references",
            [],
        ),
        "related_codes": dtc_entry.get(
            "related_codes",
            [],
        ),
        "sources": dtc_entry.get(
            "sources",
            [],
        ),
        "family": f"{code[:2]}xxx",
    }
def search_dtc(dtc_code: str) -> dict[str, Any] | None:
    """
    Search for a DTC entry and return it in the standard format.
    """
    dtc_entry = find_dtc(dtc_code)

    if dtc_entry is None:
        return None

    return normalize_dtc(dtc_entry)