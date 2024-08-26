#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-06 01:08:46
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.config import settings


if settings.environment == "PRODUCTION":
    engine_url = settings.database_private_prod_url
elif settings.environment == "LOCALDOCKER":
    engine_url = settings.database_docker_url
elif settings.environment == "STAGING":
    engine_url = settings.database_staging_url
else:
    # use local environment
    engine_url = settings.database_private_url
    # engine_url = settings.database_staging_url  # only for simulation


engine = create_engine(
    engine_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
)

test_engine = create_engine(
    settings.database_test_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


Base = declarative_base()
