# Make a FASTAPI app

import asyncio
import json
import pathlib
import sys

import anyio
import hypercorn
from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from hypercorn.asyncio import serve
from rich.console import Console
from routes import router as api_router
from workflow_templates import WorkflowTemplates

app = FastAPI(title=settings.PROJECT_NAME,
              version=settings.VERSION,
              description=settings.DESCRIPTION,
              docs_url=settings.DOCS_URL,
              redoc_url=settings.REDOC_URL,
              debug=settings.DEBUG)


async def initialize_app():
  console = Console(file=sys.stderr)
  app.state.settings = settings
  app.state.comfy_catapult_debug_path = anyio.Path(settings.CATAPULT_DEBUG_PATH)
  app.state.workflow_templates = WorkflowTemplates(simple_workflow=json.loads(
      pathlib.Path(settings.SIMPLE_WORKFLOW_JSON_API_PATH).read_text()))

  app.mount("/static", StaticFiles(directory="static"), name="static")

  # Add the routes to the app
  app.include_router(api_router)

  # Add CORS middleware
  app.add_middleware(
      CORSMiddleware,
      allow_origins=settings.ALLOWED_HOSTS,
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  # Get hostname -I from system
  # hostname = (await anyio.run_process("hostname -I")).stdout.strip().decode()
  # console.print(f"`hostname -I`: {hostname}", style="bold green")


async def run():
  config = hypercorn.config.Config()

  # hostnames = [(await anyio.run_process("hostname -I")).stdout.strip().decode()]
  bind = []
  # for hostname in hostnames:
  bind += [f"0.0.0.0:{settings.PORT}"]

  config.bind = bind
  config.loglevel = 'debug' if settings.DEBUG else 'warning'
  await serve(app, config)  # type: ignore


asyncio.run(initialize_app())
# asyncio.run(run())
