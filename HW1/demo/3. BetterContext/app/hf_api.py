"""HuggingFace API integration for image generation.

Supports two modes:
1. Inference API (production) - Requires HuggingFace Pro/credits
2. Gradio API (testing) - Free, uses public Gradio apps on HF Spaces
"""

import io
import os
from typing import Optional
from huggingface_hub import InferenceClient
from gradio_client import Client as GradioClient, handle_file
import config

# Use Gradio API for testing (free) or Inference API for production (paid)
USE_GRADIO_API = os.getenv("USE_GRADIO_API", "true").lower() == "true"


def create_inference_client() -> InferenceClient:
    """
    Create and return a HuggingFace InferenceClient configured for image generation.
    
    Returns:
        InferenceClient: Configured client for HuggingFace Inference API
        
    Raises:
        ValueError: If HF_TOKEN is not set in environment variables
    """
    if not config.HF_TOKEN:
        raise ValueError(
            "HF_TOKEN environment variable is not set. "
            "Please create a .env file with your HuggingFace API token. "
            "Get your token from https://huggingface.co/settings/tokens"
        )
    
    return InferenceClient(
        provider="hf-inference",
        api_key=config.HF_TOKEN,
    )


def generate_image_prompt(text: str, context: str = "") -> str:
    """
    Generate an image prompt from text description.
    
    Args:
        text: The text description to convert into an image prompt
        context: Optional context to add to the prompt (e.g., "story opening", "consequence")
        
    Returns:
        str: A formatted prompt suitable for image generation
    """
    # Create a concise, visual prompt from the text
    # Keep it simple and focused on visual elements
    prompt = text.strip()
    
    # Add context if provided
    if context:
        prompt = f"{context}: {prompt}"
    
    # Limit prompt length to avoid API issues
    max_length = 200
    if len(prompt) > max_length:
        prompt = prompt[:max_length].rsplit(' ', 1)[0] + "..."
    
    return prompt


def generate_icon_image_gradio(prompt: str) -> Optional[bytes]:
    """
    Generate an icon image using HuggingFace Gradio app (FREE).
    
    This uses the public FLUX.1-dev Gradio app on HuggingFace Spaces,
    which is free to use but may have rate limits.
    
    Args:
        prompt: The text prompt describing the image to generate
        
    Returns:
        bytes: The generated image as bytes (PNG format), or None if generation fails
        
    Raises:
        Exception: If API call fails or times out
    """
    try:
        # Connect to the FLUX.1-dev Gradio app
        client = GradioClient("black-forest-labs/FLUX.1-dev")
        
        # Generate image using the Gradio app
        # Returns a tuple with (image_path, seed)
        result = client.predict(
            prompt=prompt,
            seed=0,
            randomize_seed=True,
            width=512,  # Smaller size for icons
            height=512,
            guidance_scale=3.5,
            num_inference_steps=28,
            api_name="/infer"
        )
        
        # Result is a tuple: (image_path, seed)
        image_path = result[0] if isinstance(result, tuple) else result
        
        # Read the image file and return as bytes
        with open(image_path, 'rb') as f:
            return f.read()
            
    except Exception as e:
        # Log the error but don't crash the application
        print(f"Error generating image via Gradio: {e}")
        raise


def generate_icon_image_inference(prompt: str, model: str = "black-forest-labs/FLUX.1-dev") -> Optional[bytes]:
    """
    Generate an icon image using HuggingFace text-to-image models.
    
    Note: Text-to-image models require HuggingFace Pro subscription or credits.
    Free tier tokens will receive 402 Payment Required errors.
    
    Args:
        prompt: The text prompt describing the image to generate
        model: The model to use for generation (default: stable-diffusion-2-1)
               Popular options:
               - "stabilityai/stable-diffusion-2-1" (requires payment)
               - "black-forest-labs/FLUX.1-dev" (requires payment, higher quality)
        
    Returns:
        bytes: The generated image as bytes (PNG format), or None if generation fails
        
    Raises:
        Exception: If API call fails or times out
    """
    try:
        client = create_inference_client()
        
        # Generate image using the specified model
        # The output is a PIL.Image object
        image = client.text_to_image(
            prompt,
            model=model,
        )
        
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()
        
    except Exception as e:
        # Log the error but don't crash the application
        print(f"Error generating image: {e}")
        raise


def generate_icon_image(prompt: str) -> Optional[bytes]:
    """
    Generate an icon image using the configured API (Gradio or Inference).
    
    Automatically chooses between:
    - Gradio API (free, for testing) if USE_GRADIO_API=true
    - Inference API (paid, for production) if USE_GRADIO_API=false
    
    Args:
        prompt: The text prompt describing the image to generate
        
    Returns:
        bytes: The generated image as bytes (PNG format), or None if generation fails
        
    Raises:
        Exception: If API call fails or times out
    """
    if USE_GRADIO_API:
        return generate_icon_image_gradio(prompt)
    else:
        return generate_icon_image_inference(prompt)


def test_api_connection() -> dict[str, str | bool]:
    """
    Test the HuggingFace API connection with a simple image generation.
    
    Uses Gradio API (free) if USE_GRADIO_API=true, otherwise uses Inference API (paid).
    
    Returns:
        dict: Status information with 'success' boolean, 'message' string, and 'api_mode' string
    """
    api_mode = "Gradio API (Free)" if USE_GRADIO_API else "Inference API (Paid)"
    
    try:
        # Try to create a client (validates token) - only needed for Inference API
        if not USE_GRADIO_API:
            create_inference_client()
        
        # Try a simple test generation
        test_prompt = "A simple red circle on white background"
        
        if USE_GRADIO_API:
            # Use free Gradio API
            image_bytes = generate_icon_image_gradio(test_prompt)
        else:
            # Use paid Inference API
            image_bytes = generate_icon_image_inference(test_prompt, model="CompVis/stable-diffusion-v1-4")
        
        if image_bytes:
            return {
                "success": True,
                "message": f"✅ {api_mode} connection successful! Generated test image ({len(image_bytes)} bytes)",
                "api_mode": api_mode
            }
        else:
            return {
                "success": False,
                "message": f"❌ {api_mode} connection failed: No image data returned",
                "api_mode": api_mode
            }
            
    except ValueError as e:
        return {
            "success": False,
            "message": f"⚙️ Configuration error: {str(e)}",
            "api_mode": api_mode
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ {api_mode} connection failed: {str(e)}",
            "api_mode": api_mode
        }
