#!/bin/bash
exec gunicorn -b 0.0.0.0 app:app