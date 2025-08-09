#!/usr/bin/env bash
set -e
uvicorn api.main:app --reload
