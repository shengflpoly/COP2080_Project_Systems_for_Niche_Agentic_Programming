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

from langchain.tools import tool
import streamlit as st

crops = {

    

}

@tool
def irrigation_volume(_: str) -> dict:
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

    area_m2 = st.session_state.area
    crop_coefficient = st.session_state.crop_coefficient
    et0_mm = st.session_state.et0

    # --- Input Validation ---
    if area_m2 <= 0:
        raise ValueError("area must be positive.")
    if crop_coefficient <= 0:
        raise ValueError("crop_coefficient must be positive.")
    if et0_mm <= 0:
        raise ValueError("et0 must be positive.")
    # --- Core Logic ---
    liters = area_m2 * crop_coefficient * et0_mm
    liters = round(liters, 2)
    detail = f"irrigation volume = ({area_m2} m^2) * ({crop_coefficient}) * ({et0_mm} mm) = {liters} liters"

    return {"result": liters, "unit": "liters", "detail": detail}
