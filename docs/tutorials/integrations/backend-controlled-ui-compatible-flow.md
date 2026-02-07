!!! warning

This tutorial is a community contribution and is not supported by the Open WebUI team. It serves only as a demonstration on how to customize Open WebUI for your specific use case. Want to contribute? Check out the [contributing tutorial](tutorials/tips/contributing-tutorial.md).

---

# Backend-Controlled, UI-Compatible API Flow

This tutorial demonstrates how to implement server-side orchestration of Open WebUI conversations while ensuring that assistant replies appear properly in the frontend UI. This approach requires zero frontend involvement and allows complete backend control over the chat flow.
This tutorial has been verified to work with Open WebUI version v0.6.15. Future versions may introduce changes in behavior or API structure.

## Prerequisites

Before following this tutorial, ensure you have:

- A running Open WebUI instance
- Valid API authentication token
- Access to the Open WebUI backend APIs
- Basic understanding of REST APIs and JSON
- Command-line tools: `curl`, `jq` (optional for JSON parsing)

## Overview

This tutorial describes a comprehensive 7-step process that enables server-side orchestration of Open WebUI conversations while ensuring that assistant replies appear properly in the frontend UI.

### Process Flow

The essential steps are:

1. **Create a new chat with a user message** - Initialize the conversation with the user's input
2. **Enrich the chat response with an assistant message** - Add assistant message to the response object in memory
3. **Update chat with assistant message** - Send the enriched chat state to the server
4. **Trigger the assistant completion** - Generate the actual AI response (with optional knowledge integration)
5. **Wait for response completion** - Monitor the assistant response until fully generated
6. **Complete the assistant message** - Mark the response as completed
7. **Fetch and process the final chat** - Retrieve and parse the completed conversation

This enables server-side orchestration while still making replies show up in the frontend UI exactly as if they were generated through normal user interaction.

## Implementation Guide

### Critical Step: Enrich Chat Response with Assistant Message

The assistant message needs to be added to the chat response object in memory as a critical prerequisite before triggering the completion. This step is essential because the Open WebUI frontend expects assistant messages to exist in a specific structure.

The assistant message must appear in both locations:

- `chat.messages[]` - The main message array
- `chat.history.messages[<assistantId>]` - The indexed message history

**Expected structure of the assistant message:**

```json

```

Without this enrichment, the assistant's response will not appear in the frontend interface, even if the completion is successful.

## Step-by-Step Implementation

### Step 1: Create Chat with User Message

This starts the chat and returns a `chatId` that will be used in subsequent requests.

```bash
curl -X POST https://<host>/api/v1/chats/new /
  -H "Authorization: Bearer <token>" /
  -H "Content-Type: application/json" /
  -d '
    }
  }'
```

### Step 2: Enrich Chat Response with Assistant Message

Add the assistant message to the chat response object in memory. Note that this can be combined with Step 1 by including the assistant message in the initial chat creation:

```java
// Example implementation in Java
public void enrichChatWithAssistantMessage(OWUIChatResponse chatResponse, String model) 
```

!!! note

**Note:** This step can be performed in memory on the response object, or combined with Step 1 by including both user and empty assistant messages in the initial chat creation.

### Step 3: Update Chat with Assistant Message

Send the enriched chat state containing both user and assistant messages to the server:

```bash
curl -X POST https://<host>/api/v1/chats/<chatId> /
  -H "Authorization: Bearer <token>" /
  -H "Content-Type: application/json" /
  -d '
    }
  }'
```

### Step 4: Trigger Assistant Completion

Generate the actual AI response using the completion endpoint:

```bash
curl -X POST https://<host>/api/chat/completions /
  -H "Authorization: Bearer <token>" /
  -H "Content-Type: application/json" /
  -d ',
    "session_id": "session-id"
  }'
```

#### Step 4.1: Trigger Assistant Completion with Knowledge Integration (RAG)

For advanced use cases involving knowledge bases or document collections, include knowledge files in the completion request:

```bash
curl -X POST https://<host>/api/chat/completions /
  -H "Authorization: Bearer <token>" /
  -H "Content-Type: application/json" /
  -d ',
    "session_id": "session-id"
  }'
```

