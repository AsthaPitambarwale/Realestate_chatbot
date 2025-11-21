from django.urls import path
from .views import UploadDataset, GetAreas, QueryAnalysis, DownloadCSV

urlpatterns = [
    path("upload/", UploadDataset.as_view(), name="upload-dataset"),
    path("areas/", GetAreas.as_view(), name="get-areas"),
    path("query/", QueryAnalysis.as_view(), name="query-analysis"),
    path("download/", DownloadCSV.as_view(), name="download-csv"),
]
