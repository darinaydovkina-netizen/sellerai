import json
import logging
import re

import anthropic

from config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Ты профессиональный маркетолог маркетплейсов. Пользователь даёт тебе название "
    "или ссылку на товар и выбирает нужные инструменты. Ты отвечаешь ТОЛЬКО валидным "
    'JSON без markdown-обёртки. Структура: {"title": "...", "description": "...", '
    '"keywords": {"high": [], "mid": [], "low": []}, "review_positive": "...", '
    '"review_negative": "...", "photo_ideas": [], "competitor_analysis": '
    '{"strengths": [], "weaknesses": [], "recommendations": []}, "ad_text": "..."}. '
    "Генерируй только те поля, которые запрошены. Пиши на русском языке. "
    "Без воды и клише — только конкретика."
)

FIELDS_MAP = {
    "title": "title",
    "description": "description",
    "keywords": "keywords",
    "reviews": "review_positive, review_negative",
    "photos": "photo_ideas",
    "competitors": "competitor_analysis",
    "ad": "ad_text",
}


async def generate_content(product: str, tools: list[str], marketplace: str) -> dict:
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    tools_str = "\n".join([f"- {t}" for t in tools])
    user_message = (
        f"Товар: {product}\n"
        f"Маркетплейс: {marketplace}\n\n"
        f"Сгенерируй следующие поля:\n{tools_str}"
    )

    logger.info("Calling Anthropic API for product: %s", product)

    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    content = response.content[0].text
    logger.info("Anthropic API response received")

    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", content)
    if match:
        content = match.group(1).strip()

    result = json.loads(content)

    requested_fields = set()
    for tool in tools:
        if tool in FIELDS_MAP:
            for field in FIELDS_MAP[tool].split(", "):
                requested_fields.add(field)

    return {k: v for k, v in result.items() if k in requested_fields}
