import os
import requests
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")
API_VERSION = os.getenv("META_API_VERSION", "v19.0")
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def validate_env_vars():
    if not all([ACCESS_TOKEN, AD_ACCOUNT_ID]):
        raise ValueError("필수 환경 변수가 설정되지 않았습니다: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID")

def get_campaigns() -> Dict[str, str]:
    validate_env_vars()
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "id,name,effective_status"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        campaigns = data.get("data", [])
        return {c["name"]: c["id"] for c in campaigns if c["effective_status"] == "ACTIVE"}
    except requests.exceptions.RequestException as e:
        print(f"❌ Meta Campaigns API 실패: {str(e)}")
        return {}

def get_meta_insights(campaign_names_to_ids: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    validate_env_vars()
    results = {}
    for name, campaign_id in campaign_names_to_ids.items():
        url = f"{BASE_URL}/{campaign_id}/insights"
        params = {
            "access_token": ACCESS_TOKEN,
            "fields": "clicks,reach",
            "date_preset": "last_30d",
            "level": "campaign"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get("data", [])
            if data:
                insights = data[0]
                results[name] = {
                    "clicks": int(insights.get("clicks", 0)),
                    "reach": int(insights.get("reach", 0))
                }
            else:
                results[name] = {"clicks": 0, "reach": 0}

            print(f"▶ 캠페인: {name}")
            print("▶ 요청 URL:", url)
            print("▶ 요청 Params:", params)
            print("▶ 응답 JSON:", response.json())
        except requests.exceptions.RequestException as e:
            print(f"❌ Meta Insights API 실패 ({name}): {str(e)}")
            results[name] = {"clicks": 0, "impressions": 0, "spend": 0}
    return results