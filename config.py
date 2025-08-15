from dotenv import load_dotenv
import os
from aiogram.enums import ParseMode

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PARSE_MODE = ParseMode.MARKDOWN_V2

GRAPHQL_URL = "https://hackerone.com/graphql"

GRAPHQL_QUERY = """
query HacktivitySearchQuery($queryString: String!, $from: Int, $size: Int, $sort: SortInput!) {
  search(
    index: CompleteHacktivityReportIndex
    query_string: $queryString
    from: $from
    size: $size
    sort: $sort
  ) {
    nodes {
      ... on HacktivityDocument {
        id
        reporter { username }
        report {
          title
          url
          disclosed_at
          created_at
        }
        severity_rating
        team { handle }
        total_awarded_amount
        disclosed
      }
    }
  }
}
"""

GRAPHQL_VARIABLES = {
    "queryString": "disclosed:true",
    "from": 0,
    "size": 25,
    "sort": {"field": "latest_disclosable_activity_at", "direction": "DESC"},
}

HEADERS = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

CHECK_INTERVAL = 600
