#!/usr/bin/env bash

set -euxo pipefail

pushd transformscsv/api
pytest -rA
