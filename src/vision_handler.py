"""Vision capabilities using Moondream and camera (Async)."""

import cv2
import base64
import aiohttp
import asyncio
from PIL import Image
import io
import time
from typing import Optional
from . import config
from .logger import logger

class VisionHandler:
    """Handle camera input and vision understanding using Moondream (Async)."""
    
    def __init__(self):
        self.camera = None
        self.vision_model = config.VISION_MODEL
        self.ollama_url = config.OLLAMA_BASE_URL
        self._camera_lock = asyncio.Lock()
        
    async def initialize(self):
        """Async initialization."""
        await self._check_moondream()
        logger.info("✅ Vision system initialized")
    
    async def _check_moondream(self):
        """Check if Moondream is available."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_url}/api/tags", timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = data.get("models", [])
                        model_names = [m["name"] for m in models]
                        
                        has_moondream = any("moondream" in name.lower() for name in model_names)
                        
                        if has_moondream:
                            for name in model_names:
                                if "moondream" in name.lower():
                                    self.vision_model = name
                                    logger.info(f"✅ Found vision model: {self.vision_model}")
                                    break
                        else:
                            logger.warning("⚠️ Moondream not found. Run: ollama pull moondream")
        except Exception as e:
            logger.warning(f"⚠️ Could not check models: {e}")
    
    async def start_camera(self) -> bool:
        """Start the camera (run in executor)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._start_camera_sync)

    def _start_camera_sync(self) -> bool:
        """Synchronous camera start."""
        try:
            if self.camera and self.camera.isOpened():
                return True
                
            self.camera = cv2.VideoCapture(config.CAMERA_INDEX)
            
            if not self.camera.isOpened():
                logger.error("❌ Could not open camera")
                return False
            
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # Warm up
            for _ in range(5):
                self.camera.read()
                time.sleep(0.1)
            
            logger.info("✅ Camera started")
            return True
            
        except Exception as e:
            logger.error(f"❌ Camera error: {e}")
            return False
    
    async def stop_camera(self):
        """Stop the camera."""
        if self.camera:
            self.camera.release()
            self.camera = None
            cv2.destroyAllWindows()
            logger.info("✅ Camera stopped")
    
    async def capture_frame(self) -> Optional[Image.Image]:
        """Capture a single frame from camera (Async)."""
        async with self._camera_lock:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._capture_frame_sync)

    def _capture_frame_sync(self) -> Optional[Image.Image]:
        """Synchronous frame capture."""
        try:
            if not self.camera or not self.camera.isOpened():
                if not self._start_camera_sync():
                    return None
            
            ret, frame = self.camera.read()
            
            if not ret:
                logger.error("❌ Failed to capture frame")
                return None
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            
            # Resize
            max_size = 512
            if image.size[0] > max_size or image.size[1] > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            logger.error(f"❌ Capture error: {e}")
            return None
    
    def image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    async def analyze_image(self, image: Image.Image, question: str = "Describe what you see") -> Optional[str]:
        """Analyze image using Moondream vision model via Ollama (Async)."""
        try:
            logger.info(f"👁️  Analyzing image with Moondream...")
            
            img_base64 = self.image_to_base64(image)
            
            payload = {
                "model": self.vision_model,
                "prompt": question,
                "images": [img_base64],
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 150
                }
            }
            
            logger.info(f"📡 Calling Ollama vision API...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=60
                ) as response:
                    if response.status != 200:
                        logger.error(f"❌ HTTP Error: {response.status}")
                        return None
                        
                    result = await response.json()
                    description = result.get("response", "").strip()
            
            if description:
                logger.info(f"✅ Vision: {description[:100]}...")
                return description
            else:
                logger.warning("⚠️ No description from vision model")
                return None
                
        except Exception as e:
            logger.error(f"❌ Vision analysis failed: {e}")
            return None
    
    async def see_and_describe(self, question: str = "What do you see in this image? Describe in detail.") -> Optional[str]:
        """Capture and describe (Async)."""
        try:
            logger.info("📸 Capturing image from camera...")
            image = await self.capture_frame()
            
            if not image:
                logger.error("❌ Could not capture image")
                return None
            
            logger.info(f"✅ Image captured: {image.size}")
            description = await self.analyze_image(image, question)
            return description
            
        except Exception as e:
            logger.error(f"❌ See and describe failed: {e}")
            return None
        finally:
            await self.stop_camera()
    
    def __del__(self):
        """Cleanup."""
        if self.camera:
            self.camera.release()
