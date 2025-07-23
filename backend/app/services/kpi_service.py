from typing import List, Dict

# In a real application these would query materialized views

def get_sales_daily(days: int = 7) -> List[Dict]:
    """Return mock sales data for last `days` days."""
    return [{"date": f"2024-01-{i:02d}", "amount": i * 100} for i in range(1, days + 1)]


def get_quotes_funnel() -> Dict:
    """Return mock quote funnel numbers."""
    return {"new": 10, "sent": 7, "won": 3}


def get_repairs_queue() -> Dict:
    """Return mock repairs queue size."""
    return {"pending": 5}