### Step 5: Wait for Assistant Response Completion

Assistant responses can be handled in two ways depending on your implementation needs:

#### Option A: Stream Processing (Recommended)

If using `stream: true` in the completion request, you can process the streamed response in real-time and wait for the stream to complete. This is the approach used by the OpenWebUI web interface and provides immediate feedback.

#### Option B: Polling Approach

For implementations that cannot handle streaming, poll the chat endpoint until the response is ready. Use a retry mechanism with exponential backoff:

```java
// Example implementation in Java
@Retryable(
    retryFor = AssistantResponseNotReadyException.class,
    maxAttemptsExpression = "#",
    backoff = @Backoff(delayExpression = "#")
)
public String getAssistantResponseWhenReady(String chatId, ChatCompletedRequest chatCompletedRequest) 
```

For manual polling, you can use:

```bash

# Poll every few seconds until assistant content is populated

while true; do
  response=$(curl -s -X GET https://<host>/api/v1/chats/<chatId> /
    -H "Authorization: Bearer <token>")

  # Check if assistant message has content (response is ready)
  if echo "$response" | jq '.chat.messages[] | select(.role=="assistant" and .id=="assistant-msg-id") | .content' | grep -v '""' > /dev/null; then
    echo "Assistant response is ready!"
    break
  fi

  echo "Waiting for assistant response..."
  sleep 2
done
```

### Step 6: Complete Assistant Message

Once the assistant response is ready, mark it as completed:

```bash
curl -X POST https://<host>/api/chat/completed /
  -H "Authorization: Bearer <token>" /
  -H "Content-Type: application/json" /
  -d ''
```

### Step 7: Fetch Final Chat

Retrieve the completed conversation:

```bash
curl -X GET https://<host>/api/v1/chats/<chatId> /
  -H "Authorization: Bearer <token>"
```

## Additional API Endpoints

### Fetch Knowledge Collection

Retrieve knowledge base information for RAG integration:

```bash
curl -X GET https://<host>/api/v1/knowledge/<knowledge-id> /
  -H "Authorization: Bearer <token>"
```

### Fetch Model Information

Get details about a specific model:

```bash
curl -X GET https://<host>/api/v1/models/model?id=<model-name> /
  -H "Authorization: Bearer <token>"
```

### Send Additional Messages to Chat

For multi-turn conversations, you can send additional messages to an existing chat:

```bash
curl -X POST https://<host>/api/v1/chats/<chatId> /
  -H "Authorization: Bearer <token>" /
  -H "Content-Type: application/json" /
  -d '
    }
  }'
```

## Response Processing

### Parsing Assistant Responses

Assistant responses may be wrapped in markdown code blocks. Here's how to clean them:

```bash

# Example raw response from assistant

raw_response='```json

```'

# Clean the response (remove markdown wrappers)

cleaned_response=$(echo "$raw_response" | sed 's/^```json//' | sed 's/```$//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

echo "$cleaned_response" | jq '.'
```

This cleaning process handles:

- Removal of ````json` prefix
- Removal of ```` suffix
- Trimming whitespace
- JSON validation

## API Reference

### DTO Structures

#### Chat DTO (Complete Structure)

```json
,
  "currentId": "assistant-msg-id"
}
```

#### ChatCompletionsRequest DTO

```json
,
  "session_id": "session-uuid-67890",
  "filter_ids": [],
  "files": [
    
  ]
}
```

#### ChatCompletedRequest DTO

```json

```

#### ChatCompletionMessage DTO

```json

```

#### History DTO

```json

```

#### Message DTO (Complete Structure)

```json

```

```json

```

### Response Examples

#### Create Chat Response

```json
,
    "currentId": "user-msg-id"
  }
}
```

#### Final Chat Response (After Completion)

```json
,
  "currentId": "assistant-msg-id"
}
```

#### Tag DTO

```json

```

#### OWUIKnowledge DTO (Knowledge Collection)

```json

```

#### Knowledge Collection Response

```json

```

#### Model Information Response

```json

```

### Field Reference Guide

#### Required vs Optional Fields

**Chat Creation - Required Fields:**

