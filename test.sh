#!/usr/bin/env bash

set -euxo pipefail

pushd transforms/api
pytest -rA
