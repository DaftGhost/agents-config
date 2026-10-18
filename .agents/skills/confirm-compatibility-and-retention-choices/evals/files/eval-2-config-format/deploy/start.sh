#!/bin/sh
# Production hosts ship their own /etc/app/config.yaml, managed outside this repo
exec python -m app --config /etc/app/config.yaml
