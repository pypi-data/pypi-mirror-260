from fastapi import FastAPI

import poaster.access.api
import poaster.bulletin.api
from poaster.__about__ import __version__


def get_app() -> FastAPI:
    """Build and configure application server."""

    app = FastAPI(
        docs_url="/api/docs",
        title="poaster",
        version=__version__,
        summary="Minimal, libre bulletin board for posts.",
        license_info={
            "name": "GNU Affero General Public License (AGPL)",
            "url": "https://www.gnu.org/licenses/agpl-3.0.html",
        },
    )

    app.include_router(poaster.access.api.router, prefix="/api")
    app.include_router(poaster.bulletin.api.router, prefix="/api")

    return app


app = get_app()
