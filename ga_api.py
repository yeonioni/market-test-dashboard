from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    Dimension,
    Metric,
    DateRange
)
from google.oauth2 import service_account
import os

def get_ga_client():
    credentials = service_account.Credentials.from_service_account_file(
        'ga_key.json',
        scopes=['https://www.googleapis.com/auth/analytics.readonly']
    )
    return BetaAnalyticsDataClient(credentials=credentials)

def get_ga_data(property_id, start_date="2024-01-01", end_date="today"):
    client = get_ga_client()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="unifiedPagePathScreen")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="engagedSessions"),
            Metric(name="totalUsers")
        ],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)]
    )

    response = client.run_report(request)

    result = []
    for row in response.rows:
        row_data = {
            "pagePath": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "engagedSessions": int(row.metric_values[1].value),
            "totalUsers": int(row.metric_values[2].value),
        }
        print("📊 GA 데이터:", row_data)  # ✅ 여기가 핵심!
        result.append(row_data)

    return result