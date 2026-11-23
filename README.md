# Triage

A Python tool that turns a CSV inbox into a review queue. It suggests a team and priority using local rules, or an optional AI model. Every item stays `needs_review`; the tool never assigns work or sends messages.

## Try it

Python 3.10+; no packages needed.

```sh
python3 triage.py examples/items.csv --output queue.json
python3 -m unittest -v
```

Input columns are `id,title,description`. IDs must be unique. The output is JSON with each item's full text, suggestion, reason, and review status. The example contains synthetic work items.

## Optional AI suggestions

Create your own API key with your provider and set it in your shell. Never commit a key or use someone else's key. AI mode sends item titles and descriptions to the API, so use only data you are allowed to share.

```sh
export OPENAI_API_KEY="your-own-key"
python3 triage.py examples/items.csv --ai --output queue.json
```

`OPENAI_MODEL` can select another compatible model. The default is `gpt-4o-mini`; availability and pricing depend on your account. If the API fails or returns an unsupported category, the command stops instead of silently changing the queue. Review the output before using it.

## Why this project

Use it to prepare a review queue from your own work-item export while retaining a human decision point. It is not connected to a help desk or an automatic assignment system.
