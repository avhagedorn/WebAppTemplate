import datetime
from typing import List
from typing import Tuple

from project_name.db.models import Transaction


def split_by_date(data: List[Transaction], split_date: datetime) -> Tuple[List, List]:
    lower = []
    higher = []

    for item in data:
        item_date = item.purchased_at.date()
        if item_date < split_date:
            lower.append(item)
        else:
            higher.append(item)

    return lower, higher
