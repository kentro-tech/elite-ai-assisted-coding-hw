"""Create a simple loading icon placeholder image."""
from PIL import Image, ImageDraw

# Create a 120x120 image with a light blue background
img = Image.new('RGB', (120, 120), color='#E3F2FD')

# Draw a border
draw = ImageDraw.Draw(img)
draw.rectangle([0, 0, 119, 119], outline='#2196F3', width=2)

# Draw a loading symbol (hourglass or clock emoji-style)
# Draw three dots in the center
dot_color = '#2196F3'
dot_radius = 8
center_y = 60

# Three dots horizontally
for i, x in enumerate([40, 60, 80]):
    draw.ellipse([x-dot_radius, center_y-dot_radius, x+dot_radius, center_y+dot_radius], fill=dot_color)

# Save the image
img.save('static/loading-icon.png')
print("✅ Created loading-icon.png")
