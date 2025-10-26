"""Vision capabilities using Moondream and camera."""

import cv2
import base64
import requests
from PIL import Image
import io
import time
from typing import Optional
from . import config


class VisionHandler:
    """Handle camera input and vision understanding using Moondream."""
    
    def __init__(self):
        self.camera = None
        self.vision_model = "moondream"  # Just use "moondream" without version
        self.ollama_url = config.OLLAMA_BASE_URL
        
        # Verify Moondream is available
        self._check_moondream()
        
        print("✅ Vision system initialized")
    
    def _check_moondream(self):
        """Check if Moondream is available."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            # Check for moondream
            has_moondream = any("moondream" in name.lower() for name in model_names)
            
            if has_moondream:
                # Use the exact model name
                for name in model_names:
                    if "moondream" in name.lower():
                        self.vision_model = name
                        print(f"✅ Found vision model: {self.vision_model}")
                        break
            else:
                print("⚠️ Moondream not found. Run: ollama pull moondream")
                
        except Exception as e:
            print(f"⚠️ Could not check models: {e}")
    
    def start_camera(self) -> bool:
        """Start the camera."""
        try:
            self.camera = cv2.VideoCapture(0)
            
            if not self.camera.isOpened():
                print("❌ Could not open camera")
                return False
            
            # Set camera properties for better quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            # Warm up camera
            for _ in range(5):
                self.camera.read()
                time.sleep(0.1)
            
            print("✅ Camera started")
            return True
            
        except Exception as e:
            print(f"❌ Camera error: {e}")
            return False
    
    def stop_camera(self):
        """Stop the camera."""
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()
            print("✅ Camera stopped")
    
    def capture_frame(self) -> Optional[Image.Image]:
        """Capture a single frame from camera."""
        try:
            if not self.camera or not self.camera.isOpened():
                if not self.start_camera():
                    return None
            
            # Capture frame
            ret, frame = self.camera.read()
            
            if not ret:
                print("❌ Failed to capture frame")
                return None
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            image = Image.fromarray(frame_rgb)
            
            # Resize if needed (Moondream works best with smaller images)
            max_size = 512
            if image.size[0] > max_size or image.size[1] > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            print(f"❌ Capture error: {e}")
            return None
    
    def image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    def analyze_image(self, image: Image.Image, question: str = "Describe what you see") -> Optional[str]:
        """
        Analyze image using Moondream vision model via Ollama.
        
        Args:
            image: PIL Image to analyze
            question: Question to ask about the image
            
        Returns:
            Description or answer from vision model
        """
        try:
            print(f"👁️  Analyzing image with Moondream...")
            
            # Convert image to base64
            img_base64 = self.image_to_base64(image)
            
            # Moondream uses the /api/generate endpoint with images
            # Format according to Ollama vision API
            payload = {
                "model": self.vision_model,
                "prompt": question,
                "images": [img_base64],
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Lower for more factual descriptions
                    "num_predict": 150
                }
            }
            
            print(f"📡 Calling Ollama vision API...")
            
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60  # Vision models take longer
            )
            
            response.raise_for_status()
            result = response.json()
            
            description = result.get("response", "").strip()
            
            if description:
                print(f"✅ Vision: {description[:100]}...")
                return description
            else:
                print("⚠️ No description from vision model")
                return None
                
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            print(f"Response: {e.response.text if hasattr(e, 'response') else 'No response'}")
            return None
        except Exception as e:
            print(f"❌ Vision analysis failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def see_and_describe(self, question: str = "What do you see in this image? Describe in detail.") -> Optional[str]:
        """
        Capture image from camera and describe it.
        
        Args:
            question: Question to ask about the image
            
        Returns:
            Description of what the camera sees
        """
        try:
            print("📸 Capturing image from camera...")
            
            # Capture frame
            image = self.capture_frame()
            
            if not image:
                print("❌ Could not capture image")
                return None
            
            print(f"✅ Image captured: {image.size}")
            
            # Analyze with Moondream
            description = self.analyze_image(image, question)
            
            return description
            
        except Exception as e:
            print(f"❌ See and describe failed: {e}")
            return None
    
    def __del__(self):
        """Cleanup."""
        self.stop_camera()
