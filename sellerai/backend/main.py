import json
import logging
import secrets
from contextlib import asynccontextmanager
from urllib.parse import urlencode, quote

import httpx
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select

from config import settings
from database import async_session, init_db, User, Tariff, Generation
from models import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    GenerateRequest,
    OAuthUrlRequest,
    UserResponse,
    TariffInfo,
    HistoryItem,
)
from services.auth import create_access_token, verify_token, hash_password, verify_password
from services.ai import generate_content

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    await init_db()
    yield


app = FastAPI(title="SellerAI API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:5500",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "https://sellerai.ru",
        "https://www.sellerai.ru",
        settings.frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    async with async_session() as session:
        user = await session.get(User, int(payload["sub"]))
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return user


@app.get("/")
async def root():
    return {"status": "ok", "service": "SellerAI API"}


@app.post("/auth/register", status_code=201)
async def register(req: RegisterRequest):
    if not req.email or not req.password:
        raise HTTPException(status_code=400, detail="Email и пароль обязательны")
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен быть не менее 6 символов")

    async with async_session() as session:
        existing = await session.execute(select(User).where(User.email == req.email))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

        hashed = hash_password(req.password)

        tariff = await session.execute(select(Tariff).where(Tariff.name == "starter"))
        starter = tariff.scalar_one()

        user = User(email=req.email, hashed_password=hashed, tariff_id=starter.id)
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return {"id": user.id, "email": user.email}


@app.post("/auth/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    if not req.email or not req.password:
        raise HTTPException(status_code=400, detail="Email и пароль обязательны")

    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == req.email))
        user = result.scalar_one_or_none()

    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return TokenResponse(access_token=token)


_oauth_states: dict[str, str] = {}
_oauth_request_count = 0


def _clean_oauth_states():
    global _oauth_request_count
    _oauth_request_count += 1
    if _oauth_request_count % 100 == 0:
        _oauth_states.clear()


def _get_oauth_redirect_uri(request: Request, provider: str) -> str:
    return str(request.base_url).rstrip("/") + f"/auth/oauth/callback/{provider}"


PROVIDER_CONFIGS = {
    "google": {
        "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
        "params": {"scope": "openid email profile"},
        "client_id_key": "google_client_id",
        "client_secret_key": "google_client_secret",
    },
    "vk": {
        "authorize_url": "https://oauth.vk.com/authorize",
        "token_url": "https://oauth.vk.com/access_token",
        "userinfo_url": "https://api.vk.com/method/users.get",
        "params": {"scope": "email", "v": "5.131"},
        "client_id_key": "vk_client_id",
        "client_secret_key": "vk_client_secret",
    },
    "yandex": {
        "authorize_url": "https://oauth.yandex.ru/authorize",
        "token_url": "https://oauth.yandex.ru/token",
        "userinfo_url": "https://login.yandex.ru/info",
        "params": {"scope": "login:email login:info"},
        "client_id_key": "yandex_client_id",
        "client_secret_key": "yandex_client_secret",
    },
}


def _get_provider_or_404(provider: str):
    cfg = PROVIDER_CONFIGS.get(provider)
    if not cfg:
        raise HTTPException(status_code=404, detail=f"Unknown provider: {provider}")
    client_id = getattr(settings, cfg["client_id_key"])
    if not client_id:
        raise HTTPException(status_code=400, detail=f"Provider {provider} not configured")
    return cfg, client_id


async def _exchange_code(provider: str, cfg: dict, client_id: str, code: str, redirect_uri: str) -> dict:
    client_secret = getattr(settings, cfg["client_secret_key"])
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
    }
    if provider == "google":
        data["grant_type"] = "authorization_code"
    elif provider == "yandex":
        data["grant_type"] = "authorization_code"

    async with httpx.AsyncClient() as client:
        if provider == "yandex":
            resp = await client.post(cfg["token_url"], data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        else:
            resp = await client.post(cfg["token_url"], data=data)
        resp.raise_for_status()
        return resp.json()


async def _fetch_user_info(provider: str, cfg: dict, token_data: dict) -> dict:
    access_token = token_data["access_token"]
    async with httpx.AsyncClient() as client:
        if provider == "google":
            resp = await client.get(cfg["userinfo_url"], headers={"Authorization": f"Bearer {access_token}"})
            resp.raise_for_status()
            data = resp.json()
            return {"email": data["email"], "name": data.get("given_name", data.get("name", ""))}
        elif provider == "vk":
            email = token_data.get("email", "")
            resp = await client.get(f"{cfg['userinfo_url']}?v=5.131&access_token={access_token}")
            resp.raise_for_status()
            data = resp.json()
            user_data = data["response"][0]
            name = f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}".strip()
            return {"email": email, "name": name}
        elif provider == "yandex":
            resp = await client.get(cfg["userinfo_url"], headers={"Authorization": f"Bearer {access_token}"})
            resp.raise_for_status()
            data = resp.json()
            email = data.get("default_email", "")
            name = data.get("display_name", "") or f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
            return {"email": email, "name": name}


