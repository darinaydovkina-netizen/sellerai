import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select

from database import async_session, init_db, User, Tariff, Generation
from models import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    GenerateRequest,
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
