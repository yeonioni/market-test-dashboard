from flask import Flask, render_template, request
from meta_api import get_campaigns, get_meta_insights
from ga_api import get_ga_data
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        return render_template('match.html', campaigns=filter_campaigns_by_keyword(keyword), keyword=keyword)
    return render_template('index.html')

def filter_campaigns_by_keyword(keyword):
    all_campaigns = get_campaigns()
    return [c for c in all_campaigns if keyword.lower() in c.lower()]

@app.route('/match', methods=['POST'])
def match_campaigns():
    campaign_names = request.form.getlist('campaigns')
    keyword = request.form.get('keyword')
    matched_data = {}

    for i, campaign in enumerate(campaign_names):
        page_path = request.form.get(f"pagePath_{i+1}", "")
        purchase_clicks = int(request.form.get(f"purchaseClicks_{i+1}", 0))
        survey_completions = int(request.form.get(f"surveyCompletions_{i+1}", 0))
        matched_data[campaign] = {
            "pagePath": page_path,
            "purchaseClicks": purchase_clicks,
            "surveyCompletions": survey_completions
        }

    all_campaigns = get_campaigns()
    campaign_ids = {name: all_campaigns[name] for name in campaign_names}

    meta_data = get_meta_insights(campaign_ids)
    ga_data = get_ga_data(os.getenv("GA_PROPERTY_ID"))
    merged = merge_meta_ga(matched_data, meta_data, ga_data)

    return render_template('report.html', merged=merged, keyword=keyword)

def safe_div(numerator, denominator):
    return round((numerator / denominator) * 100, 2) if denominator else 0.0

def merge_meta_ga(matched_data, meta_data, ga_data):
    merged = []
    for campaign_name, matched in matched_data.items():
        page_path = matched.get("pagePath", "")
        purchase_clicks = matched.get("purchaseClicks", 0)
        survey_completions = matched.get("surveyCompletions", 0)
        meta = meta_data.get(campaign_name, {})
        ga = next((g for g in ga_data if g['pagePath'] == page_path), {})

        clicks = meta.get("clicks", 0)
        reach = meta.get("reach", 0)
        sessions = ga.get("sessions", 0)
        engaged = ga.get("engagedSessions", 0)
        users = ga.get("totalUsers", 0)

        merged.append({
            "campaign": campaign_name,
            "pagePath": page_path,
            "purchaseClicks": purchase_clicks,
            "surveyCompletions": survey_completions,
            "clicks": clicks,
            "reach": reach,
            "sessions": sessions,
            "engagedSessions": engaged,
            "totalUsers": users,

            # 🔽 계산 지표 추가
            "inflowRate": safe_div(clicks, reach),
            "purchaseRate": safe_div(purchase_clicks, clicks),
            "stayRate": safe_div(purchase_clicks, engaged),
            "surveyRate": safe_div(survey_completions, purchase_clicks)
        })
    return merged

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)