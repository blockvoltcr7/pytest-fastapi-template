import os
import httpx
import asyncio
import time
import json
from typing import Optional, Dict, Any
from app.core.config import settings

class VideoService:
    """
    Hedra API integration with intelligent status polling
    """
    
    def __init__(self):
        self.api_key = settings.hedra_api_key
        self.base_url = "https://api.hedra.com/web-app/public"
        self.timeout = httpx.Timeout(120.0)
        
        # Polling configuration from settings
        self.initial_poll_interval = settings.hedra_initial_poll_interval
        self.max_poll_interval = settings.hedra_max_poll_interval
        self.poll_backoff_factor = settings.hedra_poll_backoff_factor
        self.max_poll_time = settings.hedra_max_poll_time
        
        # Ensure video output directory exists
        os.makedirs(settings.videos_dir, exist_ok=True)
    
    async def create_lipsync_video(
        self,
        audio_path: str,
        image_path: str,
        scene_index: int,
        speaker: str,
        campaign_id: str
    ) -> Optional[str]:
        """
        Complete video generation with intelligent status polling
        """
        if not self.api_key:
            raise ValueError("Hedra API key not configured")
        
        try:
            print(f"🎬 Starting video generation for scene {scene_index} ({speaker})")
            
            # Steps 1-4: Create assets and upload files
            print(f"📦 Creating and uploading assets...")
            audio_asset_id = await self._create_hedra_asset("audio", f"{campaign_id}_scene_{scene_index}_audio")
            image_asset_id = await self._create_hedra_asset("image", f"{campaign_id}_scene_{scene_index}_image")
            
            await self._upload_file_to_hedra(audio_asset_id, audio_path, "audio/mpeg")
            await self._upload_file_to_hedra(image_asset_id, image_path, "image/png")
            print(f"✅ Assets uploaded - Audio: {audio_asset_id}, Image: {image_asset_id}")
            
            # Step 5: Create video generation
            print(f"🎥 Creating video generation...")
            generation_response = await self._create_video_generation(audio_asset_id, image_asset_id, speaker)
            generation_id = generation_response["id"]
            asset_id = generation_response["asset_id"]
            
            print(f"✅ Video generation started - ID: {generation_id}, Asset ID: {asset_id}")
            
            # Step 6: Poll status until complete (UPDATED - no fixed wait time)
            await self._poll_generation_status(generation_id)
            
            # Step 7: Get video asset
            print(f"📥 Getting completed video asset...")
            video_asset = await self._get_video_asset(asset_id)
            video_url = video_asset["asset"]["url"]
            
            print(f"✅ Video ready for download: {video_url}")
            
            # Step 8: Download final video
            final_video_path = await self._download_video(
                video_url=video_url,
                filename=f"{campaign_id}_scene_{scene_index}_{speaker.lower().replace(' ', '_')}.mp4"
            )
            
            print(f"🎉 Video generation complete: {final_video_path}")
            return final_video_path
            
        except Exception as e:
            print(f"❌ Error generating video for scene {scene_index}: {str(e)}")
            return None
    
    async def _create_hedra_asset(self, asset_type: str, asset_name: str) -> str:
        """
        Create asset container in Hedra
        POST /public/assets
        """
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "name": asset_name,
            "type": asset_type  # "audio" or "image"
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/assets",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["id"]
            else:
                raise Exception(f"Failed to create {asset_type} asset: {response.status_code} - {response.text}")
    
    async def _upload_file_to_hedra(self, asset_id: str, file_path: str, content_type: str):
        """
        Upload file to Hedra asset
        POST /public/assets/{id}/upload
        Content-Type: multipart/form-data
        """
        headers = {
            "X-Api-Key": self.api_key
            # No Content-Type header - httpx will set multipart automatically
        }
        
        # Verify file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file content
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Prepare multipart form data
        files = {
            'file': (os.path.basename(file_path), file_content, content_type)
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/assets/{asset_id}/upload",
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to upload file to asset {asset_id}: {response.status_code} - {response.text}")
    
    async def _create_video_generation(self, audio_asset_id: str, image_asset_id: str, speaker: str) -> Dict:
        """
        Create video generation - matches N8N "Create Video (Hedra)" exactly
        POST /public/generations
        
        Returns: {
            "id": "generation_id", 
            "asset_id": "asset_id"  # This is what we poll for completion
        }
        """
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Create speaker-specific video prompt
        video_prompt = self._create_video_prompt(speaker)
        
        payload = {
            "type": "video",
            "ai_model_id": "d1dd37a3-e39a-4854-a298-6510289f9cf2",  # Hedra's lip-sync model
            "start_keyframe_id": image_asset_id,
            "audio_id": audio_asset_id,
            "generated_video_inputs": {
                "text_prompt": video_prompt,
                "resolution": "720p",
                "aspect_ratio": "9:16",
                "duration_ms": 5000  # Default duration like N8N
            }
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/generations",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                # Ensure we have both generation_id and asset_id
                if "id" not in result:
                    raise Exception("No generation ID returned")
                if "asset_id" not in result:
                    raise Exception("No asset ID returned")
                return result
            else:
                raise Exception(f"Failed to create video generation: {response.status_code} - {response.text}")
    
    # NEW: Intelligent status polling method
    async def _poll_generation_status(self, generation_id: str) -> Dict:
        """
        Poll generation status with intelligent intervals
        GET /public/generations/{generation_id}/status
        
        Polling strategy:
        - Start with 15 second intervals
        - Increase interval by 20% after each poll (max 60s)
        - Stop when status is complete/failed or timeout reached
        """
        start_time = time.time()
        current_interval = self.initial_poll_interval
        poll_count = 0
        
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        print(f"🔄 Starting status polling for generation {generation_id}")
        print(f"   Initial interval: {self.initial_poll_interval}s, Max time: {self.max_poll_time}s")
        
        while (time.time() - start_time) < self.max_poll_time:
            try:
                poll_count += 1
                elapsed = int(time.time() - start_time)
                
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(
                        f"{self.base_url}/generations/{generation_id}/status",
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        status_data = response.json()
                        status = status_data.get("status", "unknown").lower()
                        progress = status_data.get("progress", 0)
                        
                        print(f"📊 Poll #{poll_count}: {status} (progress: {progress}%, elapsed: {elapsed}s)")
                        
                        # Check for completion
                        if status in ["completed", "complete", "done", "success"]:
                            total_time = time.time() - start_time
                            print(f"✅ Generation completed! Total time: {total_time:.1f}s")
                            return status_data
                        
                        # Check for failure
                        elif status in ["failed", "error", "cancelled", "timeout"]:
                            error_message = status_data.get("error_message", f"Generation failed with status: {status}")
                            print(f"❌ Generation failed: {error_message}")
                            raise Exception(f"Generation failed: {error_message}")
                        
                        # Still processing - calculate next poll time
                        else:
                            # Adaptive polling based on progress
                            if progress > 0:
                                # If we have progress info, be more aggressive early on
                                if progress < 30:
                                    next_interval = self.initial_poll_interval
                                elif progress < 70:
                                    next_interval = int(self.initial_poll_interval * 1.5)
                                else:
                                    next_interval = int(self.initial_poll_interval * 2)
                            else:
                                # No progress info - use backoff strategy
                                next_interval = min(
                                    int(current_interval * self.poll_backoff_factor),
                                    self.max_poll_interval
                                )
                            
                            print(f"⏱️  Waiting {next_interval}s before next poll...")
                            await asyncio.sleep(next_interval)
                            current_interval = next_interval
                    
                    else:
                        # API call failed - wait longer before retry
                        print(f"⚠️  Status API returned {response.status_code}, waiting {current_interval}s...")
                        await asyncio.sleep(current_interval)
                        current_interval = min(
                            int(current_interval * self.poll_backoff_factor),
                            self.max_poll_interval
                        )
                
            except httpx.TimeoutException:
                print(f"⏱️  Request timeout, waiting {current_interval}s...")
                await asyncio.sleep(current_interval)
                current_interval = min(current_interval * 2, self.max_poll_interval)
                
            except Exception as e:
                print(f"⚠️  Polling error: {str(e)}, waiting {current_interval}s...")
                await asyncio.sleep(current_interval)
                current_interval = min(current_interval * 2, self.max_poll_interval)
        
        # Timeout reached
        total_time = time.time() - start_time
        raise Exception(f"Generation polling timed out after {total_time:.1f}s ({poll_count} polls)")
    
    async def _get_video_asset(self, asset_id: str) -> Dict:
        """
        Get video asset information - matches N8N "Get BabyPod Video (Hedra)" exactly
        GET /public/assets?type=video&ids={asset_id}
        
        Returns the asset with download URL in asset.url
        """
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        params = {
            "type": "video",
            "ids": asset_id
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/assets",
                params=params,
                headers=headers
            )
            
            if response.status_code == 200:
                assets = response.json()
                
                if assets and len(assets) > 0:
                    asset = assets[0]
                    
                    # Verify the asset structure matches N8N output
                    if asset.get("asset") and asset["asset"].get("url"):
                        print(f"✅ Video asset ready: {asset['asset']['url']}")
                        return asset
                    else:
                        raise Exception("Asset exists but doesn't have download URL yet")
                else:
                    raise Exception("No video assets found for the given ID")
            else:
                raise Exception(f"Failed to get video asset: {response.status_code} - {response.text}")
    
    async def _download_video(self, video_url: str, filename: str) -> str:
        """
        Download video from Hedra URL - matches N8N "Download BabyPod Video (Hedra)"
        GET {video_url}
        """
        output_path = os.path.join(settings.videos_dir, filename)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(video_url)
            
            if response.status_code == 200:
                # Write video content to file
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                # Verify download
                file_size = os.path.getsize(output_path)
                if file_size > 0:
                    print(f"📥 Video downloaded: {output_path} ({file_size:,} bytes)")
                    return output_path
                else:
                    raise Exception("Downloaded video file is empty")
            else:
                raise Exception(f"Failed to download video: {response.status_code} - {response.text}")
    
    def _create_video_prompt(self, speaker: str) -> str:
        """
        Create video generation prompt based on speaker
        Matches the text_prompt used in N8N workflow
        """
        base_prompt = """A baby podcast host seated in front of a microphone, speaking with calm intensity and natural focus. Subtle facial expressions, minimal head movement, steady eye contact with the camera. Studio lighting with a professional podcast setup in the background."""
        
        # Add speaker-specific personality traits
        if "1" in speaker:  # Baby 1 - warm, inviting
            return base_prompt + " Warm, welcoming expression with gentle smile and kind eyes."
        else:  # Baby 2 - curious, thoughtful  
            return base_prompt + " Curious, thoughtful expression showing interest and attentiveness."
    
    async def test_connection(self) -> bool:
        """Test Hedra API connection"""
        if not self.api_key:
            print("❌ No Hedra API key configured")
            return False
        
        print(f"Hedra API key: {self.api_key}")
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            print(f"🔍 Testing Hedra API connection to {self.base_url}/assets")
            async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
                # Test with a simple asset creation
                response = await client.post(
                    f"{self.base_url}/assets",
                    json={"name": "connection_test", "type": "audio"},
                    headers=headers
                )
                
                if response.status_code == 200:
                    print("✅ Hedra API responded with 200 OK")
                    return True
                else:
                    print(f"❌ Hedra API returned status {response.status_code}")
                    print(f"Response text: {response.text}")
                    return False
                    
        except httpx.TimeoutException:
            print("❌ Hedra API request timed out")
            return False
        except httpx.RequestError as e:
            print(f"❌ Hedra API request failed: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error testing Hedra connection: {str(e)}")
            return False
    
    def get_generation_status_sync(self, generation_id: str) -> Dict[str, Any]:
        """
        Synchronous method to check generation status
        Useful for debugging or one-off checks
        """
        import requests
        
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/generations/{generation_id}/status",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)} 