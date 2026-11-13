from pathlib import Path
import pandas as pd


def analyze_stress_data(file_path):
    path = Path(file_path)

    if not path.exists():
        return {"success": False, "error": "Data file not found"}

    df = pd.read_csv(path)

    required = [
        "heart_rate",
        "eda",
        "skin_temperature",
        "movement"
    ]

    if not all(col in df.columns for col in required):
        return {"success": False, "error": "Missing sensor columns"}

    result = {
        "success": True,
        "participant": df["participant"].iloc[0],
        "records": len(df),
        "data_source": "PhysioNet STRESS - f14_b",
        "status": "Experimental data analysis",
        "signals": {}
    }

    for column in required:
        result["signals"][column] = {
            "average": round(float(df[column].mean()), 3),
	    "minimum": round(float(df[column].min()), 3),
	    "maximum": round(float(df[column].max()), 3)
            
            
        }

    return result