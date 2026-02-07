This guide provides essential information on how to interact with the API endpoints effectively to achieve seamless integration and automation using our models. Please note that this is an experimental setup and may undergo future updates for enhancement.

## Authentication

To ensure secure access to the API, authentication is required 🛡️. You can authenticate your API requests using the Bearer Token mechanism. Obtain your API key from **Settings > Account** in the Open WebUI, or alternatively, use a JWT (JSON Web Token) for authentication.

## Swagger Documentation Links

important

Make sure to set the `ENV` environment variable to `dev` in order to access the Swagger documentation for any of these services. Without this configuration, the documentation will not be available.

Access detailed API documentation for different services provided by Open WebUI:

| Application | Documentation Path      |
|-------------|-------------------------|
| Main        | `/docs`                 |

## Notable API Endpoints

### 📜 Retrieve All Models

- **Endpoint**: `GET /api/models`
- **Description**: Fetches all models created or added via Open WebUI.
- **Example**:

  ```bash
  curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:3000/api/models
  ```

### 💬 Chat Completions

- **Endpoint**: `POST /api/chat/completions`
- **Description**: Serves as an OpenAI API compatible chat completion endpoint for models on Open WebUI including Ollama models, OpenAI models, and Open WebUI Function models.

- **Curl Example**:

  ```bash
  curl -X POST http://localhost:3000/api/chat/completions /
  -H "Authorization: Bearer YOUR_API_KEY" /
  -H "Content-Type: application/json" /
  -d ''
  ```

- **Python Example**:

  ```python

  def chat_with_model(token):
      url = 'http://localhost:3000/api/chat/completions'
      headers = 
      data = 
      response = requests.post(url, headers=headers, json=data)
      return response.json()
  ```

### 🦙 Ollama API Proxy Support

If you want to interact directly with Ollama models—including for embedding generation or raw prompt streaming—Open WebUI offers a transparent passthrough to the native Ollama API via a proxy route.

