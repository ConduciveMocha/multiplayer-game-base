#!/usr/bin/env python3
import os
from app import celery, create_application
from server.serverconfig import Config
app = create_application(Config)
app.app_context().push()