async def _oauth_login(code: str, state: str, provider: str, request: Request):
    _clean_oauth_states()
    saved_state = _oauth_states.pop(state, None)
    if not saved_state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    cfg, client_id = _get_provider_or_404(provider)
    redirect_uri = _get_oauth_redirect_uri(request, provider)
    token_data = await _exchange_code(provider, cfg, client_id, code, redirect_uri)
    user_info = await _fetch_user_info(provider, cfg, token_data)

    if not user_info.get("email"):
        raise HTTPException(status_code=400, detail="Email not provided by provider")

    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == user_info["email"]))
        user = result.scalar_one_or_none()

        if not user:
            random_hash = hash_password(secrets.token_urlsafe(16))
            tariff = await session.execute(select(Tariff).where(Tariff.name == "starter"))
            starter = tariff.scalar_one()
            user = User(email=user_info["email"], hashed_password=random_hash, tariff_id=starter.id)
            session.add(user)
            await session.commit()
            await session.refresh(user)

    token = create_access_token({"sub": str(user.id), "email": user.email})
    return token


@app.get("/auth/oauth/{provider}")
async def oauth_url_get(provider: str, request: Request):
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = provider

    cfg, client_id = _get_provider_or_404(provider)
    redirect_uri = _get_oauth_redirect_uri(request, provider)

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "state": state,
    }
    params.update(cfg["params"])

    url = f"{cfg['authorize_url']}?{urlencode(params)}"
    return {"url": url}


@app.post("/auth/oauth/url")
async def oauth_url_post(req: OAuthUrlRequest, request: Request):
    state = secrets.token_urlsafe(32)
    _oauth_states[state] = req.provider

    cfg, client_id = _get_provider_or_404(req.provider)
    redirect_uri = _get_oauth_redirect_uri(request, req.provider)

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "state": state,
    }
    params.update(cfg["params"])

    url = f"{cfg['authorize_url']}?{urlencode(params)}"
    return {"url": url}


@app.get("/auth/oauth/callback/{provider}")
async def oauth_callback(provider: str, code: str, state: str, request: Request):
    try:
        token = await _oauth_login(code, state, provider, request)
        return RedirectResponse(url=f"{settings.frontend_url}/dashboard.html?token={token}")
    except HTTPException as e:
        return RedirectResponse(url=f"{settings.frontend_url}/dashboard.html?error={quote(str(e.detail))}")
    except Exception as e:
        logger.error("OAuth callback error: %s", e)
        return RedirectResponse(url=f"{settings.frontend_url}/dashboard.html?error={quote('OAuth authentication failed')}")


@app.post("/generate")
async def generate(req: GenerateRequest, user=Depends(get_current_user)):
    async with async_session() as session:
        user_db = await session.get(User, user.id)
        tariff = await session.get(Tariff, user_db.tariff_id)

        if tariff.generations_per_month != -1 and user_db.generations_used >= tariff.generations_per_month:
            raise HTTPException(
                status_code=429,
                detail="Лимит генераций на месяц исчерпан. Обновите тариф.",
            )

        try:
            result = await generate_content(req.product, req.tools, req.marketplace)
        except Exception as e:
            logger.error("Generation failed: %s", e)
            raise HTTPException(status_code=500, detail="Ошибка генерации контента. Попробуйте позже.")

        gen = Generation(
            user_id=user_db.id,
            product=req.product,
            tools=json.dumps(req.tools, ensure_ascii=False),
            marketplace=req.marketplace,
            result=json.dumps(result, ensure_ascii=False),
        )
        session.add(gen)
        user_db.generations_used += 1
        await session.commit()

    return result


@app.get("/me", response_model=UserResponse)
async def get_me(user=Depends(get_current_user)):
    async with async_session() as session:
        user_db = await session.get(User, user.id)
        tariff = await session.get(Tariff, user_db.tariff_id)

    return UserResponse(
        id=user_db.id,
        email=user_db.email,
        tariff=TariffInfo(
            id=tariff.id,
            name=tariff.name,
            generations_per_month=tariff.generations_per_month,
            price=tariff.price,
        ),
        generations_used=user_db.generations_used,
        generations_limit=tariff.generations_per_month,
        created_at=user_db.created_at,
    )


@app.get("/history", response_model=list[HistoryItem])
async def get_history(user=Depends(get_current_user)):
    async with async_session() as session:
        result = await session.execute(
            select(Generation)
            .where(Generation.user_id == user.id)
            .order_by(Generation.created_at.desc())
            .limit(20)
        )
        gens = result.scalars().all()

    return [
        HistoryItem(
            id=g.id,
            product=g.product,
            tools=json.loads(g.tools),
            marketplace=g.marketplace,
            created_at=g.created_at,
        )
        for g in gens
    ]
