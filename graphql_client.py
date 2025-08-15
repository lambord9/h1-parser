import aiohttp
from config import GRAPHQL_URL, GRAPHQL_QUERY, GRAPHQL_VARIABLES, HEADERS


async def fetch_reports_async():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            GRAPHQL_URL,
            json={
                "operationName": "HacktivitySearchQuery",
                "query": GRAPHQL_QUERY,
                "variables": GRAPHQL_VARIABLES,
            },
            headers=HEADERS,
        ) as resp:
            data = await resp.json()

    nodes = data.get("data", {}).get("search", {}).get("nodes", [])
    reports = []
    for node in nodes:
        report_data = node.get("report", {})

        reports.append(
            {
                "id": node.get("id") or report_data.get("databaseId"),
                "title": report_data.get("title", ""),
                "url": report_data.get("url", ""),
                "reporter": node.get("reporter", {}).get("username", "unknown"),
                "severity": node.get("severity_rating", "Unknown"),
                "team": node.get("team", {}).get("handle", "unknown"),
                "award": node.get("total_awarded_amount") or 0,
                "disclosed": report_data.get("disclosed_at"),
                "created": report_data.get("created_at"),
            }
        )
    return reports
