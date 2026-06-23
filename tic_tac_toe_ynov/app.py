from __future__ import annotations

import os

from flask import Flask

try:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
except ImportError:  # pragma: no cover - optional in local execution
    sentry_sdk = None
    FlaskIntegration = None

from tic_tac_toe_ynov.game import GameState


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.setdefault("APP_NAME", "tic-tac-toe-ynov")

    sentry_dsn = os.getenv("SENTRY_DSN")
    sentry_environment = os.getenv("SENTRY_ENVIRONMENT", "local")
    if sentry_sdk and sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=sentry_environment,
            release=os.getenv("SENTRY_RELEASE"),
            integrations=[FlaskIntegration()],
            traces_sample_rate=0.0,
        )

    @app.get("/")
    def index() -> tuple[dict[str, object], int]:
        game = GameState()
        return (
            {
                "name": app.config["APP_NAME"],
                "message": "Tic-tac-toe app ready for CI/CD and Kubernetes deployment.",
                "available_moves": list(game.available_moves()),
            },
            200,
        )

    @app.get("/health")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
