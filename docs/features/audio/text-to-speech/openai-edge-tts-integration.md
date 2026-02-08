!!! warning

This tutorial is a community contribution and is not supported by the Open WebUI team. It serves only as a demonstration on how to customize Open WebUI for your specific use case. Want to contribute? Check out the contributing tutorial.

# Integrating `openai-edge-tts` 🗣️ with Open WebUI

## What is `openai-edge-tts`?

[OpenAI Edge TTS](https://github.com/travisvn/openai-edge-tts) is a text-to-speech API that mimics the OpenAI API endpoint, allowing for a direct substitute in scenarios where you can define the endpoint URL, like with Open WebUI.

It uses the [edge-tts](https://github.com/rany2/edge-tts) package, which leverages the Edge browser's free "Read Aloud" feature to emulate a request to Microsoft / Azure in order to receive very high quality text-to-speech for free.

[Sample the voices](https://tts.travisvn.com)

<!-- markdownlint-disable-next-line MD033 -->

## Requirements

- Docker installed on your system
- Open WebUI running

## ⚡️ Quick start

The simplest way to get started without having to configure anything is to run the command below

```bash
docker run -d -p 5050:5050 travisvn/openai-edge-tts:latest
```

This will run the service at port 5050 with all the default configs

## Setting up Open WebUI to use `openai-edge-tts`

- Open the Admin Panel and go to `Settings` -> `Audio`
- Set your TTS Settings to match the screenshot below
- *Note: you can specify the TTS Voice here*

![Screenshot of Open WebUI Admin Settings for Audio adding the correct endpoints for this project](https://utfs.io/f/MMMHiQ1TQaBobmOhsMkrO6Tl2kxX39dbuFiQ8cAoNzysIt7f)

!!! info

The default API key is the string `your_api_key_here`. You do not have to change that value if you do not need the added security.

**And that's it! You can end here**

## Please ⭐️ star the repo on GitHub if you find [OpenAI Edge TTS](https://github.com/travisvn/openai-edge-tts) useful

<!-- markdownlint-disable-next-line MD033 -->

<!-- markdownlint-disable-next-line MD033 -->

## 🐳 Quick Config for Docker

You can configure the environment variables in the command used to run the project

```bash
docker run -d -p 5050:5050 /
  -e API_KEY=your_api_key_here /
  -e PORT=5050 /
  -e DEFAULT_VOICE=en-US-AvaNeural /
  -e DEFAULT_RESPONSE_FORMAT=mp3 /
  -e DEFAULT_SPEED=1.0 /
  -e DEFAULT_LANGUAGE=en-US /
  -e REQUIRE_API_KEY=True /
  -e REMOVE_FILTER=False /
  -e EXPAND_API=True /
  travisvn/openai-edge-tts:latest
```

!!! note

The markdown text is now put through a filter for enhanced readability and support.

You can disable this by setting the environment variable `REMOVE_FILTER=True`.

## Additional Resources

For more information on `openai-edge-tts`, you can visit the [GitHub repo](https://github.com/travisvn/openai-edge-tts)

For direct support, you can visit the [Voice AI & TTS Discord](https://tts.travisvn.com/discord)

## 🎙️ Voice Samples

[Play voice samples and see all available Edge TTS voices](https://tts.travisvn.com/)

## Troubleshooting

### Connection Issues

#### "localhost" Not Working from Docker

If Open WebUI runs in Docker and can't reach the TTS service at `localhost:5050`:

**Solutions:**
- Use `host.docker.internal:5050` instead of `localhost:5050` (Docker Desktop on Windows/Mac)
- On Linux, use the host's IP address, or add `--network host` to your Docker run command
- If both services are in Docker Compose, use the container name: `http://openai-edge-tts:5050/v1`

**Example Docker Compose for both services on the same network:**

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      - AUDIO_TTS_ENGINE=openai
      - AUDIO_TTS_OPENAI_API_BASE_URL=http://openai-edge-tts:5050/v1
      - AUDIO_TTS_OPENAI_API_KEY=your_api_key_here
    networks:
      - webui-network

  openai-edge-tts:
    image: travisvn/openai-edge-tts:latest
    ports:
      - "5050:5050"
    environment:
      - API_KEY=your_api_key_here
    networks:
      - webui-network

networks:
  webui-network:
    driver: bridge
```

#### Testing the TTS Service

Verify the TTS service is working independently:

```bash
curl -X POST http://localhost:5050/v1/audio/speech /
  -H "Content-Type: application/json" /
  -H "Authorization: Bearer your_api_key_here" /
  -d '' /
  --output test.mp3
```

If this works but Open WebUI still can't connect, the issue is network-related between containers.

### No Audio Output in Open WebUI

1. Check that the API Base URL ends with `/v1`
2. Verify the API key matches between both services (or remove the requirement)
3. Check Open WebUI container logs: `docker logs open-webui`
4. Check openai-edge-tts logs: `docker logs openai-edge-tts` (or your container name)

For more troubleshooting tips, see the [Audio Troubleshooting Guide](../../../troubleshooting/audio.md).
