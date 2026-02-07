## Overview

Open WebUI provides a large range of environment variables that allow you to customize and configure
various aspects of the application. This page serves as a comprehensive reference for all available
environment variables, providing their types, default values, and descriptions.
As new variables are introduced, this page will be updated to reflect the growing configuration options.

!!! info

This page is up-to-date with Open WebUI release version [v0.7.1](https://github.com/open-webui/open-webui/releases/tag/v0.7.1), but is still a work in progress to later include more accurate descriptions, listing out options available for environment variables, defaults, and improving descriptions.

### Important Note on `PersistentConfig` Environment Variables

!!! note

When launching Open WebUI for the first time, all environment variables are treated equally and can be used to configure the application. However, for environment variables marked as `PersistentConfig`, their values are persisted and stored internally.

After the initial launch, if you restart the container, `PersistentConfig` environment variables will no longer use the external environment variable values. Instead, they will use the internally stored values.

In contrast, regular environment variables will continue to be updated and applied on each subsequent restart.

You can update the values of `PersistentConfig` environment variables directly from within Open WebUI, and these changes will be stored internally. This allows you to manage these configuration settings independently of the external environment variables.

Please note that `PersistentConfig` environment variables are clearly marked as such in the documentation below, so you can be aware of how they will behave.

To disable this behavior and force Open WebUI to always use your environment variables (ignoring the database), set `ENABLE_PERSISTENT_CONFIG` to `False`.

**CRITICAL WARNING:** When `ENABLE_PERSISTENT_CONFIG` is `False`, you may still be able to edit settings in the Admin UI. However, these changes are **NOT saved permanently**. They will persist only for the current session and will be **lost** when you restart the container, as the system will revert to the values defined in your environment variables.

### Troubleshooting Ignored Environment Variables 🛠️

If you change an environment variable (like `ENABLE_SIGNUP=True`) but don't see the change reflected in the UI (e.g., the "Sign Up" button is still missing), it's likely because a value has already been persisted in the database from a previous run or a persistent Docker volume.

#### Option 1: Using `ENABLE_PERSISTENT_CONFIG` (Temporary Fix)

Set `ENABLE_PERSISTENT_CONFIG=False` in your environment. This forces Open WebUI to read your variables directly. Note that UI-based settings changes will not persist across restarts in this mode.

#### Option 2: Update via Admin UI (Recommended)

The simplest and safest way to change `PersistentConfig` settings is directly through the **Admin Panel** within Open WebUI. Even if an environment variable is set, changes made in the UI will take precedence and be saved to the database.

#### Option 3: Manual Database Update (Last Resort / Lock-out Recovery)

If you are locked out or cannot access the UI, you can manually update the SQLite database via Docker:

```bash
docker exec -it open-webui sqlite3 /app/backend/data/webui.db "UPDATE config SET data = json_set(data, '$.ENABLE_SIGNUP', json('true'));"
```
*(Replace `ENABLE_SIGNUP` and `true` with the specific setting and value needed.)*

#### Option 4: Resetting for a Fresh Install

If you are performing a clean installation and want to ensure all environment variables are fresh:
1. Stop the container.
2. Remove the persistent volume: `docker volume rm open-webui`.
3. Restart the container.

!!! danger
**Warning:** Removing the volume will delete all user data, including chats and accounts.

## App/Backend

The following environment variables are used by `backend/open_webui/config.py` to provide Open WebUI startup
configuration. Please note that some variables may have different default values depending on
whether you're running Open WebUI directly or via Docker. For more information on logging
environment variables, see our [logging documentation](getting-started/advanced-topics/logging).

### General

#### `WEBUI_URL`

- Type: `str`
- Default: `http://localhost:3000`
- Description: Specifies the URL where your Open WebUI installation is reachable. Needed for search engine support and OAuth/SSO.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! warning

This variable has to be set before you start using OAuth/SSO for authentication.
Since this is a persistent config environment variable, you can only change it through one of the following options:

 - Temporarily disabling persistent config using `ENABLE_PERSISTENT_CONFIG`
 - Changing `WEBUI_URL` in the admin panel > settings and changing "WebUI URL".

Failure to set WEBUI_URL before using OAuth/SSO will result in failure to log in.

#### `ENABLE_SIGNUP`

- Type: `bool`
- Default: `True`
- Description: Toggles user account creation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_SIGNUP_PASSWORD_CONFIRMATION`

- Type: `bool`
- Default: `False`
- Description: If set to True, a "Confirm Password" field is added to the sign-up page to help users avoid typos when creating their password.

#### `WEBUI_ADMIN_EMAIL`

- Type: `str`
- Default: Empty string (' ')
- Description: Specifies the email address for an admin account to be created automatically on first startup when no users exist. This enables headless/automated deployments without manual account creation. When combined with `WEBUI_ADMIN_PASSWORD`, the admin account is created during application startup, and `ENABLE_SIGNUP` is automatically disabled to prevent unauthorized account creation.

!!! info

This variable is designed for automated/containerized deployments where manual admin account creation is impractical. The admin account is only created if:
- No users exist in the database (fresh installation)
- Both `WEBUI_ADMIN_EMAIL` and `WEBUI_ADMIN_PASSWORD` are configured

After the admin account is created, sign-up is automatically disabled for security. You can re-enable it later via the Admin Panel if needed.

#### `WEBUI_ADMIN_PASSWORD`

- Type: `str`
- Default: Empty string (' ')
- Description: Specifies the password for the admin account to be created automatically on first startup when no users exist. Must be used in conjunction with `WEBUI_ADMIN_EMAIL`. The password is securely hashed before storage using the same mechanism as manual account creation.

!!! danger

**Security Considerations**
- Use a strong, unique password for production deployments
- Consider using secrets management (Docker secrets, Kubernetes secrets, environment variable injection) rather than storing the password in plain text configuration files
- After initial setup, change the admin password through the UI for enhanced security
- Never commit this value to version control

#### `WEBUI_ADMIN_NAME`

- Type: `str`
- Default: `Admin`
- Description: Specifies the display name for the automatically created admin account. This is used when `WEBUI_ADMIN_EMAIL` and `WEBUI_ADMIN_PASSWORD` are configured for headless admin creation.

#### `ENABLE_LOGIN_FORM`

- Type: `bool`
- Default: `True`
- Description: Toggles email, password, sign-in and "or" (only when `ENABLE_OAUTH_SIGNUP` is set to True) elements.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_PASSWORD_AUTH`

- Type: `bool`
- Default: `True`
- Description: Allows both password and SSO authentication methods to coexist when set to True. When set to False, it disables all password-based login attempts on the /signin and /ldap endpoints, enforcing strict SSO-only authentication. Disable this setting in production environments with fully configured SSO to prevent credential-based account takeover attacks; keep it enabled if you require password authentication as a backup or have not yet completed SSO configuration. Should never be disabled if OAUTH/SSO is not being used.

!!! danger

This should **only** ever be set to `False` when [ENABLE_OAUTH_SIGNUP](getting-started/env-configuration#enable_oauth_signup)
is also being used and set to `True`. **Never disable this if OAUTH/SSO is not being used.** Failure to do so will result in the inability to login.

#### `DEFAULT_LOCALE`

- Type: `str`
- Default: `en`
- Description: Sets the default locale for the application.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DEFAULT_MODELS`

- Type: `str`
- Default: Empty string (' '), since `None`.
- Description: Sets a default Language Model.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DEFAULT_PINNED_MODELS`

- Type: `str`
- Default: Empty string (' ')
- Description: Comma-separated list of model IDs to pin by default for new users who haven't customized their pinned models. This provides a pre-selected set of frequently used models in the model selector for new accounts.
- Example: `gpt-4,claude-3-opus,llama-3-70b`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DEFAULT_USER_ROLE`

- Type: `str`
- Options:
  - `pending` - New users are pending until their accounts are manually activated by an admin.
  - `user` - New users are automatically activated with regular user permissions.
  - `admin` - New users are automatically activated with administrator permissions.
- Default: `pending`
- Description: Sets the default role assigned to new users.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `DEFAULT_GROUP_ID`

- Type: `str`
- Default: Empty string (' ')
- Description: Sets the default group ID to assign to new users upon registration.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `PENDING_USER_OVERLAY_TITLE`

- Type: `str`
- Default: Empty string (' ')
- Description: Sets a custom title for the pending user overlay.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `PENDING_USER_OVERLAY_CONTENT`

- Type: `str`
- Default: Empty string (' ')
- Description: Sets a custom text content for the pending user overlay.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_CHANNELS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables channel support.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_FOLDERS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables the folders feature, allowing users to organize their chats into folders in the sidebar.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `FOLDER_MAX_FILE_COUNT`

- Type: `int`
- Default: `("") empty string`
- Description: Sets the maximum number of files processing allowed per folder.
- Persistence: This environment variable is a `PersistentConfig` variable. It can be configured in the **Admin Panel > Settings > General > Folder Max File Count**. Default is none (empty string) which is unlimited.

#### `ENABLE_NOTES`

- Type: `bool`
- Default: `True`
- Description: Enables or disables the notes feature, allowing users to create and manage personal notes within Open WebUI.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_MEMORIES`

- Type: `bool`
- Default: `True`
- Description: Enables or disables the [memory feature](features/memory.md), allowing models to store and retrieve long-term information about users.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WEBHOOK_URL`

- Type: `str`
- Description: Sets a webhook for integration with Discord/Slack/Microsoft Teams.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_ADMIN_EXPORT`

- Type: `bool`
- Default: `True`
- Description: Controls whether admins can export data, chats and the database in the admin panel. Database exports only work for SQLite databases for now.

#### `ENABLE_ADMIN_CHAT_ACCESS`

- Type: `bool`
- Default: `True`
- Description: Enables admin users to directly access the chats of other users. When disabled, admins can no longer accesss user's chats in the admin panel. If you disable this, consider disabling `ENABLE_ADMIN_EXPORT` too, if you are using SQLite, as the exports also contain user chats.

#### `ENABLE_ADMIN_WORKSPACE_CONTENT_ACCESS`

- Type: `bool`
- Default: `True`
- Description: Enables admin users to access all workspace content (models, knowledge bases, prompts, and tools) regardless of access control settings. When set to `False`, admins will only see workspace items they have been explicitly granted access to.

!!! warning **Deprecated**

**This environment variable is deprecated and may be removed in a future release.** Use [`BYPASS_ADMIN_ACCESS_CONTROL`](#bypass_admin_access_control.md) instead, which provides the same functionality with a clearer name.

#### `BYPASS_ADMIN_ACCESS_CONTROL`

- Type: `bool`
- Default: `True`
- Description: When disabled, admin users are treated like regular users for workspace access (models, knowledge, prompts and tools) and only see items they have **explicit permission to access** through the existing access control system. This also applies to the visibility of models in the model selector - admins will be treated as regular users: base models and custom models they do not have **explicit permission to access**, will be hidden. If set to `True` (Default), admins have access to **all created items** in the workspace area and all models in the model selector, **regardless of access permissions**.

#### `ENABLE_USER_WEBHOOKS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user webhooks.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `RESPONSE_WATERMARK`

- Type: `str`
- Default: Empty string (' ')
- Description: Sets a custom text that will be included when you copy a message in the chat. e.g., `"This text is AI generated"` -> will add "This text is AI generated" to every message, when copied.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `THREAD_POOL_SIZE`

- Type: `int`
- Default: `0`
- Description: Sets the thread pool size for FastAPI/AnyIO blocking calls. By default (when set to `0`) FastAPI/AnyIO use `40` threads. In case of large instances and many concurrent users, it may be needed to increase `THREAD_POOL_SIZE` to prevent blocking.

!!! info

If you are running larger instances, you WILL NEED to set this to a higher value like multiple hundreds if not thousands (e.g. `1000`) otherwise your app may get stuck the default pool size (which is 40 threads) is full and will not react anymore.

#### `ENABLE_CUSTOM_MODEL_FALLBACK`

- Type: `bool`
- Default: `False`
- Description: Controls whether custom models should fall back to a default model if their assigned base model is missing. When set to `True`, if a custom model's base model is not found, the system will use the first model from the configured `DEFAULT_MODELS` list instead of returning an error.

#### `SHOW_ADMIN_DETAILS`

- Type: `bool`
- Default: `True`
- Description: Toggles whether to show admin user details in the interface.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_PUBLIC_ACTIVE_USERS_COUNT`

- Type: `bool`
- Default: `True`
- Description: Controls whether the active user count is visible to all users or restricted to administrators only. When set to `False`, only admin users can see how many users are currently active, reducing backend load and addressing privacy concerns in large deployments.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_USER_STATUS`

- Type: `bool`
- Default: `True`
- Description: Globally enables or disables user status functionality. When disabled, the status UI (including blinking active/away indicators and status messages) is hidden across the application, and user status API endpoints are restricted.
- Persistence: This environment variable is a `PersistentConfig` variable. It can be toggled in the **Admin Panel > Settings > General > User Status**.

#### `ADMIN_EMAIL`

- Type: `str`
- Description: Sets the admin email shown by `SHOW_ADMIN_DETAILS`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENV`

- Type: `str`
- Options:
  - `dev` - Enables the FastAPI API documentation on `/docs`
  - `prod` - Automatically configures several environment variables
- Default:
  - **Backend Default**: `dev`
  - **Docker Default**: `prod`
- Description: Environment setting.

#### `ENABLE_PERSISTENT_CONFIG`

- Type: `bool`
- Default: `True`
- Description: Controls whether the system prioritizes configuration saved in the database over environment variables.
  - **`True` (Default):** Values saved in the **database** (via the Admin UI) take precedence. If a value is set in the UI, the environment variable is ignored for that setting.
  - **`False`:** **Environment variables** take precedence. The system will *not* load configuration from the database at startup if an environment variable is present (or it will use the default).
    - **CRITICAL WARNING:** When set to `False`, you can still seemingly "change" settings in the Admin UI. These changes will apply to the **current running session** but **will be lost upon restart**. The system will revert to the values defined in your environment variables (or defaults) every time it boots up.
    - **Use Case:** Set this to `False` if you want to strictly manage configuration via a `docker-compose.yaml` or `.env` file and prevent UI changes from persisting across restarts.

#### `CUSTOM_NAME`

- Type: `str`
- Description: Sets `WEBUI_NAME` but polls **api.openwebui.com** for metadata.

#### `WEBUI_NAME`

- Type: `str`
- Default: `Open WebUI`
- Description: Sets the main WebUI name. Appends `(Open WebUI)` if overridden.

#### `PORT`

- Type: `int`
- Default: `8080`
- Description: Sets the port to run Open WebUI from.

!!! info

If you're running the application via Python and using the `open-webui serve` command, you cannot set the port using the `PORT` configuration. Instead, you must specify it directly as a command-line argument using the `--port` flag. For example:

```bash
open-webui serve --port 9999
```

This will run the Open WebUI on port `9999`. The `PORT` environment variable is disregarded in this mode.

#### `ENABLE_REALTIME_CHAT_SAVE`

- Type: `bool`
- Default: `False`
- Description: When enabled, the system saves each individual chunk of streamed chat data to the database in real time.

!!! danger EXTREME PERFORMANCE RISK: DO NOT ENABLE IN PRODUCTION
**It is strongly recommended to NEVER enable this setting in production or multi-user environments.**

Enabling `ENABLE_REALTIME_CHAT_SAVE` causes every single token generated by the LLM to trigger a separate database write operation. In a multi-user environment, this will:
1.  **Exhaust Database Connection Pools**: Rapid-fire writes will quickly consume all available database connections, leading to "QueuePool limit reached" errors and application-wide freezes.
2.  **Severe Performance Impact**: The overhead of thousands of database transactions per minute will cause massive latency for all users.
3.  **Hardware Strain**: It creates immense I/O pressure on your storage system.

**Keep this set to `False` (the default).** Chats are still saved automatically once generation is complete. This setting is only intended for extreme debugging scenarios or single-user environments where sub-second persistence of every token is more important than stability.

#### `ENABLE_CHAT_RESPONSE_BASE64_IMAGE_URL_CONVERSION`

- Type: `bool`
- Default: `False`
- Description: When set to true, it automatically uploads base64-encoded images exceeding 1KB in markdown and converts them into image file URLs to reduce the size of response text. Some multimodal models directly output images as Base64 strings within the Markdown content. This results in larger response bodies, placing strain on CPU, network, Redis, and database resources.

#### `CHAT_RESPONSE_STREAM_DELTA_CHUNK_SIZE`

- Type: `int`
- Default: `1`
- Description: Sets a system-wide minimum value for the number of tokens to batch together before sending them to the client during a streaming response. This allows an administrator to enforce a baseline level of performance and stability across the entire system by preventing excessively small chunk sizes that can cause high CPU load. The final chunk size used for a response will be the highest value set among this global variable, the model's advanced parameters, or the per-chat settings. The default is 1, which applies no minimum batching at the global level.

#### `CHAT_STREAM_RESPONSE_CHUNK_MAX_BUFFER_SIZE`

- Type: `int`
- Default: Empty string (' '), which disables the limit (equivalent to None)
- Description: Sets the maximum buffer size in bytes for handling stream response chunks. When a single chunk exceeds this limit, the system returns an empty JSON object and skips subsequent oversized data until encountering normally-sized chunks. This prevents memory issues when dealing with extremely large responses from certain providers (e.g., models like gemini-2.5-flash-image or services returning extensive web search data exceeding). Set to an empty string or a negative value to disable chunk size limitations entirely. Recommended values are 16-20 MB (`16777216`) or larger depending on the image size of the image generation model (4K images may need even more).

!!! info

It is recommended to set this to a high single-digit or low double-digit value if you run Open WebUI with high concurrency, many users, and very fast streaming models.

#### `BYPASS_MODEL_ACCESS_CONTROL`

- Type: `bool`
- Default: `False`
- Description: Bypasses model access control. When set to `true`, all users (and admins alike) will have access to all models, regardless of the model's privacy setting (Private, Public, Shared with certain groups). This is useful for smaller or individual Open WebUI installations where model access restrictions may not be needed.

#### `WEBUI_BUILD_HASH`

- Type: `str`
- Default: `dev-build`
- Description: Used for identifying the Git SHA of the build for releases.

#### `WEBUI_BANNERS`

- Type: `list` of `dict`
- Default: `[]`
- Description: List of banners to show to users. The format for banners are:

```json
[]
```

- Persistence: This environment variable is a `PersistentConfig` variable.

!!! info

When setting this environment variable in a `.env` file, make sure to escape the quotes by wrapping the entire value in double quotes and using escaped quotes (`/"`) for the inner quotes. Example:

```
WEBUI_BANNERS="[]"
```

#### `USE_CUDA_DOCKER`

- Type: `bool`
- Default: `False`
- Description: Builds the Docker image with NVIDIA CUDA support. Enables GPU acceleration for local Whisper and embeddings.

#### `DOCKER`

- Type: `bool`
- Default: `False`
- Description: Indicates whether Open WebUI is running inside a Docker container. Used internally for environment detection.

#### `USE_CUDA`

- Type: `bool`
- Default: `False`
- Description: Controls whether to use CUDA acceleration for local models. When set to `true`, attempts to detect and use available NVIDIA GPUs. The code reads the environment variable `USE_CUDA_DOCKER` to set this internal boolean variable.

#### `DEVICE_TYPE`

- Type: `str`
- Default: `cpu`
- Description: Specifies the device type for model execution. Automatically set to `cuda` if CUDA is available and enabled, or `mps` for Apple Silicon.

#### `EXTERNAL_PWA_MANIFEST_URL`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: When defined as a fully qualified URL (e.g., https://path/to/manifest.webmanifest), requests sent to /manifest.json will use the external manifest file. When not defined, the default manifest.json file will be used.

#### `ENABLE_TITLE_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables chat title generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LICENSE_KEY`

- Type: `str`
- Default: `None`
- Description: Specifies the license key to use (for Enterprise users only).
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SSL_ASSERT_FINGERPRINT`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the SSL assert fingerprint to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_COMPRESSION_MIDDLEWARE`

- Type: `bool`
- Default: `True`
- Description: Enables gzip compression middleware for HTTP responses, reducing bandwidth usage and improving load times.

#### `DEFAULT_PROMPT_SUGGESTIONS`

- Type: `list` of `dict`
- Default: `[]` (which means to use the built-in default prompt suggestions)
- Description: List of prompt suggestions. The format for prompt suggestions are:

```json
[]
```

!!! warning

NEVER set this env var to `debug` in production.

### AIOHTTP Client

#### `AIOHTTP_CLIENT_TIMEOUT`

- Type: `int`
- Default: `300`
- Description: Specifies the timeout duration in seconds for the AIOHTTP client. This impacts things
such as connections to Ollama and OpenAI endpoints.

!!! info

This is the maximum amount of time the client will wait for a response before timing out.
If set to an empty string (' '), the timeout will be set to `None`, effectively disabling the timeout and
allowing the client to wait indefinitely.

#### `AIOHTTP_CLIENT_TIMEOUT_MODEL_LIST`

- Type: `int`
- Default: `10`
- Description: Sets the timeout in seconds for fetching the model list from Ollama and OpenAI endpoints. This affects how long Open WebUI waits for each configured endpoint when loading available models.

!!! note When to Adjust This Value

**Lower the timeout** (e.g., `3`) if:
- You have multiple endpoints configured and want faster failover when one is unreachable
- You prefer the UI to load quickly even if some slow endpoints are skipped

**Increase the timeout** (e.g., `30`) if:
- Your model servers are slow to respond (e.g., cold starts, large model loading)
- You're connecting over high-latency networks
- You're using providers like OpenRouter that may have variable response times

!!! warning Database Persistence

Connection URLs configured via the Admin Settings UI are **persisted in the database** and take precedence over environment variables. If you save an unreachable URL and the UI becomes unresponsive, you may need to use one of these recovery options:

- `RESET_CONFIG_ON_START=true` - Resets database config to environment variable values on next startup
- `ENABLE_PERSISTENT_CONFIG=false` - Always use environment variables (UI changes won't persist)

See the [Model List Loading Issues](troubleshooting/connection-error.md#️-model-list-loading-issues-slow-ui--unreachable-endpoints) troubleshooting guide for detailed recovery steps.

#### `AIOHTTP_CLIENT_TIMEOUT_OPENAI_MODEL_LIST`

- Type: `int`
- Description: Sets the timeout in seconds for fetching the model list. This can be useful in cases where network latency requires a longer timeout duration to successfully retrieve the model list.

#### `AIOHTTP_CLIENT_SESSION_SSL`

- Type: `bool`
- Default: `True`
- Description: Controls SSL/TLS verification for AIOHTTP client sessions when connecting to external APIs (e.g., Ollama Embeddings).

#### `AIOHTTP_CLIENT_TIMEOUT_TOOL_SERVER_DATA`

- Type: `int`
- Default: `10`
- Description: Sets the timeout in seconds for retrieving data from tool servers via AIOHTTP client.

#### `AIOHTTP_CLIENT_SESSION_TOOL_SERVER_SSL`

- Type: `bool`
- Default: `True`
- Description: Controls SSL/TLS verification specifically for tool server connections via AIOHTTP client.

#### `REQUESTS_VERIFY`

- Type: `bool`
- Default: `True`
- Description: Controls SSL/TLS verification for synchronous `requests` (e.g., Tika, External Reranker). Set to `False` to bypass certificate verification for self-signed certificates.

### Directories

#### `DATA_DIR`

- Type: `str`
- Default: `./data`
- Description: Specifies the base directory for data storage, including uploads, cache, vector database, etc.

#### `FONTS_DIR`

- Type: `str`
- Description: Specifies the directory for fonts.

#### `FRONTEND_BUILD_DIR`

- Type: `str`
- Default: `../build`
- Description: Specifies the location of the built frontend files.

#### `STATIC_DIR`

- Type: `str`
- Default: `./static`
- Description: Specifies the directory for static files, such as the favicon.

### Logging

#### `GLOBAL_LOG_LEVEL`

- Type: `str`
- Default: `INFO`
- Description: Sets the global logging level for all Open WebUI components. Valid values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

#### `ENABLE_AUDIT_STDOUT`

- Type: `bool`
- Default: `False`
- Description: Controls whether audit logs are output to stdout (console). Useful for containerized environments where logs are collected from stdout.

#### `ENABLE_AUDIT_LOGS_FILE`

- Type: `bool`
- Default: `True`
- Description: Controls whether audit logs are written to a file. When enabled, logs are written to the location specified by `AUDIT_LOGS_FILE_PATH`.

#### `AUDIT_LOGS_FILE_PATH`

- Type: `str`
- Default: `$/audit.log`
- Description: Configures where the audit log file is stored. Enables storing logs in separate volumes or custom locations for better organization and persistence.
- Example: `/var/log/openwebui/audit.log`, `/mnt/logs/audit.log`

#### `AUDIT_LOG_FILE_ROTATION_SIZE`

- Type: `str`
- Default: `10MB`
- Description: Specifies the maximum size of the audit log file before rotation occurs (e.g., `10MB`, `100MB`, `1GB`).

#### `AUDIT_UVICORN_LOGGER_NAMES`

- Type: `str`
- Default: `uvicorn.access`
- Description: Comma-separated list of logger names to capture for audit logging. Defaults to Uvicorn's access logger.

#### `AUDIT_LOG_LEVEL`

- Type: `str`
- Default: `NONE`
- Options: `NONE`, `METADATA`, `REQUEST`, `REQUEST_RESPONSE`
- Description: Controls the verbosity level of audit logging. `METADATA` logs basic request info, `REQUEST` includes request bodies, `REQUEST_RESPONSE` includes both requests and responses.

#### `MAX_BODY_LOG_SIZE`

- Type: `int`
- Default: `2048`
- Description: Sets the maximum size in bytes for request/response bodies in audit logs. Bodies larger than this are truncated.

#### `AUDIT_EXCLUDED_PATHS`

- Type: `str`
- Default: `/chats,/chat,/folders`
- Description: Comma-separated list of URL paths to exclude from audit logging. Paths are matched without leading slashes.RetryTo run code, enable code execution and file creation in Settings > Capabilities.Claude can make mistakes. Please double-check responses.

### Ollama

#### `ENABLE_OLLAMA_API`

- Type: `bool`
- Default: `True`
- Description: Enables the use of Ollama APIs.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OLLAMA_BASE_URL` (`OLLAMA_API_BASE_URL` is deprecated) 

- Type: `str`
- Default: `http://localhost:11434`
- Docker Default:
  - If `K8S_FLAG` is set: `http://ollama-service.open-webui.svc.cluster.local:11434`
  - If `USE_OLLAMA_DOCKER=True`: `http://localhost:11434`
  - Else `http://host.docker.internal:11434`
- Description: Configures the Ollama backend URL.

#### `OLLAMA_BASE_URLS`

- Type: `str`
- Description: Configures load-balanced Ollama backend hosts, separated by `;`. See
[`OLLAMA_BASE_URL`](#ollama_base_url.md). Takes precedence over[`OLLAMA_BASE_URL`](#ollama_base_url.md).
- Example: `http://host-one:11434;http://host-two:11434`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USE_OLLAMA_DOCKER`

- Type: `bool`
- Default: `False`
- Description: Builds the Docker image with a bundled Ollama instance.

#### `K8S_FLAG`

- Type: `bool`
- Default: `False`
- Description: If set, assumes Helm chart deployment and sets [`OLLAMA_BASE_URL`](#ollama_base_url.md) to `http://ollama-service.open-webui.svc.cluster.local:11434`

### OpenAI

#### `ENABLE_OPENAI_API`

- Type: `bool`
- Default: `True`
- Description: Enables the use of OpenAI APIs.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENAI_API_BASE_URL`

- Type: `str`
- Default: `https://api.openai.com/v1`
- Description: Configures the OpenAI base API URL.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENAI_API_BASE_URLS`

- Type: `str`
- Description: Supports balanced OpenAI base API URLs, semicolon-separated.
- Example: `http://host-one:11434;http://host-two:11434`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENAI_API_KEY`

- Type: `str`
- Description: Sets the OpenAI API key.
- Example: `sk-124781258123`
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENAI_API_KEYS`

- Type: `str`
- Description: Supports multiple OpenAI API keys, semicolon-separated.
- Example: `sk-124781258123;sk-4389759834759834`
- Persistence: This environment variable is a `PersistentConfig` variable.

### Tasks

#### `TASK_MODEL`

- Type: `str`
- Description: The default model to use for tasks such as title and web search query generation
when using Ollama models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TASK_MODEL_EXTERNAL`

- Type: `str`
- Description: The default model to use for tasks such as title and web search query generation
when using OpenAI-compatible endpoints.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TITLE_GENERATION_PROMPT_TEMPLATE`

- Type: `str`
- Description: Prompt to use when generating chat titles.
- Default: The value of `DEFAULT_TITLE_GENERATION_PROMPT_TEMPLATE` environment variable.

`DEFAULT_TITLE_GENERATION_PROMPT_TEMPLATE`:

```

### Task:

Generate a concise, 3-5 word title with an emoji summarizing the chat history.

### Guidelines:

- The title should clearly represent the main theme or subject of the conversation.
- Use emojis that enhance understanding of the topic, but avoid quotation marks or special formatting.
- Write the title in the chat's primary language; default to English if multilingual.
- Prioritize accuracy over excessive creativity; keep it clear and simple.

### Output:

JSON format: 

### Examples:

- ,
- ,
- ,
- ,
- ,
- 

### Chat History:

```

- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_FOLLOW_UP_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables follow up generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `FOLLOW_UP_GENERATION_PROMPT_TEMPLATE`

- Type: `str`
- Description: Prompt to use for generating several relevant follow-up questions.
- Default: The value of `DEFAULT_FOLLOW_UP_GENERATION_PROMPT_TEMPLATE` environment variable.

`DEFAULT_FOLLOW_UP_GENERATION_PROMPT_TEMPLATE`:

```

### Task:

Suggest 3-5 relevant follow-up questions or prompts that the user might naturally ask next in this conversation as a **user**, based on the chat history, to help continue or deepen the discussion.

### Guidelines:

- Write all follow-up questions from the user’s point of view, directed to the assistant.
- Make questions concise, clear, and directly related to the discussed topic(s).
- Only suggest follow-ups that make sense given the chat content and do not repeat what was already covered.
- If the conversation is very short or not specific, suggest more general (but relevant) follow-ups the user might ask.
- Use the conversation's primary language; default to English if multilingual.
- Response must be a JSON array of strings, no extra text or formatting.

### Output:

JSON format: 

### Chat History:

"
```

- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE`

- Type: `str`
- Description: Prompt to use when calling tools.
- Default: The value of `DEFAULT_TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE` environment variable.

`DEFAULT_TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE`:

```
Available Tools: 

Your task is to choose and return the correct tool(s) from the list of available tools based on the query. Follow these guidelines:

- Return only the JSON object, without any additional text or explanation.

- If no tools match the query, return an empty array:
   

- If one or more tools match the query, construct a JSON response containing a "tool_calls" array with objects that include:
   - "name": The tool's name.
   - "parameters": A dictionary of required parameters and their corresponding values.

The format for the JSON response is strictly:

```

- Persistence: This environment variable is a `PersistentConfig` variable.

### Code Execution

#### `ENABLE_CODE_EXECUTION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_ENGINE`

- Type: `str`
- Default: `pyodide`
- Description: Specifies the code execution engine to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_URL`

- Type: `str`
- Default: `None`
- Description: Specifies the Jupyter URL to use for code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_AUTH`

- Type: `str`
- Default: `None`
- Description: Specifies the Jupyter authentication method to use for code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_AUTH_TOKEN`

- Type: `str`
- Default: `None`
- Description: Specifies the Jupyter authentication token to use for code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_AUTH_PASSWORD`

- Type: `str`
- Default: `None`
- Description: Specifies the Jupyter authentication password to use for code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_EXECUTION_JUPYTER_TIMEOUT`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the timeout for Jupyter code execution.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Code Interpreter

#### `ENABLE_CODE_INTERPRETER`

- Type: `bool`
- Default: `True`
- Description: Enables or disables code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_ENGINE`

- Type: `str`
- Default: `pyodide`
- Description: Specifies the code interpreter engine to use.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_BLACKLISTED_MODULES`

- Type: `str` (comma-separated list of module names)
- Default: None
- Description: Specifies a comma-separated list of Python modules that are blacklisted and cannot be imported or used within the code interpreter. This enhances security by preventing access to potentially sensitive or system-level functionalities.

#### `CODE_INTERPRETER_PROMPT_TEMPLATE`

- Type: `str`
- Default: `None`
- Description: Specifies the prompt template to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_URL`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Jupyter URL to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_AUTH`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Jupyter authentication method to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_AUTH_TOKEN`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Jupyter authentication token to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_AUTH_PASSWORD`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the Jupyter authentication password to use for code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `CODE_INTERPRETER_JUPYTER_TIMEOUT`

- Type: `str`
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the timeout for the Jupyter code interpreter.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Direct Connections (OpenAPI/MCPO Tool Servers)

#### `ENABLE_DIRECT_CONNECTIONS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables direct connections.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TOOL_SERVER_CONNECTIONS`

- Type: `str` (JSON array)
- Default: `[]`
- Description: Specifies a JSON array of tool server connection configurations. Each connection should define the necessary parameters to connect to external tool servers that implement the OpenAPI/MCPO protocol. The JSON must be properly formatted or it will fallback to an empty array.
- Example: 
```json
[
  
]
```
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! warning

The JSON data structure of `TOOL_SERVER_CONNECTIONS` might evolve over time as new features are added.

### Autocomplete

#### `ENABLE_AUTOCOMPLETE_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables autocomplete generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! info

When enabling `ENABLE_AUTOCOMPLETE_GENERATION`, ensure that you also configure `AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH` and `AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE` accordingly.

#### `AUTOCOMPLETE_GENERATION_INPUT_MAX_LENGTH`

- Type: `int`
- Default: `-1`
- Description: Sets the maximum input length for autocomplete generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE`

- Type: `str`
- Default: The value of the `DEFAULT_AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE` environment variable.

`DEFAULT_AUTOCOMPLETE_GENERATION_PROMPT_TEMPLATE`:

```

### Task:

You are an autocompletion system. Continue the text in `` based on the **completion type** in `` and the given language.

### **Instructions**:

1. Analyze `` for context and meaning.
2. Use `` to guide your output:
   - **General**: Provide a natural, concise continuation.
   - **Search Query**: Complete as if generating a realistic search query.
3. Start as if you are directly continuing ``. Do **not** repeat, paraphrase, or respond as a model. Simply complete the text.
4. Ensure the continuation:
   - Flows naturally from ``.
   - Avoids repetition, overexplaining, or unrelated ideas.
5. If unsure, return: ``.

### **Output Rules**:

- Respond only in JSON format: ``.

### **Examples**:

#### Example 1:

Input:
General
The sun was setting over the horizon, painting the sky
Output:

#### Example 2:

Input:
Search Query
Top-rated restaurants in
Output:

---

### Context:

#### Output:

```

- Description: Sets the prompt template for autocomplete generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Evaluation Arena Model

#### `ENABLE_EVALUATION_ARENA_MODELS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables evaluation arena models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_MESSAGE_RATING`

- Type: `bool`
- Default: `True`
- Description: Enables message rating feature.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_COMMUNITY_SHARING`

- Type: `bool`
- Default: `True`
- Description: Controls whether users can share content with the Open WebUI Community and access community resources. When enabled, this setting shows the following UI elements across the application:
  - **Prompts Workspace**: "Made by Open WebUI Community" section with a link to discover community prompts, and a "Share" button in the prompt menu dropdown
  - **Tools Workspace**: "Made by Open WebUI Community" section with a link to discover community tools, and a "Share" button in the tool menu dropdown
  - **Models Workspace**: "Made by Open WebUI Community" section with a link to discover community model presets, and a "Share" button in the model menu dropdown
  - **Functions Admin**: "Made by Open WebUI Community" section with a link to discover community functions
  - **Share Chat Modal**: "Share to Open WebUI Community" button when sharing a chat conversation
  - **Evaluation Feedbacks**: "Share to Open WebUI Community" button for contributing feedback history to the community leaderboard
  - **Stats Sync Modal**: Enables syncing usage statistics with the community
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! info

When `ENABLE_COMMUNITY_SHARING` is set to `False`, all community sharing buttons and community resource discovery sections will be hidden from the UI. Users will still be able to export content locally, but the option to share directly to the Open WebUI Community will not be available.

### Tags Generation

#### `ENABLE_TAGS_GENERATION`

- Type: `bool`
- Default: `True`
- Description: Enables or disables tag generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `TAGS_GENERATION_PROMPT_TEMPLATE`

- Type: `str`
- Default: The value of `DEFAULT_TAGS_GENERATION_PROMPT_TEMPLATE` environment variable.

`DEFAULT_TAGS_GENERATION_PROMPT_TEMPLATE`:

```

### Task:

Generate 1-3 broad tags categorizing the main themes of the chat history, along with 1-3 more specific subtopic tags.

### Guidelines:

- Start with high-level domains (e.g., Science, Technology, Philosophy, Arts, Politics, Business, Health, Sports, Entertainment, Education)
- Consider including relevant subfields/subdomains if they are strongly represented throughout the conversation
- If content is too short (less than 3 messages) or too diverse, use only ["General"]
- Use the chat's primary language; default to English if multilingual
- Prioritize accuracy over specificity

### Output:

JSON format: 

### Chat History:

```

- Description: Sets the prompt template for tag generation.
- Persistence: This environment variable is a `PersistentConfig` variable.

### API Key Endpoint Restrictions

#### `ENABLE_API_KEYS`

- Type: `bool`
- Default: `False`
- Description: Enables the API key creation feature, allowing users to generate API keys for programmatic access to Open WebUI.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! info

This variable replaces the deprecated `ENABLE_API_KEY` environment variable.

!!! info

For API Key creation (and the API keys themselves) to work, you need **both**:
1. Enable API keys globally using this setting (`ENABLE_API_KEYS`)
2. Grant the "API Keys" permission to users via Default Permissions or User Groups

**Note:** Administrators are not exempt—they must also be granted the permission via a User Group to use API keys. See the [Authentication Setup for API Key](getting-started/advanced-topics/monitoring/index.md#authentication-setup-for-api-key-) guide for detailed setup instructions.

#### `ENABLE_API_KEYS_ENDPOINT_RESTRICTIONS`

- Type: `bool`
- Default: `False`
- Description: Enables API key endpoint restrictions for added security and configurability, allowing administrators to limit which endpoints can be accessed using API keys.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! info

This variable replaces the deprecated `ENABLE_API_KEY_ENDPOINT_RESTRICTIONS` environment variable.

#### `API_KEYS_ALLOWED_ENDPOINTS`

- Type: `str`
- Description: Specifies a comma-separated list of allowed API endpoints when API key endpoint restrictions are enabled.
- Example: `/api/v1/messages,/api/v1/channels,/api/v1/chat/completions`
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! note

The value of `API_KEYS_ALLOWED_ENDPOINTS` should be a comma-separated list of endpoint URLs, such as `/api/v1/messages, /api/v1/channels`.

!!! info

This variable replaces the deprecated `API_KEY_ALLOWED_ENDPOINTS` environment variable.

### Model Caching

#### `ENABLE_BASE_MODELS_CACHE`

- Type: `bool`
- Default: `False`
- Description: When enabled, caches the list of base models from connected Ollama and OpenAI-compatible endpoints in memory. This reduces the number of API calls made to external model providers when loading the model selector, improving performance particularly for deployments with many users or slow connections to model endpoints. Can also be configured from Admin Panel > Settings > Connections > "Cache Base Model List".
- Persistence: This environment variable is a `PersistentConfig` variable.

**How the cache works:**

- **Initialization**: When enabled, base models are fetched and cached during application startup.
- **Storage**: The cache is stored in application memory (`app.state.BASE_MODELS`).
- **Cache Hit**: Subsequent requests for models return the cached list without contacting external endpoints.
- **Cache Refresh**: The cache is refreshed when:
  - The application restarts
  - The connection settings are saved in the **Admin Panel > Settings > Connections** (clicking the **Save** button on the bottom right will trigger a refresh and update the cache with the newly fetched models)
- **No TTL**: There is no automatic time-based expiration.

!!! tip Performance Consideration

Enable this setting in production environments where model lists are relatively stable. For development environments or when frequently adding/removing models from Ollama, you may prefer to leave it disabled for real-time model discovery.

#### `MODELS_CACHE_TTL`

- Type: `int`
- Default: `1`
- Description: Sets the cache time-to-live in seconds for model list responses from OpenAI and Ollama endpoints. This reduces API calls by caching the available models list for the specified duration. Set to empty string to disable caching entirely.

This caches the external model lists retrieved from configured OpenAI-compatible and Ollama API endpoints (not Open WebUI's internal model configurations). Higher values improve performance by reducing redundant API requests to external providers but may delay visibility of newly added or removed models on those endpoints. A value of 0 disables caching and forces fresh API calls each time.

!!! tip High-Traffic Recommendation

In high-traffic scenarios, increasing this value (e.g., to 300 seconds) can significantly reduce load on external API endpoints while still providing reasonably fresh model data.

!!! info "Two Caching Mechanisms"

Open WebUI has **two model caching mechanisms** that work independently:

| Setting | Type | Default | Refresh Trigger |
|---------|------|---------|-----------------|
| `ENABLE_BASE_MODELS_CACHE` | In-memory | `False` | App restart OR Admin Save |
| `MODELS_CACHE_TTL` | TTL-based | `1` second | Automatic after TTL expires |

For maximum performance, enable both: `ENABLE_BASE_MODELS_CACHE=True` with `MODELS_CACHE_TTL=300`.

#### `JWT_EXPIRES_IN`

- Type: `str`
- Default: `4w`
- Description: Sets the JWT expiration time in seconds. Valid time units: `s`, `m`, `h`, `d`, `w` or `-1` for no expiration.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! warning

Setting `JWT_EXPIRES_IN` to `-1` disables JWT expiration, making issued tokens valid forever. **This is extremely dangerous in production** and exposes your system to severe security risks if tokens are leaked or compromised.

**Always set a reasonable expiration time in production environments (e.g., `3600s`, `1h`, `7d` etc.) to limit the lifespan of authentication tokens.**

**NEVER use `-1` in a production environment.**

If you have already deployed with `JWT_EXPIRES_IN=-1`, you can rotate or change your `WEBUI_SECRET_KEY` to immediately invalidate all existing tokens.

## Security Variables

#### `ENABLE_FORWARD_USER_INFO_HEADERS`

- type: `bool`
- Default: `False`
- Description: Forwards user information (name, ID, email, role and chat-id) as X-headers to OpenAI API and Ollama API.
If enabled, the following headers are forwarded:
  - `X-OpenWebUI-User-Name`
  - `X-OpenWebUI-User-Id`
  - `X-OpenWebUI-User-Email`
  - `X-OpenWebUI-User-Role`
  - `X-OpenWebUI-Chat-Id`

#### `ENABLE_WEB_LOADER_SSL_VERIFICATION`

- Type: `bool`
- Default: `True`
- Description: Bypass SSL Verification for RAG on Websites.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `WEBUI_SESSION_COOKIE_SAME_SITE`

- Type: `str`
- Options:
  - `lax` - Sets the `SameSite` attribute to lax, allowing session cookies to be sent with
requests initiated by third-party websites.
  - `strict` - Sets the `SameSite` attribute to strict, blocking session cookies from being sent
with requests initiated by third-party websites.
  - `none` - Sets the `SameSite` attribute to none, allowing session cookies to be sent with
requests initiated by third-party websites, but only over HTTPS.
- Default: `lax`
- Description: Sets the `SameSite` attribute for session cookies.

!!! warning

When `ENABLE_OAUTH_SIGNUP` is enabled, setting `WEBUI_SESSION_COOKIE_SAME_SITE` to `strict` can cause login failures. This is because Open WebUI uses a session cookie to validate the callback from the OAuth provider, which helps prevent CSRF attacks.

However, a `strict` session cookie is not sent with the callback request, leading to potential login issues. If you experience this problem, use the default `lax` value instead.

#### `WEBUI_SESSION_COOKIE_SECURE`

- Type: `bool`
- Default: `False`
- Description: Sets the `Secure` attribute for session cookies if set to `True`.

#### `WEBUI_AUTH_COOKIE_SAME_SITE`

- Type: `str`
- Options:
  - `lax` - Sets the `SameSite` attribute to lax, allowing auth cookies to be sent with
requests initiated by third-party websites.
  - `strict` - Sets the `SameSite` attribute to strict, blocking auth cookies from being sent
with requests initiated by third-party websites.
  - `none` - Sets the `SameSite` attribute to none, allowing auth cookies to be sent with
requests initiated by third-party websites, but only over HTTPS.
- Default: `lax`
- Description: Sets the `SameSite` attribute for auth cookies.

!!! info

If the value is not set, `WEBUI_SESSION_COOKIE_SAME_SITE` will be used as a fallback.

#### `WEBUI_AUTH_COOKIE_SECURE`

- Type: `bool`
- Default: `False`
- Description: Sets the `Secure` attribute for auth cookies if set to `True`.

!!! info

If the value is not set, `WEBUI_SESSION_COOKIE_SECURE` will be used as a fallback.

#### `WEBUI_AUTH`

- Type: `bool`
- Default: `True`
- Description: This setting enables or disables authentication.

!!! danger

If set to `False`, authentication will be disabled for your Open WebUI instance. However, it's
important to note that turning off authentication is only possible for fresh installations without
any existing users. If there are already users registered, you cannot disable authentication
directly. Ensure that no users are present in the database if you intend to turn off `WEBUI_AUTH`.

#### `ENABLE_PASSWORD_VALIDATION`

- Type: `bool`
- Default: `False`
- Description: Enables password complexity validation for user accounts. When enabled, passwords must meet the complexity requirements defined by `PASSWORD_VALIDATION_REGEX_PATTERN` during signup, password updates, and user creation operations. This helps enforce stronger password policies across the application.

!!! info

Password validation is applied to:
- New user registration (signup)
- Password changes through user settings
- Admin-initiated user creation
- Password resets

Existing users with passwords that don't meet the new requirements are **not automatically forced to update their passwords**, but will need to meet the requirements when they next change their password.

#### `PASSWORD_VALIDATION_REGEX_PATTERN`

- Type: `str`
- Default: `^(?=.*[a-z])(?=.*[A-Z])(?=.*/d)(?=.*[^/w/s]).$`
- Description: Regular expression pattern used to validate password complexity when `ENABLE_PASSWORD_VALIDATION` is enabled. The default pattern requires passwords to be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.

!!! warning

**Custom Pattern Considerations**

When defining a custom regex pattern, ensure it:
- Is a valid regular expression that Python's `re` module can compile
- Balances security requirements with user experience
- Is thoroughly tested before deployment to avoid locking users out

Invalid regex patterns will cause password validation to fail, potentially preventing user registration and password changes.

#### `WEBUI_SECRET_KEY`

- Type: `str`
- Default: `t0p-s3cr3t`
- Docker Default: Randomly generated on first start
- Description: Overrides the randomly generated string used for JSON Web Token and **encryption of sensitive data** (like OAuth tokens for MCP).

!!! danger Critical for Docker/Production

You **MUST** set `WEBUI_SECRET_KEY` to a secure, persistent value.

If you do NOT set this:
1.  It will be randomly generated each time the container restarts/recreates.
2.  **All OAuth sessions will become invalid.**
3.  **MCP Tools will break** (Error: `Error decrypting tokens`) because they cannot decrypt the tokens stored with the previous key.
4.  You will be logged out.

**Do not leave this unset in production.**

!!! warning

**Required for Multi-Worker and Multi-Node Deployments AND HIGHLY RECOMMENDED IN SINGLE-WORKER ENVIRONMENTS**

When deploying Open WebUI with `UVICORN_WORKERS > 1` or in a multi-node/worker cluster with a load balancer (e.g. helm/kubectl/kubernetes/k8s, you **must** set this variable. Without it, the following issues will occur:

- Session management will fail across workers
- Application state will be inconsistent between instances
- Websocket connections will not function properly in distributed setups
- Users may experience intermittent authentication failures

#### `ENABLE_VERSION_UPDATE_CHECK`

- Type: `bool`
- Default: `True`
- Description: When enabled, the application makes automatic update checks and notifies you about version updates.

!!! info

If `OFFLINE_MODE` is enabled, this `ENABLE_VERSION_UPDATE_CHECK` flag is always set to `false` automatically.

#### `OFFLINE_MODE`

- Type: `bool`
- Default: `False`
- Description: Disables Open WebUI's network connections for update checks and automatic model downloads.

!!! info

**Disabled when enabled:**

- Automatic version update checks (see flag `ENABLE_VERSION_UPDATE_CHECK`)
- Downloads of embedding models from Hugging Face Hub
  - If you did not download an embedding model prior to activating `OFFLINE_MODE` any RAG, web search and document analysis functionality may not work properly
- Update notifications in the UI (see flag `ENABLE_VERSION_UPDATE_CHECK`)

**Still functional:**

- External LLM API connections (OpenAI, etc.)
- OAuth authentication providers
- Web search and RAG with external APIs

Read more about `offline mode` in the [offline mode guide](tutorials/offline-mode.md).

#### `HF_HUB_OFFLINE`

- Type: `int`
- Default: `0`
- Description: Tells Hugging Face whether we want to launch in offline mode, so to not connect to hugging face and prevent all automatic model downloads

!!! info

Downloads of models, sentence transformers and other configurable items will NOT WORK when this is set to `1`.
RAG will also not work on a default installation, if this is set to `True`.

#### `RESET_CONFIG_ON_START`

- Type: `bool`
- Default: `False`
- Description: Resets the `config.json` file on startup.

#### `SAFE_MODE`

- Type: `bool`
- Default: `False`
- Description: Enables safe mode, which disables potentially unsafe features, deactivating all functions.

#### `CORS_ALLOW_ORIGIN`

- Type: `str`
- Default: `*`
- Description: Sets the allowed origins for Cross-Origin Resource Sharing (CORS). Smicolon ';' separated list of allowed origins.

!!! warning

**This variable is required to be set**, otherwise you may experience Websocket issues and weird "/" responses or "Unexpected token 'd', "data: /
```

- Description: Defines the ComfyUI workflow configuration in JSON format. Export from ComfyUI using "Save (API Format)" to ensure compatibility.
- Persistence: This environment variable is a `PersistentConfig` variable.

##### `COMFYUI_WORKFLOW_NODES`

- Type: `list[dict]`
- Default: `[]`
- Description: Specifies the ComfyUI workflow node mappings for image generation, defining which nodes handle prompt, model, dimensions, and other parameters. Configured automatically via the admin UI.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### Image Editing

##### `IMAGES_EDIT_COMFYUI_BASE_URL`

- Type: `str`
- Default: ``
- Description: Configures the ComfyUI base URL for image editing operations, enabling self-hosted ComfyUI workflows for image manipulation.
- Persistence: This environment variable is a `PersistentConfig` variable.

##### `IMAGES_EDIT_COMFYUI_API_KEY`

- Type: `str`
- Default: ``
- Description: Provides authentication for ComfyUI image editing API requests when the ComfyUI instance requires API key authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

##### `IMAGES_EDIT_COMFYUI_WORKFLOW`

- Type: `str` (JSON)
- Default: ``
- Description: Defines the ComfyUI workflow configuration in JSON format for image editing operations. Must include nodes for image input, prompt, and output. Export from ComfyUI using "Save (API Format)".
- Persistence: This environment variable is a `PersistentConfig` variable.

##### `IMAGES_EDIT_COMFYUI_WORKFLOW_NODES`

- Type: `list[dict]`
- Default: `[]`
- Description: Specifies the ComfyUI workflow node mappings for image editing, defining which nodes handle image input, prompt, model, dimensions, and other parameters. Configured automatically via the admin UI.
- Persistence: This environment variable is a `PersistentConfig` variable.

---

### AUTOMATIC1111

#### `AUTOMATIC1111_BASE_URL`

- Type: `str`
- Default: ``
- Description: Specifies the URL to AUTOMATIC1111's Stable Diffusion API (e.g., `http://127.0.0.1:7860`).
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUTOMATIC1111_API_AUTH`

- Type: `str`
- Default: ``
- Description: Sets the AUTOMATIC1111 API authentication credentials if required.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `AUTOMATIC1111_PARAMS`

- Type: `str` (JSON)
- Default: ``
- Description: Additional parameters in JSON format to pass to AUTOMATIC1111 API requests (e.g., ``).
- Persistence: This environment variable is a `PersistentConfig` variable.

## OAuth

!!! info

You can only configure one OAUTH provider at a time. You cannot have two or more OAUTH providers configured simultaneously.

#### `ENABLE_OAUTH_SIGNUP`

- Type: `bool`
- Default: `False`
- Description: Enables account creation when signing up via OAuth. Distinct from `ENABLE_SIGNUP`.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! danger

`ENABLE_LOGIN_FORM` must be set to `False` when `ENABLE_OAUTH_SIGNUP` is set to `True`. Failure to do so will result in the inability to login.

#### `ENABLE_OAUTH_PERSISTENT_CONFIG`

- Type: `bool`
- Default: `True`
- Description: Controls whether OAuth-related settings are persisted in the database after the first launch.

!!! info

By default, OAuth configurations are stored in the database and managed via the Admin Panel after the initial setup. Set this variable to `False` to force Open WebUI to **always** read OAuth settings from the environment variables on every restart. This is ideal for environments using GitOps or immutable infrastructure where configuration is managed exclusively through external files (e.g., Docker Compose, Kubernetes ConfigMaps).

#### `OAUTH_SUB_CLAIM`

- Type: `str`
- Default: `None`
- Description: Overrides the default claim used to identify a user's unique ID (`sub`) from the OAuth/OIDC provider's user info response. By default, Open WebUI attempts to infer this from the provider's configuration. This variable allows you to explicitly specify which claim to use. For example, if your identity provider uses 'employee_id' as the unique identifier, you would set this variable to 'employee_id'.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_MERGE_ACCOUNTS_BY_EMAIL`

- Type: `bool`
- Default: `False`
- Description: If enabled, merges OAuth accounts with existing accounts using the same email
address. This is considered unsafe as not all OAuth providers will verify email addresses and can lead to potential account takeovers.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_OAUTH_WITHOUT_EMAIL`

- Type: `bool`
- Default: `False`
- Description: Enables authentication with OpenID Connect (OIDC) providers that do not support or expose an email scope. When enabled, Open WebUI will create and manage user accounts without requiring an email address from the OAuth provider.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! warning

**Use with Caution**

Enabling this option bypasses email-based user identification, which is the standard method for uniquely identifying users across authentication systems. When enabled:

- User accounts will be created using the `sub` claim (or the claim specified in `OAUTH_SUB_CLAIM`) as the primary identifier
- Email-based features such as password recovery, email notifications, and account merging via `OAUTH_MERGE_ACCOUNTS_BY_EMAIL` will not function properly
- Ensure your OIDC provider's `sub` claim is stable and unique to prevent authentication conflicts

Only enable this if your identity provider does not support email scope and you have alternative user identification mechanisms in place.

This setting is designed for enterprise environments using identity providers that:
- Use employee IDs, usernames, or other non-email identifiers as the primary user claim
- Have privacy policies that prevent sharing email addresses via OAuth
- Operate in air-gapped or highly restricted networks where email-based services are unavailable

For most standard OAuth providers (Google, Microsoft, GitHub, etc.), this setting should remain `False`.

#### `OAUTH_UPDATE_PICTURE_ON_LOGIN`

- Type: `bool`
- Default: `False`
- Description: If enabled, updates the local user profile picture with the OAuth-provided picture on login.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! info

If the OAuth picture claim is disabled by setting `OAUTH_PICTURE_CLAIM` to `''` (empty string), then setting this variable to `true` will not update the user profile pictures.

#### `ENABLE_OAUTH_ID_TOKEN_COOKIE`

- Type: `bool`
- Default: `True`
- Description: Controls whether the **legacy** `oauth_id_token` cookie (unsafe, not recommended, token can go stale/orphaned) is set in the browser upon a successful OAuth login. This is provided for **backward compatibility** with custom tools or older versions that might rely on scraping this cookie. **The new, recommended approach is to use the server-side session management.**
- Usage: For new and secure deployments, **it is recommended to set this to `False`** to minimize the information exposed to the client-side. Keep it as `True` only if you have integrations that depend on the old cookie-based method.

#### `OAUTH_CLIENT_INFO_ENCRYPTION_KEY`

- Type: `str`
- Default: Falls back to the value of `WEBUI_SECRET_KEY`.
- Description: Specifies the secret key used to encrypt and decrypt OAuth client tokens stored server-side in the database. This is a critical security component for OAuth client tokens. If not set, it defaults to using the main `WEBUI_SECRET_KEY`, but it is highly recommended to set it to a unique, securely generated value for production environments. `OAUTH_CLIENT_INFO_ENCRYPTION_KEY` is used in conjunction with OAuth 2.1 MCP server authentication.

#### `OAUTH_SESSION_TOKEN_ENCRYPTION_KEY`

- Type: `str`
- Default: Falls back to the value of `WEBUI_SECRET_KEY`.
- Description: Specifies the secret key used to encrypt and decrypt OAuth tokens stored server-side in the database. This is a critical security component for protecting user credentials at rest. If not set, it defaults to using the main `WEBUI_SECRET_KEY`, but it is highly recommended to set it to a unique, securely generated value for production environments.

!!! warning

**Required for Multi-Replica Deployments**
In any production environment running more than one instance of Open WebUI (e.g., Docker Swarm, Kubernetes), this variable **MUST** be explicitly set to a persistent, shared secret. If left unset, each replica will generate or use a different key, causing session decryption to fail intermittently as user requests are load-balanced across instances.

#### `WEBUI_AUTH_TRUSTED_EMAIL_HEADER`

- Type: `str`
- Description: Defines the trusted request header for authentication. See [SSO docs](features/auth/sso/index.md).

#### `WEBUI_AUTH_TRUSTED_NAME_HEADER`

- Type: `str`
- Description: Defines the trusted request header for the username of anyone registering with the
`WEBUI_AUTH_TRUSTED_EMAIL_HEADER` header. See [SSO docs](features/auth/sso/index.md).

#### `WEBUI_AUTH_TRUSTED_GROUPS_HEADER`

- Type: `str`
- Description: Defines the trusted request header containing a comma-separated list of group memberships for the user when using trusted header authentication. See [SSO docs](features/auth/sso/index.md).

### Google

See https://support.google.com/cloud/answer/6158849?hl=en

!!! info

You must also set `OPENID_PROVIDER_URL` or otherwise logout may not work.

#### `GOOGLE_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for Google OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GOOGLE_CLIENT_SECRET`

- Type: `str`
- Description: Sets the client secret for Google OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GOOGLE_OAUTH_SCOPE`

- Type: `str`
- Default: `openid email profile`
- Description: Sets the scope for Google OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GOOGLE_REDIRECT_URI`

- Type: `str`
- Default: `/oauth/google/callback`
- Description: Sets the redirect URI for Google OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Microsoft

See https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app

!!! info

You must also set `OPENID_PROVIDER_URL` or otherwise logout may not work.

#### `MICROSOFT_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for Microsoft OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_CLIENT_SECRET`

- Type: `str`
- Description: Sets the client secret for Microsoft OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_CLIENT_TENANT_ID`

- Type: `str`
- Description: Sets the tenant ID for Microsoft OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_OAUTH_SCOPE`

- Type: `str`
- Default: `openid email profile`
- Description: Sets the scope for Microsoft OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_REDIRECT_URI`

- Type: `str`
- Default: `/oauth/microsoft/callback`
- Description: Sets the redirect URI for Microsoft OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_CLIENT_LOGIN_BASE_URL`

- Type: `str`
- Default: `https://login.microsoftonline.com`
- Description: Sets the base login URL for Microsoft OAuth authentication. Allows configuration of alternative login endpoints for government clouds or custom deployments.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `MICROSOFT_CLIENT_PICTURE_URL`

- Type: `str`
- Default: `https://graph.microsoft.com/v1.0/me/photo/$value`
- Description: Specifies the Microsoft Graph API endpoint for retrieving user profile pictures during OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

### GitHub

See https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps

!!! info

You must also set `OPENID_PROVIDER_URL` or otherwise logout may not work.

#### `GITHUB_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for GitHub OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GITHUB_CLIENT_SECRET`

- Type: `str`
- Description: Sets the client secret for GitHub OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GITHUB_CLIENT_SCOPE`

- Type: `str`
- Default: `user:email`
- Description: Specifies the scope for GitHub OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `GITHUB_CLIENT_REDIRECT_URI`

- Type: `str`
- Default: `/oauth/github/callback`
- Description: Sets the redirect URI for GitHub OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Feishu

See https://open.feishu.cn/document/sso/web-application-sso/login-overview

#### `FEISHU_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for Feishu OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `FEISHU_CLIENT_SECRET`

- Type: `str`
- Description: Sets the client secret for Feishu OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `FEISHU_CLIENT_SCOPE`

- Type: `str`
- Default: `contact:user.base:readonly`
- Description: Specifies the scope for Feishu OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `FEISHU_CLIENT_REDIRECT_URI`

- Type: `str`
- Description: Sets the redirect URI for Feishu OAuth.
- Persistence: This environment variable is a `PersistentConfig` variable.

### OpenID (OIDC)

#### `OAUTH_CLIENT_ID`

- Type: `str`
- Description: Sets the client ID for OIDC.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_CLIENT_SECRET`

- Type: `str`
- Description: Sets the client secret for OIDC.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OPENID_PROVIDER_URL`

- Type: `str`
- Description: Path to the `.well-known/openid-configuration` endpoint
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! danger

The environment variable `OPENID_PROVIDER_URL` MUST be configured, otherwise the logout functionality will not work for most providers.
Even when using Microsoft, GitHub or other providers, you MUST set the `OPENID_PROVIDER_URL` environment variable.

#### `OPENID_REDIRECT_URI`

- Type: `str`
- Default: `/oauth/oidc/callback`
- Description: Sets the redirect URI for OIDC
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_SCOPES`

- Type: `str`
- Default: `openid email profile`
- Description: Sets the scope for OIDC authentication. `openid` and `email` are required.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_CODE_CHALLENGE_METHOD`

- Type: `str`
- Options:
  - `S256` - Hash `code_verifier` with SHA-256.
- Default: Empty string (' '), since `None` is set as default.
- Description: Specifies the code challenge method for OAuth authentication. Set to `S256` when PKCE is required by the provider.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_PROVIDER_NAME`

- Type: `str`
- Default: `SSO`
- Description: Sets the name for the OIDC provider.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_USERNAME_CLAIM`

- Type: `str`
- Default: `name`
- Description: Set username claim for OpenID.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_EMAIL_CLAIM`

- Type: `str`
- Default: `email`
- Description: Set email claim for OpenID.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_PICTURE_CLAIM`

- Type: `str`
- Default: `picture`
- Description: Set picture (avatar) claim for OpenID.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! info

If `OAUTH_PICTURE_CLAIM` is set to `''` (empty string), then the OAuth picture claim is disabled and the user profile pictures will not be saved.

#### `OAUTH_GROUP_CLAIM`

- Type: `str`
- Default: `groups`
- Description: Specifies the group claim for OAuth authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_OAUTH_ROLE_MANAGEMENT`

- Type: `bool`
- Default: `False`
- Description: Enables role management for OAuth delegation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_OAUTH_GROUP_MANAGEMENT`

- Type: `bool`
- Default: `False`
- Description: Enables or disables OAuth group management.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_OAUTH_GROUP_CREATION`

- Type: `bool`
- Default: `False`
- Description: When enabled, groups from OAuth claims that don't exist in Open WebUI will be automatically created.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_BLOCKED_GROUPS`

- Type: `str`
- Default: `[]`
- Description: JSON array of group names that are blocked from accessing the application. Users belonging to these groups will be denied access even if they have valid OAuth credentials.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_ROLES_CLAIM`

- Type: `str`
- Default: `roles`
- Description: Sets the roles claim to look for in the OIDC token.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_ALLOWED_ROLES`

- Type: `str`
- Default: `user,admin`
- Description: Sets the roles that are allowed access to the platform.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_ADMIN_ROLES`

- Type: `str`
- Default: `admin`
- Description: Sets the roles that are considered administrators.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_ROLES_SEPARATOR`

- Type: `str`
- Default: `,`
- Description: Allows custom role separators for for splitting the `OAUTH_*_ROLES` variables. Meant for OAuth roles that contain commas; useful for roles specified in LDAP syntax or other systems where commas are part of role names. If the claim is a string and contains the separator, it will be also split by that separator.

#### `OAUTH_GROUPS_SEPARATOR`

- Type: `str`
- Default: `;`
- Description: Specifies the delimiter used to parse multiple group names from the OAuth group claim. This separator is used when the identity provider returns group memberships as a delimited string rather than an array. Useful when integrating with systems that use non-standard separators or when group names themselves contain commas.

#### `OAUTH_ALLOWED_DOMAINS`

- Type: `str`
- Default: `*`
- Description: Specifies the allowed domains for OAuth authentication. (e.g., "example1.com,example2.com").
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `OAUTH_AUDIENCE`

- Type: `str`
- Default: Empty string (' ')
- Description: Specifies an audience parameter passed to the OAuth provider's authorization endpoint during login. Some providers (such as Auth0 and Ory) use this value to determine the type of access token returned—without it, providers typically return an opaque token, while with it, they return a JWT that can be decoded and validated. This parameter is not part of the official OAuth/OIDC spec for authorization endpoints but is widely supported by some providers.

!!! info

This is useful when you need a JWT access token for downstream validation or when your OAuth provider requires an audience hint for proper token generation. For Auth0, this is typically your API identifier (e.g., `https://your-api.auth0.com/api/v2/`). For Ory, specify the resource server you want to access.

## LDAP

#### `ENABLE_LDAP`

- Type: `bool`
- Default: `False`
- Description: Enables or disables LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SERVER_LABEL`

- Type: `str`
- Description: Sets the label of the LDAP server.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SERVER_HOST`

- Type: `str`
- Default: `localhost`
- Description: Sets the hostname of the LDAP server.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SERVER_PORT`

- Type: `int`
- Default: `389`
- Description: Sets the port number of the LDAP server.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_ATTRIBUTE_FOR_MAIL`

- Type: `str`
- Description: Sets the attribute to use as mail for LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_ATTRIBUTE_FOR_USERNAME`

- Type: `str`
- Description: Sets the attribute to use as a username for LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_APP_DN`

- Type: `str`
- Description: Sets the distinguished name for the LDAP application.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_APP_PASSWORD`

- Type: `str`
- Description: Sets the password for the LDAP application.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SEARCH_BASE`

- Type: `str`
- Description: Sets the base to search for LDAP authentication.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SEARCH_FILTER`

- Type: `str`
- Default: `None`
- Description: Sets additional filter conditions for LDAP user search. This filter is **appended** to the automatically-generated username filter. Open WebUI automatically constructs the username portion of the filter using `LDAP_ATTRIBUTE_FOR_USERNAME`, so you should **not** include user placeholders like `%(user)s` or `%s` — these are not supported. Use this for additional conditions such as group membership restrictions (e.g., `(memberOf=cn=allowed-users,ou=groups,dc=example,dc=com)`). Alternative to `LDAP_SEARCH_FILTERS`.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_SEARCH_FILTERS`

- Type: `str`
- Description: Sets additional filter conditions for LDAP user search. This is an alias for `LDAP_SEARCH_FILTER`. The filter is appended to the automatically-generated username filter — do **not** include user placeholders like `%(user)s` or `%s`.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_USE_TLS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables TLS for LDAP connection.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_CA_CERT_FILE`

- Type: `str`
- Description: Sets the path to the LDAP CA certificate file.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_VALIDATE_CERT`

- Type: `bool`
- Description: Sets whether to validate the LDAP CA certificate.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_CIPHERS`

- Type: `str`
- Default: `ALL`
- Description: Sets the ciphers to use for LDAP connection.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_LDAP_GROUP_MANAGEMENT`

- Type: `bool`
- Default: `False`
- Description: Enables the group management feature.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `ENABLE_LDAP_GROUP_CREATION`

- Type: `bool`
- Default: `False`
- Description: If a group from LDAP does not exist in Open WebUI, it will be created automatically.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `LDAP_ATTRIBUTE_FOR_GROUPS`

- Type: `str`
- Default: `memberOf`
- Description: Specifies the LDAP attribute that contains the user's group memberships. `memberOf` is a standard attribute for this purpose in Active Directory environments.
- Persistence: This environment variable is a `PersistentConfig` variable.

## SCIM

#### `SCIM_ENABLED`

- Type: `bool`
- Default: `False`
- Description: Enables or disables SCIM 2.0 (System for Cross-domain Identity Management) support for automated user and group provisioning from identity providers like Okta, Azure AD, and Google Workspace.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `SCIM_TOKEN`

- Type: `str`
- Default: `""`
- Description: Sets the bearer token for SCIM authentication. This token must be provided by identity providers when making SCIM API requests. Generate a secure random token (e.g., using `openssl rand -base64 32`) and configure it in both Open WebUI and your identity provider.
- Persistence: This environment variable is a `PersistentConfig` variable.

## User Permissions

### Chat Permissions

#### `USER_PERMISSIONS_CHAT_CONTROLS`

- Type: `bool`
- Default: `True`
- Description: Acts as a master switch to enable or disable the main "Controls" button and panel in the chat interface. **If this is set to False, users will not see the Controls button, and the granular permissions below will have no effect**.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_VALVES`

- Type: `bool`
- Default: `True`
- Description: When `USER_PERMISSIONS_CHAT_CONTROLS` is enabled, this setting specifically controls the visibility of the "Valves" section within the chat controls panel.

#### `USER_PERMISSIONS_CHAT_SYSTEM_PROMPT`

- Type: `bool`
- Default: `True`
- Description: When `USER_PERMISSIONS_CHAT_CONTROLS` is enabled, this setting specifically controls the visibility of the customizable "System Prompt" section within the chat controls panel, folders and the user settings.

#### `USER_PERMISSIONS_CHAT_PARAMS`

- Type: `bool`
- Default: `True`
- Description: When `USER_PERMISSIONS_CHAT_CONTROLS` is enabled, this setting specifically controls the visibility of the "Advanced Parameters" section within the chat controls panel.

#### `USER_PERMISSIONS_CHAT_FILE_UPLOAD`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to upload files to chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_DELETE`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to delete chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_EDIT`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to edit chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_DELETE_MESSAGE`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to delete individual messages within chats. This provides granular control over message deletion capabilities separate from full chat deletion.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_CONTINUE_RESPONSE`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to continue AI responses. When disabled, users cannot use the "Continue Response" button, which helps prevent potential system prompt leakage through response continuation manipulation.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_REGENERATE_RESPONSE`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to regenerate AI responses. Controls access to both the standard regenerate button and the guided regeneration menu.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_RATE_RESPONSE`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to rate AI responses using the thumbs up/down feedback system. This controls access to the response rating functionality for evaluation and feedback collection.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_STT`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to use Speech-to-Text in chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_TTS`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to use Text-to-Speech in chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_CALL`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to make calls in chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_MULTIPLE_MODELS`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to use multiple models in chats.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_TEMPORARY`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user permission to create temporary chats. **Note:** Temporary chats disable backend document parsing for privacy.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_CHAT_TEMPORARY_ENFORCED`

- Type: `str`
- Default: `False`
- Description: Enables or disables enforced temporary chats for users.
- Persistence: This environment variable is a `PersistentConfig` variable.

### Feature Permissions

#### `USER_PERMISSIONS_FEATURES_DIRECT_TOOL_SERVERS`

- Type: `str`
- Default: `False`
- Description: Enables or disables user permission to access direct tool servers.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_WEB_SEARCH`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to use the web search feature.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_IMAGE_GENERATION`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to use the image generation feature.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_CODE_INTERPRETER`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to use code interpreter feature.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_MEMORIES`

- Type: `str`
- Default: `True`
- Description: Enables or disables user permission to use the [memory feature](features/memory.md).
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_FOLDERS`

- Type: `str`
- Default: `True`
- Description: Enables or disables the visibility of the Folders feature (chat sidebar) to users.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_NOTES`

- Type: `str`
- Default: `True`
- Description: Enables or disables the visibility of the Notes feature to users.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_CHANNELS`

- Type: `str`
- Default: `True`
- Description: Enables or disables the ability for users to create their own group channels.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_FEATURES_API_KEYS`

- Type: `bool`
- Default: `False`
- Description: Sets the permission for API key creation feature for users. When enabled, users will have the ability to create and manage API keys for programmatic access.
- Persistence: This environment variable is a `PersistentConfig` variable.

!!! info

For API Key creation (and the API keys themselves) to work, you need **both**:
1. Grant the "API Keys" permission to users via this setting or User Groups
2. Enable API keys globally using `ENABLE_API_KEYS`

**Note:** Administrators are not exempt—they must also be granted the permission via a User Group to use API keys. See the [Authentication Setup for API Key](getting-started/advanced-topics/monitoring/index.md#authentication-setup-for-api-key-) guide for detailed setup instructions.

### Workspace Permissions

#### `USER_PERMISSIONS_WORKSPACE_MODELS_ACCESS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_KNOWLEDGE_ACCESS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace knowledge.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_PROMPTS_ACCESS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace prompts.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_TOOLS_ACCESS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables user permission to access workspace tools.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_MODELS_ALLOW_PUBLIC_SHARING`

- Type: `str`
- Default: `False`
- Description: Enables or disables public sharing of workspace models.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_KNOWLEDGE_ALLOW_PUBLIC_SHARING`

- Type: `str`
- Default: `False`
- Description: Enables or disables public sharing of workspace knowledge.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_PROMPTS_ALLOW_PUBLIC_SHARING`

- Type: `str`
- Default: `False`
- Description: Enables or disables public sharing of workspace prompts.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_WORKSPACE_TOOLS_ALLOW_PUBLIC_SHARING`

- Type: `str`
- Default: `False`
- Description: Enables or disables public sharing of workspace tools.
- Persistence: This environment variable is a `PersistentConfig` variable.

#### `USER_PERMISSIONS_NOTES_ALLOW_PUBLIC_SHARING`

- Type: `str`
- Default: `True`
- Description: Enables or disables public sharing of notes.

### Settings Permissions

#### `USER_PERMISSIONS_SETTINGS_INTERFACE`

- Type: `bool`
- Default: `True`
- Description: Enables or disables user / group permissions for the interface settings section in the Settings Modal.
- Persistence: This environment variable is a `PersistentConfig` variable.

## Misc Environment Variables

These variables are not specific to Open WebUI but can still be valuable in certain contexts.

### Cloud Storage

#### `STORAGE_PROVIDER`

- Type: `str`
- Options:
  - `s3` - uses the S3 client library and related environment variables mentioned in [Amazon S3 Storage](#amazon-s3-storage.md)
  - `gcs` - uses the GCS client library and related environment variables mentioned in [Google Cloud Storage](#google-cloud-storage.md)
  - `azure` - uses the Azure client library and related environment variables mentioned in [Microsoft Azure Storage](#microsoft-azure-storage.md)
- Default: empty string (' '), which defaults to `local`
- Description: Sets the storage provider.

#### Amazon S3 Storage

#### `S3_ACCESS_KEY_ID`

- Type: `str`
- Description: Sets the access key ID for S3 storage.

#### `S3_ADDRESSING_STYLE`

- Type: `str`
- Default: `None`
- Description: Specifies the addressing style to use for S3 storage (e.g., 'path', 'virtual').

#### `S3_BUCKET_NAME`

- Type: `str`
- Description: Sets the bucket name for S3 storage.

#### `S3_ENDPOINT_URL`

- Type: `str`
- Description: Sets the endpoint URL for S3 storage.

!!! info

If the endpoint is an S3-compatible provider like MinIO that uses a TLS certificate signed by a private CA, set the environment variable `AWS_CA_BUNDLE` to the path of your PEM-encoded CA certificates file. See the [Amazon SDK Docs](https://docs.aws.amazon.com/sdkref/latest/guide/feature-gen-config.html) for more information.

#### `S3_KEY_PREFIX`

- Type: `str`
- Description: Sets the key prefix for a S3 object.

#### `S3_REGION_NAME`

- Type: `str`
- Description: Sets the region name for S3 storage.

#### `S3_SECRET_ACCESS_KEY`

- Type: `str`
- Description: Sets the secret access key for S3 storage.

#### `S3_USE_ACCELERATE_ENDPOINT`

- Type: `str`
- Default: `False`
- Description: Specifies whether to use the accelerated endpoint for S3 storage.

#### `S3_ENABLE_TAGGING`

- Type: `str`
- Default: `False`
- Description: Enables S3 object tagging after uploads for better organization, searching, and integration with file management policies. Always set to `False` when using Cloudflare R2, as R2 does not support object tagging.

#### Google Cloud Storage

#### `GOOGLE_APPLICATION_CREDENTIALS_JSON`

- Type: `str`
- Description: Contents of Google Application Credentials JSON file.
  - Optional - if not provided, credentials will be taken from the environment. User credentials if run locally and Google Metadata server if run on a Google Compute Engine.
  - A file can be generated for a service account following this [guide.](https://developers.google.com/workspace/guides/create-credentials#service-account)

#### `GCS_BUCKET_NAME`

- Type: `str`
- Description: Sets the bucket name for Google Cloud Storage. Bucket must already exist.

#### Microsoft Azure Storage

#### `AZURE_STORAGE_ENDPOINT`

- Type: `str`
- Description: Sets the endpoint URL for Azure Storage.

#### `AZURE_STORAGE_CONTAINER_NAME`

- Type: `str`
- Description: Sets the container name for Azure Storage.

#### `AZURE_STORAGE_KEY`

- Type: `str`
- Description: Set the access key for Azure Storage.
  - Optional - if not provided, credentials will be taken from the environment. User credentials if run locally and Managed Identity if run in Azure services.

### OpenTelemetry Configuration

!!! warning Additional Dependencies May Be Required

OpenTelemetry support requires additional Python dependencies that **may not be included by default** depending on your installation method (e.g., standard `pip install open-webui` versus Docker images).

If you encounter `ImportError` or missing module errors related to OpenTelemetry, you may need to install them manually:

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

#### `ENABLE_OTEL`

- Type: `bool`
- Default: `False`
- Description: Enables or disables OpenTelemetry for observability. When enabled, tracing, metrics, and logging data can be collected and exported to an OTLP endpoint.

#### `ENABLE_OTEL_TRACES`

- Type: `bool`
- Default: `False`
- Description: Enables or disables OpenTelemetry traces collection and export. This variable works in conjunction with `ENABLE_OTEL`.

#### `ENABLE_OTEL_METRICS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables OpenTelemetry metrics collection and export. This variable works in conjunction with `ENABLE_OTEL`.

#### `ENABLE_OTEL_LOGS`

- Type: `bool`
- Default: `False`
- Description: Enables or disables OpenTelemetry logging export. When enabled, application logs are sent to the configured OTLP endpoint. This variable works in conjunction with `ENABLE_OTEL`.

#### `OTEL_EXPORTER_OTLP_ENDPOINT`

- Type: `str`
- Default: `http://localhost:4317`
- Description: Specifies the default OTLP (OpenTelemetry Protocol) endpoint for exporting traces, metrics, and logs. This can be overridden for metrics if `OTEL_METRICS_EXPORTER_OTLP_ENDPOINT` is set, and for logs if `OTEL_LOGS_EXPORTER_OTLP_ENDPOINT` is set.

#### `OTEL_METRICS_EXPORTER_OTLP_ENDPOINT`

- Type: `str`
- Default: Value of `OTEL_EXPORTER_OTLP_ENDPOINT`
- Description: Specifies the dedicated OTLP endpoint for exporting OpenTelemetry metrics. If not set, it defaults to the value of `OTEL_EXPORTER_OTLP_ENDPOINT`. This is useful when separate endpoints for traces and metrics are used.

#### `OTEL_LOGS_EXPORTER_OTLP_ENDPOINT`

- Type: `str`
- Default: Value of `OTEL_EXPORTER_OTLP_ENDPOINT`
- Description: Specifies the dedicated OTLP endpoint for exporting OpenTelemetry logs. If not set, it defaults to the value of `OTEL_EXPORTER_OTLP_ENDPOINT`. This is useful when separate endpoints for logs, traces, and metrics are used.

#### `OTEL_EXPORTER_OTLP_INSECURE`

- Type: `bool`
- Default: `False`
- Description: If set to `True`, the OTLP exporter will use an insecure connection (e.g., HTTP for gRPC) for traces. For metrics, its behavior is governed by `OTEL_METRICS_EXPORTER_OTLP_INSECURE`, and for logs by `OTEL_LOGS_EXPORTER_OTLP_INSECURE`.

#### `OTEL_METRICS_EXPORTER_OTLP_INSECURE`

- Type: `bool`
- Default: Value of `OTEL_EXPORTER_OTLP_INSECURE`
- Description: If set to `True`, the OTLP exporter will use an insecure connection for metrics. If not specified, it uses the value of `OTEL_EXPORTER_OTLP_INSECURE`.

#### `OTEL_LOGS_EXPORTER_OTLP_INSECURE`

- Type: `bool`
- Default: Value of `OTEL_EXPORTER_OTLP_INSECURE`
- Description: If set to `True`, the OTLP exporter will use an insecure connection for logs. If not specified, it uses the value of `OTEL_EXPORTER_OTLP_INSECURE`.

#### `OTEL_SERVICE_NAME`

- Type: `str`
- Default: `open-webui`
- Description: Sets the service name that will be reported to your OpenTelemetry collector or observability platform. This helps identify your Open WebUI instance.

#### `OTEL_RESOURCE_ATTRIBUTES`

- Type: `str`
- Default: Empty string (' ')
- Description: Allows you to define additional resource attributes to be attached to all telemetry data, in a comma-separated `key1=val1,key2=val2` format.

#### `OTEL_TRACES_SAMPLER`

- Type: `str`
- Options: `parentbased_always_on`, `always_on`, `always_off`, `parentbased_always_off`, etc.
- Default: `parentbased_always_on`
- Description: Configures the sampling strategy for OpenTelemetry traces. This determines which traces are collected and exported to reduce data volume.

#### `OTEL_BASIC_AUTH_USERNAME`

- Type: `str`
- Default: Empty string (' ')
- Description: Sets the username for basic authentication with the default OTLP endpoint. This applies to traces, and by default, to metrics and logs unless overridden by their specific authentication variables.

#### `OTEL_BASIC_AUTH_PASSWORD`

- Type: `str`
- Default: Empty string (' ')
- Description: Sets the password for basic authentication with the default OTLP endpoint. This applies to traces, and by default, to metrics and logs unless overridden by their specific authentication variables.

#### `OTEL_METRICS_BASIC_AUTH_USERNAME`

- Type: `str`
- Default: Value of `OTEL_BASIC_AUTH_USERNAME`
- Description: Sets the username for basic authentication specifically for the OTLP metrics endpoint. If not specified, it uses the value of `OTEL_BASIC_AUTH_USERNAME`.

#### `OTEL_METRICS_BASIC_AUTH_PASSWORD`

- Type: `str`
- Default: Value of `OTEL_BASIC_AUTH_PASSWORD`
- Description: Sets the password for basic authentication specifically for the OTLP metrics endpoint. If not specified, it uses the value of `OTEL_BASIC_AUTH_PASSWORD`.

#### `OTEL_LOGS_BASIC_AUTH_USERNAME`

- Type: `str`
- Default: Value of `OTEL_BASIC_AUTH_USERNAME`
- Description: Sets the username for basic authentication specifically for the OTLP logs endpoint. If not specified, it uses the value of `OTEL_BASIC_AUTH_USERNAME`.

#### `OTEL_LOGS_BASIC_AUTH_PASSWORD`

- Type: `str`
- Default: Value of `OTEL_BASIC_AUTH_PASSWORD`
- Description: Sets the password for basic authentication specifically for the OTLP logs endpoint. If not specified, it uses the value of `OTEL_BASIC_AUTH_PASSWORD`.

#### `OTEL_OTLP_SPAN_EXPORTER`

- Type: `str`
- Options: `grpc`, `http`
- Default: `grpc`
- Description: Specifies the default protocol for exporting OpenTelemetry traces (gRPC or HTTP). This can be overridden for metrics if `OTEL_METRICS_OTLP_SPAN_EXPORTER` is set, and for logs if `OTEL_LOGS_OTLP_SPAN_EXPORTER` is set.

#### `OTEL_METRICS_OTLP_SPAN_EXPORTER`

- Type: `str`
- Options: `grpc`, `http`
- Default: Value of `OTEL_OTLP_SPAN_EXPORTER`
- Description: Specifies the protocol for exporting OpenTelemetry metrics (gRPC or HTTP). If not specified, it uses the value of `OTEL_OTLP_SPAN_EXPORTER`.

#### `OTEL_LOGS_OTLP_SPAN_EXPORTER`

- Type: `str`
- Options: `grpc`, `http`
- Default: Value of `OTEL_OTLP_SPAN_EXPORTER`
- Description: Specifies the protocol for exporting OpenTelemetry logs (gRPC or HTTP). If not specified, it uses the value of `OTEL_OTLP_SPAN_EXPORTER`.

### Database Pool

#### `DATABASE_URL`

- Type: `str`
- Default: `sqlite:///$/webui.db`
- Description: Specifies the complete database connection URL, following SQLAlchemy's URL scheme. This variable takes precedence over individual database connection parameters if explicitly set.

!!! info

**For PostgreSQL support, ensure you installed with `pip install open-webui[all]` instead of the basic installation.**
Supports SQLite, Postgres, and encrypted SQLite via SQLCipher.
**Changing the URL does not migrate data between databases.**

Documentation on the URL scheme is available [here](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls).

If your database password contains special characters, please ensure they are properly URL-encoded. For example, a password like `p@ssword` should be encoded as `p%40ssword`.

For configuration using individual parameters or encrypted SQLite, see the relevant sections below.

#### `ENABLE_DB_MIGRATIONS`

- Type: `bool`
- Default: `True`
- Description: Controls whether database migrations are automatically run on startup. In multi-pod or multi-worker deployments, set this to `False` on all pods except one to designate a "master" pod responsible for migrations, preventing race conditions or schema corruption.

!!! warning

**Required for Multi-Replica Setups**
For multi-replica or high-availability deployments (Kubernetes, Docker Swarm), you **MUST** use an external database (PostgreSQL) instead of SQLite. SQLite does not support concurrent writes from multiple instances and will result in database corruption or data inconsistency.

#### `DATABASE_TYPE`

- Type: `str`
- Default: `None` (automatically set to `sqlite` if `DATABASE_URL` uses default SQLite path)
- Description: Specifies the database type (e.g., `sqlite`, `postgresql`, `sqlite+sqlcipher`). This is used in conjunction with other individual parameters to construct the `DATABASE_URL` if a complete `DATABASE_URL` is not explicitly defined.
- Persistence: No

#### `DATABASE_USER`

- Type: `str`
- Default: `None`
- Description: Specifies the username for database authentication. This is used to construct the `DATABASE_URL` when a complete `DATABASE_URL` is not explicitly defined.
- Persistence: No

#### `DATABASE_PASSWORD`

- Type: `str`
- Default: `None`
- Description: Specifies the password for database authentication. This is used to construct the `DATABASE_URL` when a complete `DATABASE_URL` is not explicitly defined. If your password contains special characters, please ensure they are properly URL-encoded.
- Persistence: No

#### `DATABASE_HOST`

- Type: `str`
- Default: `None`
- Description: Specifies the hostname or IP address of the database server. This is used to construct the `DATABASE_URL` when a complete `DATABASE_URL` is not explicitly defined.
- Persistence: No

#### `DATABASE_PORT`

- Type: `int`
- Default: `None`
- Description: Specifies the port number of the database server. This is used to construct the `DATABASE_URL` when a complete `DATABASE_URL` is not explicitly defined.
- Persistence: No

#### `DATABASE_NAME`

- Type: `str`
- Default: `None`
- Description: Specifies the name of the database to connect to. This is used to construct the `DATABASE_URL` when a complete `DATABASE_URL` is not explicitly defined.
- Persistence: No

!!! info

When `DATABASE_URL` is not explicitly set, Open WebUI will attempt to construct it using a combination of `DATABASE_TYPE`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT`, and `DATABASE_NAME`. For this automatic construction to occur, **all** of these individual parameters must be provided. If any are missing, the default `DATABASE_URL` (SQLite file) or any explicitly set `DATABASE_URL` will be used instead.

#### `DATABASE_USER_ACTIVE_STATUS_UPDATE_INTERVAL`

- Type: `float`
- Default: `None`
- Description: Sets the minimum time interval in seconds between user active status updates in the database. Helps reduce write operations for high-traffic instances. Set to `0.0` to update on every activity.

#### `DATABASE_ENABLE_SESSION_SHARING`

- Type: `bool`
- Default: `False`
- Description: Controls database session sharing behavior. When enabled (`True`), `get_db_context` reuses existing database sessions, which can improve performance and scalability in high-concurrency environments. When disabled (`False`), new sessions are always created.

!!! tip Recommendations by Database Type

- **SQLite:** Keep this setting **disabled** (default `False`). Enabling session sharing on SQLite with limited hardware resources may cause performance issues.
- **PostgreSQL:** Consider **enabling** this setting (`True`) for improved performance, especially in multi-user or high-concurrency deployments.

This setting is very deployment-specific. Users are encouraged to experiment based on their hardware specs and database choice to find the optimal configuration.

!!! warning

Enabling this on low-spec hardware (e.g., Raspberry Pi, containers with limited CPU allocation) may cause significant slowdowns or timeouts. If you experience slow admin page loads or API timeouts after upgrading, ensure this setting is disabled.

### Encrypted SQLite with SQLCipher

For enhanced security, Open WebUI supports at-rest encryption for its primary SQLite database using SQLCipher. This is recommended for deployments handling sensitive data where using a larger database like PostgreSQL is not needed.

!!! warning Additional Dependencies Required

SQLCipher encryption requires additional dependencies that are **not included by default**. Before using this feature, you must install:

- The **SQLCipher system library** (e.g., `libsqlcipher-dev` on Debian/Ubuntu, `sqlcipher` on macOS via Homebrew)
- The **`sqlcipher3-wheels`** Python package (`pip install sqlcipher3-wheels`)

For Docker users, this means building a custom image with these dependencies included.

To enable encryption, you must configure two environment variables:

1. Set `DATABASE_TYPE="sqlite+sqlcipher"`.
2. Set `DATABASE_PASSWORD="your-secure-password"`.

When these are set and a full `DATABASE_URL` is **not** explicitly defined, Open WebUI will automatically create and use an encrypted database file at `./data/webui.db`.

!!! danger

- The **`DATABASE_PASSWORD`** environment variable is **required** when using `sqlite+sqlcipher`.
- The **`DATABASE_TYPE`** variable tells Open WebUI which connection logic to use. Setting it to `sqlite+sqlcipher` activates the encryption feature.

Ensure the database password is kept secure, as it is needed to decrypt and access all application data.

!!! warning Migrating Existing Data to SQLCipher

**Open WebUI does not support automatic migration from an unencrypted SQLite database to an encrypted SQLCipher database.** If you enable SQLCipher on an existing installation, the application will fail to read your existing unencrypted data.

To use SQLCipher with existing data, you must either start fresh (with users exporting/re-importing chats), manually migrate the database using external SQLite/SQLCipher tools, use filesystem-level encryption (LUKS/BitLocker) instead, or switch to PostgreSQL.

#### `DATABASE_SCHEMA`

- Type: `str`
- Default: `None`
- Description: Specifies the database schema to connect to.

#### `DATABASE_POOL_SIZE`

- Type: `int`
- Default: `None`
- Description: Specifies the pooling strategy and size of the database pool. By default SQLAlchemy will automatically chose the proper pooling strategy for the selected database connection. A value of `0` disables pooling. A value larger `0` will set the pooling strategy to `QueuePool` and the pool size accordingly.

!!! tip High-Concurrency Deployments

For deployments with many concurrent users, consider increasing both `DATABASE_POOL_SIZE` and `DATABASE_POOL_MAX_OVERFLOW`. A good starting point is `DATABASE_POOL_SIZE=15` and `DATABASE_POOL_MAX_OVERFLOW=20`.

**Important:** The combined total (`DATABASE_POOL_SIZE` + `DATABASE_POOL_MAX_OVERFLOW`) should remain well below your database server's `max_connections` limit. PostgreSQL defaults to 100 max connections, so keeping the combined total under 50-80 per Open WebUI instance is recommended to leave room for other clients and maintenance connections.

#### `DATABASE_POOL_MAX_OVERFLOW`

- Type: `int`
- Default: `0`
- Description: Specifies the database pool max overflow. This allows additional connections beyond `DATABASE_POOL_SIZE` during traffic spikes.

!!! info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.max_overflow).

#### `DATABASE_POOL_TIMEOUT`

- Type: `int`
- Default: `30`
- Description: Specifies the database pool timeout in seconds to get a connection.

!!! info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#sqlalchemy.pool.QueuePool.params.timeout).

#### `DATABASE_POOL_RECYCLE`

- Type: `int`
- Default: `3600`
- Description: Specifies the database pool recycle time in seconds.

!!! info

More information about this setting can be found [here](https://docs.sqlalchemy.org/en/20/core/pooling.html#setting-pool-recycle).

#### `DATABASE_ENABLE_SQLITE_WAL`

- Type: `bool`
- Default: `False`
- Description: Enables or disables SQLite WAL (Write-Ahead Logging) mode. When enabled, SQLite transactions can be managed more efficiently, allowing multiple readers and one writer concurrently, which can improve database performance, especially under high concurrency. **This setting only applies to SQLite databases.**

### Redis

#### `REDIS_URL`

- Type: `str`
- Description: Specifies the URL of the Redis instance or cluster host for storing application state.
- Examples:
  - `redis://localhost:6379/0`
  - `rediss://:password@localhost:6379/0` *(with password and TLS)*
  - `rediss://redis-cluster.redis.svc.cluster.local:6379/0?ssl_cert_reqs=required&ssl_certfile=/tls/redis/tls.crt&ssl_keyfile=/tls/redis/tls.key&ssl_ca_certs=/tls/redis/ca.crt` *(with mTLS)*

!!! warning

**Required for Multi-Worker and Multi-Node Deployments**

When deploying Open WebUI with `UVICORN_WORKERS > 1` or in a multi-node/worker cluster with a load balancer (e.g. helm/kubectl/kubernetes/k8s, you **must** set the `REDIS_URL` value. Without it, the following issues will occur:

- Session management will fail across workers
- Application state will be inconsistent between instances
- Websocket connections will not function properly in distributed setups
- Users may experience intermittent authentication failures

Redis serves as the central state store that allows multiple Open WebUI instances to coordinate and share critical application data.

!!! info

**Single Instance Deployments**

If you're running Open WebUI as a single instance with `UVICORN_WORKERS=1` (the default), Redis is **not required**. The application will function normally without it.

#### `REDIS_SENTINEL_HOSTS`

- Type: `str`
- Description: Comma-separated list of Redis Sentinels for app state. If specified, the "hostname" in `REDIS_URL` will be interpreted as the Sentinel service name.

#### `REDIS_SENTINEL_PORT`

- Type: `int`
- Default: `26379`
- Description: Sentinel port for app state Redis.

#### `REDIS_CLUSTER`

- Type: `bool`
- Default: `False`
- Description: Connect to a Redis Cluster instead of a single instance or using Redis Sentinels. If `True`, `REDIS_URL` must also be defined.

!!! info

This option has no effect if `REDIS_SENTINEL_HOSTS` is defined.

#### `REDIS_KEY_PREFIX`

- Type: `str`
- Default: `open-webui`
- Description: Customizes the Redis key prefix used for storing configuration values. This allows multiple Open WebUI instances to share the same Redis instance without key conflicts. When operating in Redis cluster mode, the prefix is formatted as `:` (e.g., `:config:*`) to enable multi-key operations on configuration keys within the same hash slot.

#### `REDIS_SOCKET_CONNECT_TIMEOUT`

- Type: `float` (seconds) or empty string for None
- Default: None (no timeout, uses redis-py library default)
- Description: Sets the socket connection timeout in seconds for Redis and Sentinel connections. This timeout applies to the initial TCP connection establishment. When set, it prevents indefinite blocking when attempting to connect to unreachable Redis nodes.

!!! danger

**Critical for Redis Sentinel Deployments**

Without a socket connection timeout, Redis Sentinel failover can cause the application to hang indefinitely when a master node goes offline. The application may become completely unresponsive and even fail to restart.

For Sentinel deployments, it is **strongly recommended** to set this value (e.g., `REDIS_SOCKET_CONNECT_TIMEOUT=5`).

!!! warning

**Interaction with WEBSOCKET_REDIS_OPTIONS**

If you explicitly set `WEBSOCKET_REDIS_OPTIONS`, this variable will **not** apply to the AsyncRedisManager used for websocket communication. In that case, you must include `socket_connect_timeout` directly within `WEBSOCKET_REDIS_OPTIONS`:
```bash
WEBSOCKET_REDIS_OPTIONS=''
```

If `WEBSOCKET_REDIS_OPTIONS` is not set, `REDIS_SOCKET_CONNECT_TIMEOUT` will be applied to websocket connections automatically.

#### `ENABLE_WEBSOCKET_SUPPORT`

- Type: `bool`
- Default: `True`
- Description: Enables websocket support in Open WebUI.

!!! warning

**Required for Multi-Worker and Multi-Node Deployments**

When deploying Open WebUI with `UVICORN_WORKERS > 1` or in a multi-node/worker cluster with a load balancer (e.g. helm/kubectl/kubernetes/k8s, you **must** set this variable. Without it, the following issues will occur:

- Session management will fail across workers
- Application state will be inconsistent between instances
- Websocket connections will not function properly in distributed setups
- Users may experience intermittent authentication failures

#### `WEBSOCKET_MANAGER`

- Type: `str`
- Default: `"" (empty string)`
- Description: Specifies the websocket manager to use. Allowed values include: `redis`

!!! warning

**Required for Multi-Worker and Multi-Node Deployments**

When deploying Open WebUI with `UVICORN_WORKERS > 1` or in a multi-node/worker cluster with a load balancer (e.g. helm/kubectl/kubernetes/k8s, you **must** set this variable. Without it, the following issues will occur:

- Session management will fail across workers
- Application state will be inconsistent between instances
- Websocket connections will not function properly in distributed setups
- Users may experience intermittent authentication failures

#### `WEBSOCKET_REDIS_URL`

- Type: `str`
- Default: `$`
- Description: Specifies the URL of the Redis instance or cluster host for websocket communication. It is distinct from `REDIS_URL` and in practice, it is recommended to set both.

!!! warning

**Required for Multi-Worker and Multi-Node Deployments**

When deploying Open WebUI with `UVICORN_WORKERS > 1` or in a multi-node/worker cluster with a load balancer (e.g. helm/kubectl/kubernetes/k8s, you **must** set this variable. Without it, the following issues will occur:

- Session management will fail across workers
- Application state will be inconsistent between instances
- Websocket connections will not function properly in distributed setups
- Users may experience intermittent authentication failures

#### `WEBSOCKET_SENTINEL_HOSTS`

- Type: `str`
- Description: Comma-separated list of Redis Sentinels for websocket. If specified, the "hostname" in `WEBSOCKET_REDIS_URL` will be interpreted as the Sentinel service name.

#### `WEBSOCKET_SENTINEL_PORT`

- Type: `int`
- Default: `26379`
- Description: Sentinel port for websocket Redis.

#### `WEBSOCKET_REDIS_CLUSTER`

- Type: `bool`
- Default: `$`
- Description: Specifies that websocket should communicate with a Redis Cluster instead of a single instance or using Redis Sentinels. If `True`, `WEBSOCKET_REDIS_URL` and/or `REDIS_URL` must also be defined.

!!! info

This option has no effect if `WEBSOCKET_SENTINEL_HOSTS` is defined.

#### `WEBSOCKET_REDIS_OPTIONS`

- Type: `str`
- Default: `` (empty, which allows `REDIS_SOCKET_CONNECT_TIMEOUT` to apply if set)
- Description: A string representation of a dictionary containing additional Redis connection options for the websocket Redis client (AsyncRedisManager). This allows you to specify advanced connection parameters such as SSL settings, timeouts, or other Redis client configurations that are not covered by the standard `WEBSOCKET_REDIS_URL`. The string should be formatted as valid JSON. For example: ``. All JSON encodable options listed [here](https://redis.readthedocs.io/en/stable/connections.html) can be used.

!!! warning

**AWS SSM and Docker compose cannot ingest raw JSON, as such you need to escape any double quotes like the following:**
``

!!! info

**Precedence with REDIS_SOCKET_CONNECT_TIMEOUT**

When this variable is left empty (default), `REDIS_SOCKET_CONNECT_TIMEOUT` is automatically applied to websocket connections if set. However, if you explicitly set `WEBSOCKET_REDIS_OPTIONS` to any value, `REDIS_SOCKET_CONNECT_TIMEOUT` will **not** be injected—you must include `socket_connect_timeout` manually within this JSON if needed.

#### `WEBSOCKET_SERVER_LOGGING`

- Type: `bool`
- Default: `false`
- Description: Controls logging for SocketIO server related to websocket operations.

!!! warning

**This can be very verbose, it is only recommended to use this flag when debugging Redis related issues.**

#### `WEBSOCKET_SERVER_ENGINEIO_LOGGING`

- Type: `bool`
- Default: `false`
- Description: Controls logging for EngineIO server related to websocket operations.

!!! warning

**This can be very verbose, it is only recommended to use this flag when debugging Redis related issues.**

#### `WEBSOCKET_SERVER_PING_TIMEOUT`

- Type: `int`
- Default: `20`
- Description: The timeout for a ping to Redis in seconds.

#### `WEBSOCKET_SERVER_PING_INTERVAL`

- Type: `int`
- Default: `25`
- Description: The frequency for a ping to Redis in seconds.

#### `ENABLE_STAR_SESSIONS_MIDDLEWARE`

- Type: `bool`
- Default: `False`
- Description: Enables Redis-based session storage for OAuth authentication flows using the StarSessions middleware. When enabled, OAuth session state is stored in Redis instead of browser cookies, which can help resolve CSRF errors in multi-replica deployments where session data needs to be shared across pods. Experimental feature that enables Redis-based session storage for OAuth flows using StarSessions middleware, helping resolve CSRF errors in multi-replica deployments.
- Persistence: This is an experimental environment variable.

!!! warning
**Experimental Feature - Known Limitations**

This feature is currently experimental and has known compatibility issues:

- **Redis Sentinel and Redis Cluster configurations are not yet supported** and will cause authentication failures if this setting is enabled
- Only basic Redis setups (single instance or standard Redis URL) are currently compatible
- This feature was introduced to address CSRF "mismatching_state" errors in multi-pod deployments, but it is disabled by default due to ongoing compatibility work

**Only enable this setting if:**
- You are experiencing persistent CSRF errors during OAuth login in a multi-replica deployment
- You are using a basic Redis setup (not Sentinel or Cluster)
- You have confirmed that `WEBUI_SECRET_KEY` is set to the same value across all replicas
- You understand this is an experimental feature that may change or be removed in future releases

For most deployments, the default browser cookie-based session management is sufficient and more stable.

### Uvicorn Settings

#### `UVICORN_WORKERS`

- Type: `int`
- Default: `1`
- Description: Controls the number of worker processes that Uvicorn spawns to handle requests. Each worker runs its own instance of the application in a separate process.

!!! info

When deploying in orchestrated environments like Kubernetes or using Helm charts, it's recommended to keep UVICORN_WORKERS set to 1. Container orchestration platforms already provide their own scaling mechanisms through pod replication, and using multiple workers inside containers can lead to resource allocation issues and complicate horizontal scaling strategies.

If you use UVICORN_WORKERS, you also need to ensure that related environment variables for scalable multi-worker setups are set accordingly.

!!! warning Database Migrations with Multiple Workers / Multi-Pod Deployments
When `UVICORN_WORKERS > 1` or when running multiple replicas, starting the application can trigger concurrent database migrations from multiple processes, potentially causing database schema corruption or inconsistent states.

**Recommendation:**
To handle migrations safely in multi-process/multi-pod environments, you can:
1.  **Designate a Master (Recommended):** Set `ENABLE_DB_MIGRATIONS=False` on all but one instance/worker. The instance with `ENABLE_DB_MIGRATIONS=True` (default) will handle the migration, while others will wait or skip it.
2.  **Scale Down:** Temporarily scale down to a single instance/worker to let migrations finish before scaling back up.

**For Kubernetes, Helm, and Orchestrated Setups:**
It is recommended to use the `ENABLE_DB_MIGRATIONS` variable to designate a specific pod for migrations, or use an init container/job to handle migrations before scaling up the main application pods. This ensures schema updates are applied exactly once.

### Cache Settings

#### `CACHE_CONTROL`

- Type: `str`
- Default: Not set (no Cache-Control header added)
- Description: Sets the Cache-Control header for all HTTP responses. Supports standard directives like `public`, `private`, `no-cache`, `no-store`, `must-revalidate`, `max-age=seconds`, etc. If an invalid value is provided, defaults to `"no-store, max-age=0"` (no caching).
- Examples:
  - `"private, max-age=86400"` - Cache privately for 24 hours
  - `"public, max-age=3600, must-revalidate"` - Cache publicly for 1 hour, then revalidate
  - `"no-cache, no-store, must-revalidate"` - Never cache

### Proxy Settings

Open WebUI supports using proxies for HTTP and HTTPS retrievals. To specify proxy settings,
Open WebUI uses the following environment variables:

#### `http_proxy`

- Type: `str`
- Description: Sets the URL for the HTTP proxy.

#### `https_proxy`

- Type: `str`
- Description: Sets the URL for the HTTPS proxy.

#### `no_proxy`

- Type: `str`
- Description: Lists domain extensions (or IP addresses) for which the proxy should not be used,
separated by commas. For example, setting no_proxy to '.mit.edu' ensures that the proxy is
bypassed when accessing documents from MIT.

### Install Required Python Packages

Open WebUI provides environment variables to customize the pip installation process. Below are the environment variables used by Open WebUI for adjusting package installation behavior:

#### `PIP_OPTIONS`

- Type: `str`
- Description: Specifies additional command-line options that pip should use when installing packages. For example, you can include flags such as `--upgrade`, `--user`, or `--no-cache-dir` to control the installation process.

#### `PIP_PACKAGE_INDEX_OPTIONS`

- Type: `str`
- Description: Defines custom package index behavior for pip. This can include specifying additional or alternate index URLs (e.g., `--extra-index-url`), authentication credentials, or other parameters to manage how packages are retrieved from different locations.
