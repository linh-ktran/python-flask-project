"""Health check."""

from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint("health", __name__, url_prefix="/health", description="Health check")


@blp.route("")
class HealthCheck(MethodView):

    @blp.response(200)
    def get(self) -> dict:
        return {"status": "healthy", "service": "Industrial Asset Manager API"}
