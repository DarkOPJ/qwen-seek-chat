from app import create_app
from app.constants import (
    DEVELOPMENT_ENVIRONMENT,
    PRODUCTION_ENVIRONMENT,
    UAT_ENVIRONMENT,
)
from app.utils import validate_environment

validate_environment(
    modes=[DEVELOPMENT_ENVIRONMENT, UAT_ENVIRONMENT, PRODUCTION_ENVIRONMENT]
)
app = create_app()