- `title` - Chat title (string)
- `models` - Array of model names (string[])
- `messages` - Initial message array

**Chat Creation - Optional Fields:**

- `files` - Knowledge files for RAG (defaults to empty array)
- `tags` - Chat tags (defaults to empty array)
- `params` - Model parameters (defaults to empty object)

**Message Structure - User Message:**

- **Required:** `id`, `role`, `content`, `timestamp`, `models`
- **Optional:** `parentId` (for threading)

**Message Structure - Assistant Message:**

- **Required:** `id`, `role`, `content`, `parentId`, `modelName`, `modelIdx`, `timestamp`
- **Optional:** Additional metadata fields

**ChatCompletionsRequest - Required Fields:**

- `chat_id` - Target chat ID
- `id` - Assistant message ID
- `messages` - Array of ChatCompletionMessage
- `model` - Model identifier
- `session_id` - Session identifier

**ChatCompletionsRequest - Optional Fields:**

- `stream` - Enable streaming (defaults to false)
- `background_tasks` - Control automatic tasks
- `features` - Enable/disable features
- `variables` - Template variables
- `filter_ids` - Pipeline filters
- `files` - Knowledge collections for RAG

#### Field Constraints

**Timestamps:**

- Format: Unix timestamp in milliseconds
- Example: `1720000000000` (July 4, 2024, 00:00:00 UTC)

**UUIDs:**

- All ID fields should use valid UUID format
- Example: `550e8400-e29b-41d4-a716-446655440000`

**Model Names:**

- Must match available models in your Open WebUI instance
- Common examples: `gpt-4o`, `gpt-3.5-turbo`, `claude-3-sonnet`

**Session IDs:**

- Can be any unique string identifier
- Recommendation: Use UUID format for consistency

**Knowledge File Status:**

- Valid values: `"processed"`, `"processing"`, `"error"`
- Only use `"processed"` files for completions

## Important Notes

- This workflow is compatible with Open WebUI + backend orchestration scenarios
- **Critical:** The assistant message enrichment must be done in memory on the response object, not via API call
- **Alternative Approach:** You can include both user and assistant messages in the initial chat creation (Step 1) instead of doing Step 2 separately
- No frontend code changes are required for this approach
- The `stream: true` parameter allows for real-time response streaming if needed
- **Response Monitoring:** Use streaming for real-time processing or polling for simpler implementations that cannot handle streams
- Background tasks like title generation can be controlled via the `background_tasks` object
- Session IDs help maintain conversation context across requests
- **Knowledge Integration:** Use the `files` array to include knowledge collections for RAG capabilities
- **Response Parsing:** Handle JSON responses that may be wrapped in markdown code blocks
- **Error Handling:** Implement proper retry mechanisms for network timeouts and server errors

## Summary

Use the Open WebUI backend APIs to:

1. **Start a chat** - Create the initial conversation with user input
2. **Enrich with assistant message** - Add assistant placeholder to the response object in memory (can be combined with Step 1)
3. **Update chat state** - Send the enriched chat to the server
4. **Trigger a reply** - Generate the AI response (with optional knowledge integration)
5. **Monitor completion** - Wait for the assistant response using streaming or polling
6. **Complete the message** - Mark the response as completed
7. **Fetch the final chat** - Retrieve and parse the completed conversation

**Enhanced Capabilities:**

- **RAG Integration** - Include knowledge collections for context-aware responses
- **Asynchronous Processing** - Handle long-running AI operations with streaming or polling
- **Response Parsing** - Clean and validate JSON responses from the assistant
- **Session Management** - Maintain conversation context across requests

This enables backend-controlled workflows that still appear properly in the Web UI frontend chat interface, providing seamless integration between programmatic control and user experience.

The key advantage of this approach is that it maintains full compatibility with the Open WebUI frontend while allowing complete backend orchestration of the conversation flow, including advanced features like knowledge integration and asynchronous response handling.

## Testing

You can test your implementation by following the step-by-step CURL examples provided above. Make sure to replace placeholder values with your actual:

- Host URL
- Authentication token
- Chat IDs
- Message IDs
- Model names

!!! tip

Start with a simple user message and gradually add complexity like knowledge integration and advanced features once the basic flow is working.
