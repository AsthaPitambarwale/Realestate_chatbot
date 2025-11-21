from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from .utils import (
    load_dataset,
    match_areas_from_query,
    generate_mock_summary,
    generate_comparison_summary,
    generate_price_growth_summary,
    make_chart_json,
    DATA_CACHE
)
from django.conf import settings
import pandas as pd
import io
import os
import re
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Real Estate API is running"})

OPENAI_KEY = getattr(settings, "OPENAI_API_KEY", None)
if OPENAI_KEY:
    try:
        import openai
        openai.api_key = OPENAI_KEY
    except Exception:
        openai = None


class UploadDataset(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, format=None):
        f = request.FILES.get('file')
        if not f:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            df = load_dataset(f)
            DATA_CACHE["df"] = df
            return Response({"message": "File uploaded and parsed", "rows": len(df)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAreas(APIView):
    def get(self, request):
        df = DATA_CACHE.get("df")
        if df is None:
            return Response({"areas": []}, status=status.HTTP_200_OK)

        for c in ['area', 'locality', 'location', 'name']:
            if c in df.columns:
                area_col = c
                break
        else:
            area_col = df.columns[0]

        areas = sorted(df[area_col].dropna().astype(str).unique().tolist())
        return Response({"areas": areas}, status=status.HTTP_200_OK)


class QueryAnalysis(APIView):
    def post(self, request):
        payload = request.data
        query = payload.get('query', '').strip()

        if not query:
            return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

        df = DATA_CACHE.get("df")
        if df is None:
            sample_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample.xlsx')
            if os.path.exists(sample_path):
                df = load_dataset(sample_path)
            else:
                return Response({"error": "No dataset loaded"}, status=status.HTTP_400_BAD_REQUEST)

        # detect area column
        for c in ['area', 'locality', 'location', 'name']:
            if c in df.columns:
                area_col = c
                break
        else:
            area_col = df.columns[0]

        # extract areas from query
        areas = match_areas_from_query(query, df)

        if not areas:
            parts = [p.strip() for p in re.split(r',| and | & | vs | v\.? | versus ', query.lower())]
            detected = []
            for p in parts:
                if not p:
                    continue
                mask_part = df[area_col].astype(str).str.contains(p, case=False, na=False)
                detected.extend(df[mask_part][area_col].astype(str).unique().tolist())
            areas = list(dict.fromkeys([a for a in detected if a and str(a).lower() != "nan"]))

        if not areas:
            areas = df[area_col].dropna().astype(str).unique().tolist()[:3]

        # FILTER DF
        mask = pd.Series(False, index=df.index)
        for a in areas:
            mask = mask | df[area_col].astype(str).str.contains(str(a), case=False, na=False)
        df_filtered = df[mask].copy()
        df_filtered = df_filtered.replace([float('inf'), float('-inf')], pd.NA).fillna(0)

        # BUILD CHART JSON
        chart_json = make_chart_json(df_filtered)

        # SAFE table preview
        table_preview = df_filtered.head(200).replace([pd.NA], 0).to_dict(orient='records')

        # DETECT QUERY TYPE
        query_lower = query.lower()
        summary = ""
        comparison_summary = None

        # 1️⃣ Price growth query
        if any(x in query_lower for x in ["price growth", "price increase", "last 3 years", "price trend"]):
            summary = generate_price_growth_summary(df, areas[0], years=3)

        # 2️⃣ Comparison query
        elif len(areas) >= 2 and any(x in query_lower for x in ["compare", " vs ", " versus "]):
            summary = generate_comparison_summary(df, areas[:2])
            comparison_summary = summary  # optional duplicate key

        # 3️⃣ Default single area summary
        else:
            summary = generate_mock_summary(df_filtered, areas)

        result = {
            "query": query,
            "areas": areas,
            "summary": summary,
            "chart": chart_json,
            "table": table_preview,
            "rows": len(df_filtered)
        }

        if comparison_summary:
            result["comparison_summary"] = comparison_summary

        return Response(result)


class DownloadCSV(APIView):
    def get(self, request):
        df = DATA_CACHE.get("df")
        if df is None:
            return Response({"error": "No dataset loaded"}, status=status.HTTP_400_BAD_REQUEST)

        area = request.GET.get('area')
        if area:
            for c in ['area', 'locality', 'location', 'name']:
                if c in df.columns:
                    col = c
                    break
            mask = df[col].astype(str).str.contains(area, case=False, na=False)
            df_out = df[mask]
        else:
            df_out = df

        df_out = df_out.fillna("")
        buf = io.StringIO()
        df_out.to_csv(buf, index=False)
        buf.seek(0)

        response = Response(buf.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="filtered_data.csv"'
        return response
