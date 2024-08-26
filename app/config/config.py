#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2023-01-19 21:33:57
# @Author  : Dahir Muhammad Dahir (dahirmuhammad3@gmail.com)
# @Link    : link
# @Version : 1.0.0


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Production Settings"""

    app_name: str = "Esgrown"
    environment: str = ""

    # production database settings
    prod_postgres_user: str
    prod_postgres_password: str
    prod_postgres_db: str
    prod_database_private_address: str
    prod_database_public_address: str

    # database settings
    postgres_user: str
    postgres_password: str
    postgres_db: str
    test_database_name: str
    database_private_address: str
    database_public_address: str
    database_docker_address: str
    database_port: str

    # staging database settings
    postgres_user_staging: str
    postgres_password_staging: str
    postgres_db_staging: str
    test_database_name_staging: str
    database_address_staging: str
    database_port_staging: str

    database_private_prod_url: str
    database_public_prod_url: str
    database_private_url: str
    database_public_url: str
    database_docker_url: str
    database_staging_url: str
    database_test_url: str
    database_pool_size: int = 50
    database_max_overflow: int = 85

    # initial admin (only for local runs)
    initial_email: str
    initial_password: str
    initial_firstname: str
    initial_lastname: str
    initial_middlename: str

    # Test admin
    test_super_user_email: str
    test_super_username: str
    test_super_user_password: str

    # jwt settings
    jwt_secret_key: str
    jwt_algorithm: str
    token_life_span: int
    token_mobile_life_span: int
    token_long_life_span: int

    # OTP
    otp_life_span: int
    otp_length: int

    # url
    token_url: str
    frontend_url: str
    thirdparty_payment_verify_url: str

    # email
    source_email: str
    sendgrid_api_key: str

    # SMS
    sendchamp_base_url: str
    sendchamp_key: str

    # Phone
    source_phone: str

    # cloud
    cloud_bucket_name: str
    cloud_storage_url: str
    GOOGLE_APPLICATION_CREDENTIALS: str

    # cors
    cors_origins: list[str] = []

    # FlutterWave
    flutterwave_base_url: str
    flutterwave_payment_url: str
    flutterwave_verify_url: str
    flutterwave_verify_by_ref_url: str
    flutterwave_public_key: str
    flutterwave_secret_key: str
    flutterwave_encryption_key: str

    # Paystack
    paystack_base_url: str
    paystack_payment_url: str
    paystack_verify_url: str
    paystack_public_key: str
    paystack_secret_key: str

    moniepoint_base_url: str
    moniepoint_payment_url: str
    moniepoint_verify_url: str
    moniepoint_public_key: str
    moniepoint_secret_key: str

    # Monnify
    monnify_base_url: str
    monnify_payment_url: str
    monnify_invoice_url: str
    monnify_verify_url: str
    monnify_login_url: str

    # System Variables
    business_qr_url: str

    # Logfire
    logfire_token: str

    # Swiftend API
    swiftend_key: str
    phone_verification_url: str
    bvn_verification_url: str

    # Twilio API
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str

    # Active SMS
    sms_sender: str

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.staging", ".env.production"),
        env_file_encoding="utf-8",
    )


settings = Settings()  # type: ignore
