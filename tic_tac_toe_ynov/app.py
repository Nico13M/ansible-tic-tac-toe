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


SENTRY_DSN = os.getenv(
    "SENTRY_DSN",
    "https://4b853e5f7de04f1a6b85d6f5bc8ea5a5@o4511613544235008.ingest.de.sentry.io/4511613648699472",
)

if sentry_sdk:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        send_default_pii=True,
        environment=os.getenv("SENTRY_ENVIRONMENT", "local"),
        release=os.getenv("SENTRY_RELEASE"),
        integrations=[FlaskIntegration()],
        traces_sample_rate=0.0,
    )


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.setdefault("APP_NAME", "tic-tac-toe-ynov")

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

    @app.get("/debug/sentry-test")
    def sentry_test() -> tuple[dict[str, str], int]:
        division_by_zero = 1 / 0
        return {"result": str(division_by_zero)}, 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
