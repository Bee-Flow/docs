# Voice

!!! warning "Pro tier feature"
    Requires a Pro or higher license key.

Bee Flow supports two voice modes:

## Push-to-talk

Click the microphone in the chat composer, hold it, speak, release. Your speech is transcribed and submitted as the next message.

## Voice call

Click the **Voice call** button in the chat header. The assistant streams a continuous conversation — you talk, it talks back, with low-latency interruption support.

![Voice call UI](../img/screenshots/voice-call.png)

## Models

The voice pipeline routes through your configured provider:

- **OpenAI Realtime** — recommended for English / Spanish / French / German.
- **Anthropic + ElevenLabs** — text-only models bridged via TTS/STT.
- **Local Whisper** — self-hosted STT for privacy-sensitive deployments.

## Privacy

The Privacy Shield runs on the transcribed text before it reaches the model — exactly the same as text chat. Voice inputs are not retained beyond session lifetime unless you explicitly enable conversation history.