- **Base URL**: `/ollama/<api>`
- **Reference**: [Ollama API Documentation](https://github.com/ollama/ollama/blob/main/docs/api.md)

#### 🔁 Generate Completion (Streaming)

```bash
curl http://localhost:3000/ollama/api/generate /
  -H "Authorization: Bearer YOUR_API_KEY" /
  -H "Content-Type: application/json" /
  -d ''
```

#### 📦 List Available Models

```bash
curl http://localhost:3000/ollama/api/tags /
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 🧠 Generate Embeddings

```bash
curl -X POST http://localhost:3000/ollama/api/embed /
  -H "Authorization: Bearer YOUR_API_KEY" /
  -H "Content-Type: application/json" /
  -d ''
```

!!! info
When using the Ollama Proxy endpoints, you **must** include the `Content-Type: application/json` header for POST requests, or the API may fail to parse the body. Authorization headers are also required if your instance is secured.

This is ideal for building search indexes, retrieval systems, or custom pipelines using Ollama models behind the Open WebUI.

### 🧩 Retrieval Augmented Generation (RAG)

The Retrieval Augmented Generation (RAG) feature allows you to enhance responses by incorporating data from external sources. Below, you will find the methods for managing files and knowledge collections via the API, and how to use them in chat completions effectively.

#### Uploading Files

To utilize external data in RAG responses, you first need to upload the files. The content of the uploaded file is automatically extracted and stored in a vector database.

- **Endpoint**: `POST /api/v1/files/`
- **Query Parameters**:
  - `process` (boolean, default: `true`): Whether to extract content and compute embeddings
  - `process_in_background` (boolean, default: `true`): Whether to process asynchronously
- **Curl Example**:

  ```bash
  curl -X POST -H "Authorization: Bearer YOUR_API_KEY" -H "Accept: application/json" /
  -F "file=@/path/to/your/file" http://localhost:3000/api/v1/files/
  ```

- **Python Example**:

  ```python

  def upload_file(token, file_path):
      url = 'http://localhost:3000/api/v1/files/'
      headers = 
      files = 
      response = requests.post(url, headers=headers, files=files)
      return response.json()
  ```

!!! warning Async Processing and Race Conditions

By default, file uploads are processed **asynchronously**. The upload endpoint returns immediately with a file ID, but content extraction and embedding computation continue in the background. 

If you attempt to add the file to a knowledge base before processing completes, you will receive a `400` error:

```
The content provided is empty. Please ensure that there is text or data present before proceeding.
```

**You must wait for file processing to complete before adding files to knowledge bases.** See the [Checking File Processing Status](#checking-file-processing-status.md) section below.

#### Checking File Processing Status

Before adding a file to a knowledge base, verify that processing has completed using the status endpoint.

- **Endpoint**: `GET /api/v1/files//process/status`
- **Query Parameters**:
  - `stream` (boolean, default: `false`): If `true`, returns a Server-Sent Events (SSE) stream

**Status Values:**
| Status | Description |
|--------|-------------|
| `pending` | File is still being processed |
| `completed` | Processing finished successfully |
| `failed` | Processing failed (check `error` field for details) |

- **Python Example** (Polling):

  ```python

  def wait_for_file_processing(token, file_id, timeout=300, poll_interval=2):
      """
      Wait for a file to finish processing.
      
      Returns:
          dict: Final status with 'status' key ('completed' or 'failed')
      
      Raises:
          TimeoutError: If processing doesn't complete within timeout
      """
      url = f'http://localhost:3000/api/v1/files//process/status'
      headers = 
      
      start_time = time.time()
`      while time.time() - start_time &lt; timeout:`
          response = requests.get(url, headers=headers)
          result = response.json()
          status = result.get('status')
          
          if status == 'completed':
              return result
          elif status == 'failed':
              raise Exception(f"File processing failed: ")
          
          time.sleep(poll_interval)
      
      raise TimeoutError(f"File processing did not complete within  seconds")
  ```

- **Python Example** (SSE Streaming):

  ```python

  def wait_for_file_processing_stream(token, file_id):
      """
      Wait for file processing using Server-Sent Events stream.
      More efficient than polling for long-running operations.
      """
      url = f'http://localhost:3000/api/v1/files//process/status?stream=true'
      headers = 
      
      with requests.get(url, headers=headers, stream=True) as response:
          for line in response.iter_lines():
              if line:
                  line = line.decode('utf-8')
                  if line.startswith('data: '):
                      data = json.loads(line[6:])
                      status = data.get('status')
                      
                      if status == 'completed':
                          return data
                      elif status == 'failed':
                          raise Exception(f"File processing failed: ")
      
      raise Exception("Stream ended unexpectedly")
  ```

#### Adding Files to Knowledge Collections

After uploading, you can group files into a knowledge collection or reference them individually in chats.

important
**Always wait for file processing to complete before adding files to a knowledge base.** Files that are still processing will have empty content, causing a `400` error. Use the status endpoint described above to verify the file status is `completed`.

- **Endpoint**: `POST /api/v1/knowledge//file/add`
- **Curl Example**:

  ```bash
  curl -X POST http://localhost:3000/api/v1/knowledge//file/add /
  -H "Authorization: Bearer YOUR_API_KEY" /
  -H "Content-Type: application/json" /
  -d ''
  ```

- **Python Example**:

  ```python

  def add_file_to_knowledge(token, knowledge_id, file_id):
      url = f'http://localhost:3000/api/v1/knowledge//file/add'
      headers = 
      data = 
      response = requests.post(url, headers=headers, json=data)
      return response.json()
  ```

#### Complete Workflow Example

Here's a complete example that uploads a file, waits for processing, and adds it to a knowledge base:

```python

WEBUI_URL = 'http://localhost:3000'
TOKEN = 'your-api-key-here'

def upload_and_add_to_knowledge(file_path, knowledge_id, timeout=300):
    """
    Upload a file and add it to a knowledge base.
    Properly waits for processing to complete before adding.
    """
    headers = 
    
    # Step 1: Upload the file
    with open(file_path, 'rb') as f:
        response = requests.post(
            f'/api/v1/files/',
            headers=headers,
            files=
        )
    
    if response.status_code != 200:
        raise Exception(f"Upload failed: ")
    
    file_data = response.json()
    file_id = file_data['id']
    print(f"File uploaded with ID: ")
    
    # Step 2: Wait for processing to complete
    print("Waiting for file processing...")
    start_time = time.time()
    
`    while time.time() - start_time &lt; timeout:`
        status_response = requests.get(
            f'/api/v1/files//process/status',
            headers=headers
        )
        status_data = status_response.json()
        status = status_data.get('status')
        
        if status == 'completed':
            print("File processing completed!")
            break
        elif status == 'failed':
            raise Exception(f"Processing failed: ")
        
        time.sleep(2)  # Poll every 2 seconds
    else:
        raise TimeoutError("File processing timed out")
    
    # Step 3: Add to knowledge base
    add_response = requests.post(
        f'/api/v1/knowledge//file/add',
        headers=,
        json=
    )
    
    if add_response.status_code != 200:
        raise Exception(f"Failed to add to knowledge: ")
    
    print(f"File successfully added to knowledge base!")
    return add_response.json()

# Usage

result = upload_and_add_to_knowledge('/path/to/document.pdf', 'your-knowledge-id')
```

#### Using Files and Collections in Chat Completions

You can reference both individual files or entire collections in your RAG queries for enriched responses.

##### Using an Individual File in Chat Completions

This method is beneficial when you want to focus the chat model's response on the content of a specific file.

- **Endpoint**: `POST /api/chat/completions`
- **Curl Example**:

  ```bash
  curl -X POST http://localhost:3000/api/chat/completions /
  -H "Authorization: Bearer YOUR_API_KEY" /
  -H "Content-Type: application/json" /
  -d ''
  ```

- **Python Example**:

  ```python

  def chat_with_file(token, model, query, file_id):
      url = 'http://localhost:3000/api/chat/completions'
      headers = 
      payload = 
      response = requests.post(url, headers=headers, json=payload)
      return response.json()
  ```

##### Using a Knowledge Collection in Chat Completions

Leverage a knowledge collection to enhance the response when the inquiry may benefit from a broader context or multiple documents.

- **Endpoint**: `POST /api/chat/completions`
- **Curl Example**:

  ```bash
  curl -X POST http://localhost:3000/api/chat/completions /
  -H "Authorization: Bearer YOUR_API_KEY" /
  -H "Content-Type: application/json" /
  -d ''
  ```

- **Python Example**:

  ```python

  def chat_with_collection(token, model, query, collection_id):
      url = 'http://localhost:3000/api/chat/completions'
      headers = 
      payload = 
      response = requests.post(url, headers=headers, json=payload)
      return response.json()
  ```

These methods enable effective utilization of external knowledge via uploaded files and curated knowledge collections, enhancing chat applications' capabilities using the Open WebUI API. Whether using files individually or within collections, you can customize the integration based on your specific needs.

## Advantages of Using Open WebUI as a Unified LLM Provider

Open WebUI offers a myriad of benefits, making it an essential tool for developers and businesses alike:

- **Unified Interface**: Simplify your interactions with different LLMs through a single, integrated platform.
- **Ease of Implementation**: Quick start integration with comprehensive documentation and community support.

By following these guidelines, you can swiftly integrate and begin utilizing the Open WebUI API. Should you encounter any issues or have questions, feel free to reach out through our Discord Community or consult the FAQs. Happy coding! 🌟
