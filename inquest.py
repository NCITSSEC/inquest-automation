import requests
import urllib3
import json
import sys
import re
import os

# SSL 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 제외할 문자열 (artifact에 포함 시 제거)
excluded_artifacts = {
    "safelinks.protection.outlook.com",
    "forms.office.com",
    "oauth2.googleapis.com",
    "google.com",
    "www.googletagmanager.com",
    "storage.googleapis.com",
    "www.w3.org",
    "www.youtube.com",
    "youtu.be",
    "th.bing.com",
    "openai.com",
    "huggingface.co",
    "weaviate.io",
    "msrc.microsoft.com",
    "docs.fortinet.com",
    "success.trendmicro.com",
    "www.elastic.co",
    "build.nvidia.com",
    "t.me",
    "x.com",
    "www.instagram.com",
    "www.bilibili.com",
    "github.com",
    "raw.github.com",
    "raw.githubusercontent.com",
    "marketplace.visualstudio.com",
    "bitbucket.org",
    "www.msftconnecttest.com",
    "1.1.1.1",
    "8.8.8.8",
    "52.167.249.196",
    "40.113.110.67",
    "157.240.215.174",
    "162.159.140.229",
    "d4a0fe56316a2c45b9ba9ac1005363309a3edc7acf9e4df64d326a0ff273e80f",
    "bd2c2cf0631d881ed382817afcce2b093f4e412ffb170a719e2762f250abfea4",
    "www.adobe.com",
    "www.clarity.ms",
    "www.baidu.com",
    "www.sogou.com",
    "steamcommunity.com",
    "wix.com",
    "s.go-mpulse.net",
    "slack.com",
    "52.196.128.139",
    "resources.trendmicro.com",
    "162.159.129.233",
    "162.159.134.233",
    "cdn.discordapp.com",
    "aws.amazon.com",
    "gmail.com",
    "www.nist.gov",
    "twitter.com",
    "slack.com",
    "onedrive.live.com"
    "en.wikipedia.org",
    "13.57.92.51",
    "151.101.2.137",
    "192.0.78.13",
    "192.124.249.10",
    "204.79.197.200",
    "52.167.249.196"    
}

# 제외할 타입
excluded_types = {"yarasignature", "url"}

# 요청
response = requests.get("https://labs.inquest.net/api/iocdb/list", verify=False)
response.raise_for_status()
json_data = response.json()

items = json_data.get("data", [])
seen_artifacts = set()
filtered_data = []

# 필터링
for item in items:
    if not isinstance(item, dict):
        continue

    artifact_type = item.get("artifact_type", "").lower()
    artifact = item.get("artifact", "").lower()

    if artifact_type in excluded_types:
        continue
    if any(excluded in artifact for excluded in excluded_artifacts):
        continue
    if artifact in seen_artifacts:
        continue

    seen_artifacts.add(artifact)

    if "reference_text" in item:
        item["reference_text"] = re.sub(r'\s+', ' ', item["reference_text"]).strip()

    filtered_data.append(item)

final_result = {
    "data": filtered_data,
    "success": True
}

# GitHub Actions에서 저장할 고정 경로 설정
output_path = "data/inquest_feed.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 결과를 한 줄로 저장 (minified JSON)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_result, f, ensure_ascii=False, separators=(',', ':'))
