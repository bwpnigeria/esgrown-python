#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2023-01-23 11:50:13
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import settings
from app.access_control import router as access_control_router
from app.user import router as users_router
from app.lga import router as lga_router
from app.dashboard import router as dashboard_router

from app.profile import router as individual_router

app = FastAPI(
    title="Esgrown"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# add two routes one for "/privacy" and another for "/terms"


@app.get("/privacy")
def privacy():
    return {"privacy": "privacy policy"}


@app.get("/terms")
def terms():
    return {"terms": "terms and conditions"}


# Access Control
app.include_router(access_control_router.perms_router)
app.include_router(access_control_router.roles_router)
app.include_router(access_control_router.groups_router)

# Users
app.include_router(users_router.users_router)
app.include_router(users_router.auth_router)

# Local Government
app.include_router(lga_router.state_router)
app.include_router(lga_router.lga_router)

# Profile
app.include_router(individual_router.individual_router)


# Helper
# app.include_router(alumni_router.helper_router)
