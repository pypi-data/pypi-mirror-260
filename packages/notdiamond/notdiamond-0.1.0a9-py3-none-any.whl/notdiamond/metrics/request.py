import requests
from requests.models import Response


def feedback_request(feedback_payload: dict,
                     pipeline_id: str,
                     notdiamond_api_key: str):
    url = "base_url/v1/report/metrics/accuracy"

    payload = {
        "pipeline_id": pipeline_id,
        "metric": feedback_payload
    }

    headers = {
        "content-type": "application/json",
        "Authorization": f"Bearer {notdiamond_api_key}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
    except:
        response = Response()
        response.status_code = 200

    return response
