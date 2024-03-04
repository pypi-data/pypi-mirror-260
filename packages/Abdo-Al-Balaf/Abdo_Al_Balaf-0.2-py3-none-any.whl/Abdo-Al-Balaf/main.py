from PIL import Image
import requests
from io import BytesIO

# GitHub raw image URL
github_image_url = 'https://shorturl.at/hxHW5'

# Fetch the image from the URL
response = requests.get(github_image_url)

try:
  image = Image.open(BytesIO(response.content))
  image.show()

except Exception as e:
  print(f"Error: {e}")
