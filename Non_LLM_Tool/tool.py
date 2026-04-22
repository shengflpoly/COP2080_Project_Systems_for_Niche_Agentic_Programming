# tool.py
# -------------------------------------------------------
# Tool Name : irrigation_volume
# Domain : Agriculture
# Author : Shengcong He
# Description: This tool computes the liters needed for a specific 
# crop for commercial crop growth efficiently and economically 
# with factors: the size of the land and the rate of water loss.
# Usage : See README.md for a sample call.
# -------------------------------------------------------

def irrigation_volume(area_m2: float, crop_coefficient: float, et0_mm: float) -> dict:
    """
    This tool is to retrieve the irrigation volume from a specific crop, size of the land, and the rate of water loss.

    Args:
        area_m2: The area of the land in m^2. 
        crop_coefficient: A factor to estimate a specific crop's water needs.
        et0_mm: The rate of water loss in mm.
    
    Returns:
        dict: {
            "result": <Primary computed value>
            "unit": <string label, liter>
            "detail": <explanation string>
        }
    Raises:
        ValueError: if any input is out of expected range or type.
    """
    # --- Input Validation ---
    if area_m2 <= 0:
        raise ValueError("area_m2 must be positive.")
    if crop_coefficient <= 0:
        raise ValueError("crop_coefficient must be positive.")
    if et0_mm <= 0:
        raise ValueError("eto_mm must be positive.")
    # --- Core Logic ---
    liters = area_m2 * crop_coefficient * et0_mm
    liters = round(liters, 2)
    detail = f"irrigation volume = ({area_m2} m^2) * ({crop_coefficient}) * ({et0_mm} mm) = {liters} liters"

    return {"result": liters, "unit": "liters", "detail": detail}
