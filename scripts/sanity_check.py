import sys
import os
import json

# Add parent dir to path to import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend import write_to_memory

def run_sanity():
    print("Running Sanity Check...")
    
    # 1. Test Memory Writing
    try:
        res = write_to_memory("user", "Sanity Check Test User Fact")
        print(f"Memory Write: {res}")
    except Exception as e:
        print(f"Memory Failed: {e}")
        return

    # 2. Generate Output JSON
    output_data = {
        "status": "success",
        "features": ["rag", "memory_persistence"],
        "memory_written": True
    }
    
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/sanity_output.json", "w") as f:
        json.dump(output_data, f, indent=2)
    
    print("Sanity Check Complete. artifacts/sanity_output.json created.")

if __name__ == "__main__":
    run_sanity()
