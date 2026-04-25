from langchain.tools import tool
from rag import run_rag_query

crops = {
    "wheat": 0.8,
    "corn": 1.0,
    "vegetables": 0.7
}

@tool
def irrigation_knowledge(query: str) -> str:
    """
    Use this tool when the user asks for explanations, definitions, 
    or general knowledge about irrigation concepts, 
    such as ET0, crop coefficient, water efficiency, etc.
    Do Not use for calculations.
    """
    return run_rag_query(query)

@tool
def irrigation_volume_tool(area_m2: float, et0_mm: float, crop_coefficient: float = None, crop: str = None) -> dict:
    """
    This tool is to retrieve the irrigation volume from a specific crop, size of the land, and the rate of water loss.
    Use this tool ONLY when the user asks to calculate irrigation volume.
    Requires numeric inputs: area_m2, crop_coefficient, et0_mm.
    
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
    if crop is not None:
        crop = crop.lower()
        if crop not in crops:
            raise ValueError(f"Unknown crop: {crop}")
        kc = crops[crop]
    elif crop_coefficient is not None:
        kc = crop_coefficient
    else:
        raise ValueError("Provide either crop or crop_coefficient")

    # --- Input Validation ---
    if area_m2 <= 0:
        raise ValueError("area_m2 must be positive.")
    if kc <= 0:
        raise ValueError("crop_coefficient must be positive.")
    if et0_mm <= 0:
        raise ValueError("et0_mm must be positive.")
    # --- Core Logic ---
    liters = area_m2 * kc * et0_mm
    liters = round(liters, 2)
    detail = f"irrigation volume = ({area_m2} m^2) * ({kc}) * ({et0_mm} mm) = {liters} liters"

    return {"result": liters, "unit": "liters", "detail": detail}