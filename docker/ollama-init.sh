# Optional: pull default Ollama model on first startup.
# This can take several minutes depending on network speed.
MODEL="${OLLAMA_DEFAULT_MODEL:-llama3.2:3b}"

echo "Pulling Ollama model: ${MODEL}"
curl -s http://ollama:11434/api/tags > /dev/null 2>&1 || sleep 10

until curl -sf http://ollama:11434/api/tags > /dev/null; do
  echo "Waiting for Ollama..."
  sleep 5
done

curl -sf -X POST http://ollama:11434/api/pull \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"${MODEL}\"}" || echo "Model pull failed — pull manually later."

echo "Ollama model init complete."
