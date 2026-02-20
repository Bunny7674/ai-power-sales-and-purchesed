from services.image_service import generate_image

def create_marketing_image(prompt):
    image_url = generate_image(prompt)
    return image_url

# Langchain tools temporarily disabled due to missing dependencies
# To enable, install: pip install langchain

def generate_marketing_image(prompt: str) -> str:
    """Generate marketing image from text prompt."""
    return generate_image(prompt)

