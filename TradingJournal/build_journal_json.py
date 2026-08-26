"""
TradingJournal/build_journal_json.py
Generates TradingJournal/journal.json from journal_engine calculations.
"""
import json
from pathlib import Path
from datetime import datetime
from TradingJournal.journal_engine import build_master_journal


def build_journal_json():
    print("Building master trading journal JSON...")
    
    # 1. Fetch normalized trade log history from engine
    journal_logs = build_master_journal()
    
    # 2. Package into JSON payload with ISO timestamp
    payload = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_records": len(journal_logs),
        "journal": journal_logs
    }
    
    # 3. Write output to TradingJournal/journal.json
    output_path = Path(__file__).parent / "journal.json"
    with open(output_path, "w") as f:
        json.dump(payload, f, indent=4)
        
    print(f"Successfully generated {output_path} with {len(journal_logs)} entries.")


if __name__ == "__main__":
    build_journal_json()