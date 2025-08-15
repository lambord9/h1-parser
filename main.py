import asyncio
import re
from graphql_client import fetch_reports_async
from storage import init_db, is_new_report, save_report, is_db_empty
from telegram_client import send_message
from config import CHECK_INTERVAL


def escape_markdown(text: str) -> str:
    import re

    escape_chars = r"\_*[]()~`>#+-=|{}.!<>"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


def escape_markdown(text: str) -> str:
    escape_chars = r"\_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


def format_report(report):
    title = escape_markdown(report["title"])
    reporter = escape_markdown(report["reporter"])
    team = escape_markdown(report["team"])
    severity = escape_markdown(str(report.get("severity", "unknown")))
    award = escape_markdown(str(report.get("award", 0)))
    created = escape_markdown(report.get("created", "unknown"))
    disclosed = escape_markdown(report.get("disclosed", "unknown"))
    url = escape_markdown(report["url"])
    return (
        f"*New h1 report was disclosed*\n"
        f"*{title}*\n"
        f"👤 Reporter: *{reporter}*\n"
        f"🏢 Team: *{team}*\n"
        f"💰 Award: {award}$\n"
        f"⚠️ Severity: *{severity}*\n"
        f"📅 Created: `{created}`\n"
        f"📢 Disclosed: `{disclosed}`\n"
        f"{url}"
    )


async def first_run_fill_db():
    reports = await fetch_reports_async()
    for r in reversed(reports):
        save_report(r)
    print(f"Добавлено {len(reports)} репортов в базу")


async def main():
    init_db()

    # if is_db_empty():
    #     await first_run_fill_db()

    while True:
        try:
            reports = await fetch_reports_async()
            new_reports = [r for r in reversed(reports) if is_new_report(r["id"])]

            for r in new_reports:
                save_report(r)
                await send_message(format_report(r))

        except Exception as e:
            print(f"Ошибка: {e}")

        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
