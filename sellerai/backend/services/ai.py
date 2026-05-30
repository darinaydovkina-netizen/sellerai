import json
import logging
import re

import httpx
from httpx import HTTPStatusError, RequestError

from config import settings

logger = logging.getLogger(__name__)

YANDEX_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

SYSTEM_PROMPT = (
    "Ты профессиональный маркетолог маркетплейсов. Пользователь даёт тебе название "
    "или ссылку на товар и выбирает нужные инструменты. Ты отвечаешь ТОЛЬКО валидным "
    "JSON без markdown-обёртки. Структура: {\"title\": \"...\", \"description\": \"...\", "
    "\"keywords\": {\"high\": [], \"mid\": [], \"low\": []}, \"review_positive\": \"...\", "
    "\"review_negative\": \"...\", \"photo_ideas\": [], \"competitor_analysis\": "
    "{\"strengths\": [], \"weaknesses\": [], \"recommendations\": []}, \"ad_text\": \"...\"}. "
    "Генерируй только те поля, которые запрошены. Пиши на русском языке. "
    "Без воды и клише — только конкретика."
)

FIELDS_MAP = {
    "title": "title",
    "description": "description",
    "keywords": "keywords",
    "reviews": "review_positive, review_negative",
    "review_answers": "review_positive, review_negative",
    "photos": "photo_ideas",
    "photo_ideas": "photo_ideas",
    "competitors": "competitor_analysis",
    "competitor_analysis": "competitor_analysis",
    "ad": "ad_text",
}


def _clean_json(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return raw.strip()


async def generate_content(product: str, tools: list[str], marketplace: str) -> dict:
    tools_str = "\n".join([f"- {t}" for t in tools])
    user_message = (
        f"Товар: {product}\n"
        f"Маркетплейс: {marketplace}\n\n"
        f"Сгенерируй следующие поля:\n{tools_str}"
    )

    model_uri = f"gpt://{settings.yandex_folder_id}/yandexgpt/latest"

    payload = {
        "modelUri": model_uri,
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "4000",
        },
        "messages": [
            {"role": "system", "text": SYSTEM_PROMPT},
            {"role": "user", "text": user_message},
        ],
    }

    headers = {
        "Authorization": f"Api-Key {settings.yandex_api_key}",
        "Content-Type": "application/json",
    }

    logger.info("Calling YandexGPT for product: %s", product)

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(YANDEX_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except HTTPStatusError as e:
        logger.error("YandexGPT HTTP error: %s - %s", e.response.status_code, e.response.text)
        raise RuntimeError(f"YandexGPT API вернул ошибку {e.response.status_code}")
    except RequestError as e:
        logger.error("YandexGPT request failed: %s", e)
        raise RuntimeError("Не удалось подключиться к YandexGPT API")

    logger.info("YandexGPT response received")

    raw = data["result"]["alternatives"][0]["message"]["text"]
    cleaned = _clean_json(raw)

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error("YandexGPT JSON parse error: %s | raw=%s", e, cleaned[:500])
        raise RuntimeError("YandexGPT вернул невалидный JSON")

    requested_fields = set()
    for tool in tools:
        if tool in FIELDS_MAP:
            for field in FIELDS_MAP[tool].split(", "):
                requested_fields.add(field)

    return {k: v for k, v in result.items() if k in requested_fields}
