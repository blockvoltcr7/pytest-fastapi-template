# API Endpoints and Payloads - AI LipSync Baby Workflow

## 1. ElevenLabs Text-to-Speech API

**Endpoint:** `POST https://api.elevenlabs.io/v1/text-to-speech/8JVbfL6oEdmuxKn5DK2C`

**Headers:**
```json
{
  "Content-Type": "application/json",
  "xi-api-key": "SECRET"
}
```

**Payload:**
```json
{
  "text": "RESPONSE"
}
```

**Purpose:** Converts the generated podcast script into high-quality speech audio using a specific voice model.


---

## 3. OpenAI GPT-4.1 - Image Prompt Generation



**Node Type:** `@n8n/n8n-nodes-langchain.openAi`
**Model:** `gpt-4.1`

**Messages:**
```json
{
  "content": "Generate a high-resolution image of a very cute, chubby, {{ $json['Baby Hairstyle '] }} hair, {{ $json['Baby Ethnicity '] }} baby wearing large over-ear headphones and speaking into a professional podcast microphone. The baby has a focused yet adorable expression. The background should resemble a podcast studio setting with a dark, rich curtain and warm, soft lighting that highlights the baby's chubby cheeks and innocent face.\n\nEnsure the entire description is output as a single JSON object called Prompt"
}
```

**Options:**
- `jsonOutput`: true

**Purpose:** Creates a detailed prompt for generating the baby podcaster image.

---

## 4. OpenAI Image Generation

import base64
from openai import OpenAI
client = OpenAI()

img = client.images.generate(
    model="gpt-image-1",
    prompt="Generate a high-resolution image of a very cute, chubby, {{ $json['Baby Hairstyle '] }} hair, {{ $json['Baby Ethnicity '] }} baby wearing large over-ear headphones and speaking into a professional podcast microphone. The baby has a focused yet adorable expression. The background should resemble a podcast studio setting with a dark, rich curtain and warm, soft lighting that highlights the baby's chubby cheeks and innocent face.\n\nEnsure the entire description is output as a single JSON object called Prompt",
    n=1,
    size="1024x1536"
)

image_bytes = base64.b64decode(img.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)

**Purpose:** Generates the baby podcaster image based on the AI-created prompt.

---

## 5. Hedra - Create Image Asset

**Endpoint:** `POST https://api.hedra.com/web-app/public/assets`

**Authentication:** Custom HTTP Auth (API Key)

**Payload:**
```json
{
  "name": "baby-podcaster-image",
  "type": "image"
}
```

**Purpose:** Creates an image asset container in Hedra platform for the baby image.

---

## 6. Hedra - Create Audio Asset

**Endpoint:** `POST https://api.hedra.com/web-app/public/assets`

**Authentication:** Custom HTTP Auth (API Key)

**Payload:**
```json
{
  "name": "baby-podcaster-audio",
  "type": "audio"
}
```

**Purpose:** Creates an audio asset container in Hedra platform for the podcast audio.

---

## 7. Hedra - Upload Audio File

**Endpoint:** `POST https://api.hedra.com/web-app/public/assets/{{ $json.id }}/upload`

**Headers:**
```json
{
  "X-Api-Key": "SECRET",
  "Content-Type": "multipart/form-data"
}
```

**Payload:**
- Form data with binary file upload
- Field name: `file`
- Input data field: `data`

**Purpose:** Uploads the generated audio file to the Hedra audio asset.

---

## 8. Hedra - Upload Image File

**Endpoint:** `POST https://api.hedra.com/web-app/public/assets/{{ $json.id }}/upload`

**Authentication:** {
  "headers": {
    "X-Api-Key": "SECRET",
    "Content-Type": "application/json"
  }
}

**Payload:**
- Form data with binary file upload (multipart/form-data)
- Field name: `file`
- Input data field: `data`

**Purpose:** Uploads the generated baby image to the Hedra image asset.

---

## 9. Hedra - Create Lip-Sync Video

**Endpoint:** `POST https://api.hedra.com/web-app/public/generations`

**Authentication:** {
  "headers": {
    "X-Api-Key": "SECRET",
    "Content-Type": "application/json"
  }
}
**Payload:**
```json
{
  "type": "video",
  "ai_model_id": "d1dd37a3-e39a-4854-a298-6510289f9cf2",
  "start_keyframe_id": "{{ $json.image_asset_id }}",
  "audio_id": "{{ $json.audio_asset_id }}",
  "generated_video_inputs": {
    "text_prompt": "A baby podcast host seated in front of a microphone, speaking with calm intensity and natural focus. Subtle facial expressions, minimal head movement, steady eye contact with the camera. Studio lighting with a professional podcast setup in the background.",
    "resolution": "720p",
    "aspect_ratio": "9:16",
    "duration_ms": 5000
  }
}
```

**Purpose:** Initiates the AI lip-sync video generation combining the baby image with the podcast audio.

---

## 10. Hedra - Get Video Status

**Endpoint:** `GET https://api.hedra.com/web-app/public/assets?type=video&ids={{ $json.asset_id }}`

**Authentication:** Custom HTTP Auth (API Key)

**Purpose:** Retrieves the generated video status and download URL after processing.

---

## 11. Hedra - Download Video

**Endpoint:** `GET {{ $json.asset.url }}`

**Response Format:** File download

**Purpose:** Downloads the completed lip-sync video from Hedra.

---

## 12. Supabase Storage - Upload Video

**Node Type:** `n8n-nodes-base.httpRequest`  
**Operation:** `POST`

**Parameters:**
```json
{
  "url": "https://{{ $credentials.supabaseUrl }}/storage/v1/object/videos/{{ $json.id }}.mp4",
  "headers": {
    "apikey": "{{ $credentials.supabaseApiKey }}",
    "Authorization": "Bearer {{ $credentials.supabaseServiceRoleKey }}",
    "Content-Type": "video/mp4"
  },
  "bodyContentType": "binary",
  "binaryProperty": "data"
}
```

**Purpose:** Uploads the generated video file directly to the Supabase Storage bucket named `videos`.

---

## API Security and Authentication Summary

### API Keys Used:
1. **ElevenLabs:** `SECRET`
2. **OpenAI:** `sSECRET`
3. **Hedra:** `SECRET`

