from datetime import datetime

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GenerateRequest(BaseModel):
    product: str
    tools: list[str]
    marketplace: str


class Keywords(BaseModel):
    high: list[str]
    mid: list[str]
    low: list[str]


class CompetitorAnalysis(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]


class GenerateResponse(BaseModel):
    title: str | None = None
    description: str | None = None
    keywords: Keywords | None = None
    review_positive: str | None = None
    review_negative: str | None = None
    photo_ideas: list[str] | None = None
    competitor_analysis: CompetitorAnalysis | None = None
    ad_text: str | None = None


class TariffInfo(BaseModel):
    id: int
    name: str
    generations_per_month: int
    price: int


class UserResponse(BaseModel):
    id: int
    email: str
    tariff: TariffInfo
    generations_used: int
    generations_limit: int
    created_at: datetime


class OAuthUrlRequest(BaseModel):
    provider: str


class HistoryItem(BaseModel):
    id: int
    product: str
    tools: list[str]
    marketplace: str
    created_at: datetime
