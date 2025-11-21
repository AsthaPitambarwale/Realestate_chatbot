import pandas as pd
import numpy as np
import re
from collections import defaultdict
from django.conf import settings
import os
import io

# --------------------------------------------------------------------
# IN-MEMORY CACHE
# --------------------------------------------------------------------
DATA_CACHE = {
    "df": None,
    "last_path": None
}

# --------------------------------------------------------------------
# LOAD DATASET + COLUMN NORMALIZATION + NAN HANDLING
# --------------------------------------------------------------------
def load_dataset(path_or_file=None):
    """Load Excel and normalize columns based on your dataset structure."""

    if path_or_file is None and DATA_CACHE["df"] is not None:
        return DATA_CACHE["df"]

    # Read Excel
    if hasattr(path_or_file, "read"):
        df = pd.read_excel(path_or_file, engine='openpyxl')
    else:
        df = pd.read_excel(path_or_file, engine='openpyxl')

    # Normalize headers
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Convert numeric columns automatically where possible
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors="ignore")
        except Exception:
            pass

    # Forced numeric conversion for known numeric fields
    numeric_cols = [
        'year', 'loc_lat', 'loc_lng',
        'total_sales - igr', 'total sold - igr',
        'flat_sold - igr', 'office_sold - igr', 'others_sold - igr',
        'shop_sold - igr', 'commercial_sold - igr', 'other_sold - igr',
        'residential_sold - igr',
        'flat - weighted average rate', 'office - weighted average rate',
        'others - weighted average rate', 'shop - weighted average rate',
        'total units', 'total carpet area supplied (sqft)',
        'flat total', 'shop total', 'office total', 'others total'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sanitize NaN & infinite values
    df = df.replace([np.inf, -np.inf], np.nan)

    DATA_CACHE["df"] = df
    return df


# --------------------------------------------------------------------
# AREA MATCHING (IMPROVED)
# --------------------------------------------------------------------
def match_areas_from_query(query, df):
    """Extract locality names from user text with fuzzy logic."""
    if not isinstance(query, str):
        return []

    query = query.lower().strip()

    # detect area column
    for c in ['area', 'locality', 'location', 'name']:
        if c in df.columns:
            area_col = c
            break
    else:
        area_col = df.columns[0]

    unique_areas = df[area_col].dropna().astype(str).unique()
    unique_areas_lower = [a.lower() for a in unique_areas]

    matches = []

    # Direct substring match
    for area, area_low in zip(unique_areas, unique_areas_lower):
        if area_low in query:
            matches.append(area)

    # Word-level fuzzy match
    if not matches:
        words = re.findall(r'[A-Za-z]+', query)
        for w in words:
            w_low = w.lower()
            for area, area_low in zip(unique_areas, unique_areas_lower):
                if w_low and w_low in area_low:
                    matches.append(area)

    # Multi-area split by common separators
    if not matches:
        parts = re.split(r',| and | & | vs | v\.? | versus ', query)
        for p in parts:
            p = p.strip()
            if not p:
                continue
            for area, area_low in zip(unique_areas, unique_areas_lower):
                if p in area_low or area_low in p:
                    matches.append(area)

    matches = list(dict.fromkeys(matches))  # remove duplicates
    return matches


# --------------------------------------------------------------------
# SINGLE AREA SUMMARY
# --------------------------------------------------------------------
def generate_mock_summary(df_filtered, areas):
    """Generate a professional market-style summary for the given areas."""
    if df_filtered is None or df_filtered.empty:
        return f"No market records found for: {', '.join(areas)}."

    area_label = ", ".join(areas)
    summary = []

    # Header
    summary.append(f"Market Overview for {area_label}.")

    # Year Coverage
    if "year" in df_filtered.columns:
        years_raw = df_filtered['year'].dropna().unique().tolist()
        years = []
        for y in years_raw:
            try:
                years.append(int(y))
            except Exception:
                pass
        years = sorted(years)
        if years:
            summary.append(f"The dataset covers {years[0]} to {years[-1]}, offering a multi-year view of performance.")
        else:
            summary.append("Year information is limited or unavailable.")

    # Demand & Sales Trends
    sales_fields = {
        'flat_sold - igr': "Residential Flats",
        'shop_sold - igr': "Shops",
        'office_sold - igr': "Offices",
        'others_sold - igr': "Other Units"
    }

    demand_lines = []
    for col, label in sales_fields.items():
        if col in df_filtered.columns:
            yearly = df_filtered.groupby('year')[col].sum().replace({np.nan: 0})
            if len(yearly) > 1:
                start = int(yearly.iloc[0]) if pd.notna(yearly.iloc[0]) else 0
                end = int(yearly.iloc[-1]) if pd.notna(yearly.iloc[-1]) else 0
                trend_word = "increased" if end > start else ("declined" if end < start else "remained stable")
                pct = ((end - start) / start * 100) if start not in [0, None] else 0
                demand_lines.append(f"{label}: {trend_word} from {start} units to {end} units ({pct:.1f}%).")

    if demand_lines:
        summary.append("Demand & Sales Trends:")
        summary.extend(demand_lines)

    # Pricing / Rate Insights
    price_fields = {
        'flat - weighted average rate': "Residential Flat Rates",
        'shop - weighted average rate': "Shop Rates",
        'office - weighted average rate': "Office Rates",
        'others - weighted average rate': "Other Property Rates"
    }

    price_lines = []
    for col, label in price_fields.items():
        if col in df_filtered.columns:
            avg_rate = df_filtered[col].mean()
            if pd.notna(avg_rate):
                price_lines.append(f"{label} average is approximately ₹{avg_rate:,.0f} per sq.ft.")

    if price_lines:
        summary.append("Pricing Insights:")
        summary.extend(price_lines)

    # Supply Overview
    if "total units" in df_filtered.columns:
        avg_supply = df_filtered["total units"].mean()
        if pd.notna(avg_supply):
            summary.append(f"Average annual supply is {avg_supply:,.0f} units, indicating development activity levels.")

    # Conclusion
    summary.append(f"Overall, {area_label} demonstrates market dynamics driven by supply and demand, useful for investment and planning decisions.")

    return "\n".join(summary)


# --------------------------------------------------------------------
# TWO-AREA COMPARISON
# --------------------------------------------------------------------
def generate_comparison_summary(df, areas):
    """Generate a concise comparative summary for the given areas."""
    if not areas or len(areas) < 2:
        return "Comparison requires at least two areas."

    # detect area column
    for c in ['area', 'locality', 'location', 'name']:
        if c in df.columns:
            area_col = c
            break
    else:
        area_col = df.columns[0]

    available_areas = df[area_col].dropna().astype(str).unique().tolist()
    chosen = []
    for a in areas:
        matches = [x for x in available_areas if x.lower() == str(a).lower()]
        if not matches:
            matches = [x for x in available_areas if str(a).lower() in x.lower()]
        if matches:
            chosen.append(matches[0])

    if len(chosen) < 2:
        return f"Could not find sufficient data for comparison for: {', '.join(areas)}"

    header = f"Demand Trend Comparison: {chosen[0]} vs {chosen[1]}"
    lines = [header]

    sales_cols = {
        'flat_sold - igr': "Residential Flats",
        'shop_sold - igr': "Shops",
        'office_sold - igr': "Offices",
        'others_sold - igr': "Other Units"
    }

    for col, label in sales_cols.items():
        if col not in df.columns:
            continue
        area_lines = []
        for area in chosen[:2]:
            df_area = df[df[area_col].astype(str).str.lower() == area.lower()]
            if df_area.empty:
                continue
            yearly = df_area.groupby('year')[col].sum().replace({np.nan: 0})
            if len(yearly) > 1:
                start = int(yearly.iloc[0]) if pd.notna(yearly.iloc[0]) else 0
                end = int(yearly.iloc[-1]) if pd.notna(yearly.iloc[-1]) else 0
                pct = ((end - start) / start * 100) if start not in [0, None] else 0
                trend_word = "increased" if end > start else ("declined" if end < start else "stable")
                area_lines.append(f"{area}: {trend_word} from {start} → {end} ({pct:.1f}%)")
        if area_lines:
            lines.append(f"{label}:")
            lines.extend([f"- {l}" for l in area_lines])

    lines.append("Conclusion: Comparison based on available multi-year demand patterns; use with contextual local knowledge.")
    return "\n".join(lines)


# --------------------------------------------------------------------
# PRICE GROWTH SUMMARY
# --------------------------------------------------------------------
def generate_price_growth_summary(df, area, years=3):
    """Generate price growth summary for a single area over the last N years."""
    if not area or df is None or df.empty:
        return f"No data available for {area}."

    # detect area column
    for c in ['area', 'locality', 'location', 'name']:
        if c in df.columns:
            area_col = c
            break
    else:
        area_col = df.columns[0]

    df_area = df[df[area_col].astype(str).str.lower() == area.lower()]
    if df_area.empty:
        return f"No data available for {area}."

    # Take last N years
    if "year" not in df_area.columns or 'flat - weighted average rate' not in df_area.columns:
        return f"Insufficient data for price growth analysis for {area}."

    df_area = df_area[['year', 'flat - weighted average rate']].dropna()
    df_area = df_area.sort_values("year", ascending=True)
    last_years = df_area['year'].drop_duplicates().sort_values(ascending=False).head(years).sort_values()
    df_area = df_area[df_area['year'].isin(last_years)]

    if df_area.empty:
        return f"No price data available for {area} in the last {years} years."

    start_price = df_area.iloc[0]['flat - weighted average rate']
    end_price = df_area.iloc[-1]['flat - weighted average rate']
    if pd.isna(start_price) or pd.isna(end_price):
        return f"No price data available for {area} in the last {years} years."

    trend_word = "increased" if end_price > start_price else ("declined" if end_price < start_price else "remained stable")
    pct_change = ((end_price - start_price) / start_price * 100) if start_price != 0 else 0

    summary = (
        f"Price Growth Summary for {area} over the last {years} years:\n"
        f"Residential flat rates {trend_word} from ₹{start_price:,.0f} per sq.ft to ₹{end_price:,.0f} per sq.ft ({pct_change:.1f}%)."
    )
    return summary


# --------------------------------------------------------------------
# CHART GENERATOR (ROBUST + ALWAYS SAFE)
# --------------------------------------------------------------------
def make_chart_json(df_filtered):
    """Generate safe chart JSON for line chart."""
    if df_filtered is None or df_filtered.empty:
        return {"labels": [], "datasets": []}

    if "year" not in df_filtered.columns:
        return {"labels": [], "datasets": []}

    numeric_cols = [
        'flat_sold - igr', 'office_sold - igr', 'shop_sold - igr', 'others_sold - igr',
        'flat - weighted average rate', 'office - weighted average rate',
        'shop - weighted average rate', 'others - weighted average rate',
        'total units'
    ]

    existing = [c for c in numeric_cols if c in df_filtered.columns]
    if not existing:
        return {"labels": [], "datasets": []}

    group = (
        df_filtered.groupby("year")[existing]
        .mean()
        .reset_index()
        .dropna(subset=["year"])
        .sort_values("year")
    )

    labels = []
    for y in group["year"]:
        try:
            labels.append(int(y))
        except Exception:
            labels.append(0)

    datasets = []
    for col in existing:
        col_values = []
        for x in group[col]:
            if pd.isna(x) or np.isinf(x):
                col_values.append(0)
            else:
                try:
                    col_values.append(float(x))
                except:
                    col_values.append(0)
        datasets.append({
            "label": col,
            "data": col_values
        })

    return {
        "labels": labels,
        "datasets": datasets
    }
