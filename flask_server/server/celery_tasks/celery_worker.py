#!/usr/bin/env python3
import os
from app import celery, create_app
from server.serverconfig import Config
app = create_app(Config)
app.app_context().push()
