# todo should be uncommented code black by your case.
# import sentry_sdk
# from sentry_sdk.integrations.pymongo import PyMongoIntegration
# from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
# from sentry_sdk.integrations.celery import CeleryIntegration
# from sentry_sdk.integrations.redis import RedisIntegration
# from app.core.config import settings
#
# sentry_sdk.init(
#     dsn=settings.sentry_dsn,
#     integrations=[
#         PyMongoIntegration(),
#     ],
#
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production,
#     traces_sample_rate=1.0,
# )
#
# sentry_sdk.init(
#     dsn=settings.sentry_dsn,
#     integrations=[
#         SqlalchemyIntegration(),
#     ],
# )
#
# sentry_sdk.init(
#     dsn=settings.sentry_dsn,
#     integrations=[
#         RedisIntegration(),
#     ],
# )
#
# sentry_sdk.init(
#     dsn=settings.sentry_dsn,
#     integrations=[
#         CeleryIntegration(),
#     ],
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production,
#     traces_sample_rate=1.0,
# )
