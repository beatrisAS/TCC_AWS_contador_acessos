#!/usr/bin/env bash
set -euo pipefail

export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-test}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-test}"
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export CDK_DEFAULT_ACCOUNT="${CDK_DEFAULT_ACCOUNT:-000000000000}"
export CDK_DEFAULT_REGION="$AWS_DEFAULT_REGION"

if ! curl -fsS http://localhost:4566/_localstack/health >/dev/null; then
  echo "LocalStack não está disponível em http://localhost:4566. Execute: docker compose up -d"
  exit 1
fi

cd "$(dirname "$0")/../contador-de-acessos-aws/backend"
python3 -m venv .venv 2>/dev/null || true
source .venv/bin/activate
pip install -r requirements.txt

if ! command -v cdklocal >/dev/null 2>&1; then
  echo "cdklocal não encontrado. Instale com: npm install -g aws-cdk-local aws-cdk"
  exit 1
fi

cdklocal bootstrap
cdklocal deploy --require-approval never
