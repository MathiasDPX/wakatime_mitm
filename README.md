# wakamitm

wakamitm — WakaTime heartbeat middleware

wakamitm intercepts and forwards heartbeat requests to one or more configurable backends. It provides a simple middleware (apps) system to preprocess and postprocess payloads (authentication, filtering, enrichment) and sends requests to configured backends in parallel.

## Features

- Catch-all HTTP proxy for GET / POST / DELETE requests
- Parallel forwarding to multiple backends
- Pluggable middleware (apps) for pre/post processing (for example `auth`)
- Configuration via `config.toml`

## Quick install & setup

Prerequisites:

- Docker (recommended for production)
- or Python 3.11+ and pip (for local runs)

## Configuration

The main configuration file is `config.toml`. See `example-config.toml` for a working example

```toml
[redirector]
backends = [
	["https://hackatime.hackclub.com/api/hackatime/v1/", "Basic B64_TOKEN"],
	["https://api.wakatime.com/api/v1/", "Bearer AnotherToken"]
]

[apps.leetcode-nvim]
enabled = true

[apps.auth]
enabled = true
tokens = []
```

Key fields:

- `redirector.backends` — list of backends. Each entry is `[base_url, auth_header]`. The intercepted path is appended to `base_url`. `auth_header` is added as the `Authorization` header for that backend
- `apps.<name>.enabled` — enable or disable an app
- `apps.auth.tokens` — list of accepted tokens

The application loads `config.toml` from the working directory and exposes its raw content in the `WAKAMITM_CONFIG` environment variable for middleware apps.

## Usage

The app behaves as a proxy: it receives incoming requests (GET/POST/DELETE) and forwards them to the configured backends.

```bash
curl -X GET http://localhost:5000/users/current/statusbar/today \
	-H "Authorization: Bearer YOUR_TOKEN" \
```

Behavior notes:

- The header `X-Middleware-Apps` is added to requests forwarded to backends and lists enabled apps
- The `auth` middleware validates the `Authorization` header. It accepts `Basic <base64>` (decoded) and `Bearer <token>`
- Middleware apps can implement `_predispatch` and `_postdispatch` to modify request and response payloads

## Deployment

After pulling the repository you can create a `docker-compose.yml`

```yaml
version: "3.9"

services:
  web:
    build: .
    container_name: wakatime-mitm
    ports:
      - "8080:80"
    restart: unless-stopped
```

Now, you can start it with `docker compose up -d --build`