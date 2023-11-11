import aioredis
from pydantic import BaseSettings

from app import settings


class Config(BaseSettings):
    redis_url: str = f'redis://{settings.REDIS_HOST}:6379'


config = Config()
redis = aioredis.from_url(config.redis_url, decode_responses=True)


async def add_to_blacklist(token: str):
    return await redis.sadd('blacklist', token)


async def is_in_blacklist(token: str):
    return await redis.sismember('blacklist', token)


async def set_user_token(user_id: int, token: str):
    return await redis.set(f'jwt:{user_id}', token)


async def get_user_jwt_token(user_id: int):
    return await redis.get(f'jwt:{user_id}')
