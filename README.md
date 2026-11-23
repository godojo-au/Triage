# Triage

A Python tool that turns a CSV inbox into a review queue. For model-assisted routing, it retrieves similar examples from a small knowledge CSV and passes those examples with the item to a model. Every item stays `needs_review`; the tool never assigns work or sends messages.

## Try it

Python 3.10+; no packages needed.

```sh
python3 triage.py examples/items.csv --output queue.json
python3 -m unittest -v
```

Input columns are `id,title,description`. IDs must be unique. The output is JSON with each item's full text, suggestion, reason, and review status. The example contains synthetic work items.

## Model-assisted suggestions

Choose one route. The local rules option above needs no model. The model routes use `examples/knowledge.csv` by default; replace it with your own reviewed examples using `--knowledge your_examples.csv`. The output includes the IDs of retrieved examples so you can inspect the basis for a suggestion.

For an API model, create your own key, set it in your shell, and use `--provider openai`. Never commit a key. This sends item text and retrieved examples to the API, so use only data you may share.

```sh
export OPENAI_API_KEY="your-own-key"
python3 triage.py examples/items.csv --provider openai --output queue.json
```

For a local model, install [Ollama](https://ollama.com/), pull a chat model, and start its local service:

```sh
ollama pull llama3.2
python3 triage.py examples/items.csv --provider ollama --model llama3.2 --output queue.json
```

The API default is `gpt-4o-mini`; use `--model` to choose another model available to your account. Ollama defaults to `llama3.2`; set `OLLAMA_HOST` if its service is elsewhere. Model availability and API pricing depend on your setup. If a model call fails or returns an unsupported category, the command stops. Review the output before using it.

## Why this project

Use it to prepare a review queue from your own work-item export while retaining a human decision point. It is not connected to a help desk or an automatic assignment system.
