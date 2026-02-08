!!! warning

This tutorial is a community contribution and is not supported by the Open WebUI team. It serves only as a demonstration on how to customize Open WebUI for your specific use case. Want to contribute? Check out the contributing tutorial.

# 🪄 Special Arguments

When developping your own `Tools`, `Functions` (`Filters`, `Pipes` or `Actions`), `Pipelines` etc, you can use special arguments explore the full spectrum of what Open-WebUI has to offer.

This page aims to detail the type and structure of each special argument as well as provide an example.

### `body`

A `dict` usually destined to go almost directly to the model. Although it is not strictly a special argument, it is included here for easier reference and because it contains itself some special arguments.

Example

```json

,
    ,
  ],
  "features": ,
  "stream_options": ,
  "metadata": "[The exact same dict as __metadata__]",
  "files": "[The exact same list as __files__]"
}

```

### `__user__`

A `dict` with user information.

!!! note "that if the `UserValves` class is defined, its instance has to be accessed via `__user__["valves"]`. Otherwise, the `valves` keyvalue is missing entirely from `__user__`."

Example

```json

```

### `__metadata__`

A `dict` with wide ranging information about the chat, model, files, etc.

Example

```json
,
  "model": "[The exact same dict as __model__]",
  "direct": false,
  "function_calling": "native",
  "type": "user_response",
  "interface": "open-webui"
}

```

### `__model__`

A `dict` with information about the model.

Example

```json
,
  "preset": true,
  "actions": [],
  "tags": [
      ,
      
  ]
}

```

### `__messages__`

A `list` of the previous messages.

See the `body["messages"]` value above.

### `__chat_id__`

The `str` of the `chat_id`, representing the unique identifier of the current chat/conversation.

This parameter is reliably passed for all function invocations that originate from a chat context, including:
- Regular user messages
- Internal task calls (title generation, query generation, tag generation, etc.)

This allows stateful functions/pipes/manifolds to maintain per-chat state without fragmentation.

See also `__metadata__["chat_id"]` for accessing the same value via the metadata dict.

### `__session_id__`

The `str` of the `session_id`.

See the `__metadata__["session_id"]` value above.

### `__message_id__`

The `str` of the `message_id`.

See the `__metadata__["message_id"]` value above.

### `__event_emitter__`

A `Callable` used to display event information to the user.

### `__event_call__`

A `Callable` used for `Actions`.

### `__files__`

A `list` of files sent via the chat. Note that images are not considered files and are sent directly to the model as part of the `body["messages"]` list.

The actual binary of the file is not part of the arguments for performance reason, but the file remain nonetheless accessible by its path if needed. For example using `docker` the python syntax for the path could be:

```python
from pathlib import Path

the_file = Path(f"/app/backend/data/uploads/_")
assert the_file.exists()
```

!!! note "that the same files dict can also be accessed via `__metadata__["files"]` (and its value is `[]` if no files are sent) or via `body["files"]` (but the `files` key is missing entirely from `body` if no files are sent)."

Example

```json

[
  ,
    "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "url": "/api/v1/files/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "name": "Napoleon - Wikipedia.pdf",
    "collection_name": "file-96xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    "status": "uploaded",
    "size": 10486578,
    "error": "",
    "itemId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    # itemId is not the same as file["id"]
  }
]

```

### `__request__`

An instance of `fastapi.Request`. You can read more in the [migration page](../migration/index.md) or in [fastapi's documentation](https://fastapi.tiangolo.com/reference/request/).

### `__task__`

A `str` for the type of task. Its value is just a shorthand for `__metadata__["task"]` if present, otherwise `None`.

Possible values

```json

[
    "title_generation",
    "tags_generation",
    "emoji_generation",
    "query_generation",
    "image_prompt_generation",
    "autocomplete_generation",
    "function_calling",
    "moa_response_generation"
]
```

### `__task_body__`

A `dict` containing the `body` needed to accomplish a given `__task__`. Its value is just a shorthand for `__metadata__["task_body"]` if present, otherwise `None`.

Its structure is the same as `body` above, with modifications like using the appropriate model and system message etc.

### `__tools__`

A `list` of `ToolUserModel` instances.

For details the attributes of `ToolUserModel` instances, the code can be found in [tools.py](https://github.com/open-webui/open-webui/blob/main/backend/open_webui/models/tools.py).
