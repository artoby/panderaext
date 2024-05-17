import pandas as pd
from pandera.extensions import register_check_method


@register_check_method()
def is_sorted_ascending(series: pd.Series) -> bool:
    return series.is_monotonic_increasing


@register_check_method()
def is_single_value(series: pd.Series) -> bool:
    return series.nunique() == 1
