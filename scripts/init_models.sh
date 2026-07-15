#!/bin/bash
# Model initialization script for Ollama

set -e

OLLAMA_HOST="${OLLAMA_HOST:-http://ollama:11434}"
MODELS=("qwen3:1.7b" "deepseek-r1:1.5b")

echo "Waiting for Ollama to be ready..."
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null; do
    echo "Ollama not ready, waiting..."
    sleep 5
done

echo "Ollama is ready!"

for model in "${MODELS[@]}"; do
    echo "Checking if model $model exists..."
    if curl -s "$OLLAMA_HOST/api/tags" | grep -q "\"name\":\"$model\""; then
        echo "Model $model already exists, skipping pull"
    else
        echo "Pulling model $model..."
        curl -X POST "$OLLAMA_HOST/api/pull" \
            -H "Content-Type: application/json" \
            -d "{\"name\": \"$model\", \"stream\": false}" \
            --max-time 600
        echo "Model $model pulled successfully"
    fi
done

echo "All models initialized!"