from PIL import Image, ImageEnhance
from pathlib import Path

files = [Path('assets/Junken/gu.png'), Path('assets/Junken/choki.png')]
ref_path = Path('assets/Junken/pa.png')
ref = Image.open(ref_path).convert('RGBA')
ref_bg = ref.getpixel((0, 0))

for path in files:
    img = Image.open(path).convert('RGBA')
    width, height = img.size
    data = []
    for r, g, b, a in img.getdata():
        if a <= 24:
            data.append((r, g, b, 0))
            continue
        if abs(r - ref_bg[0]) <= 45 and abs(g - ref_bg[1]) <= 45 and abs(b - ref_bg[2]) <= 45:
            data.append((r, g, b, 0))
        else:
            data.append((r, g, b, a))
    img.putdata(data)

    # Keep the subject crisp and close in feel to the reference image.
    rgb = img.convert('RGB')
    rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.05)
    img = rgb.convert('RGBA')

    # Restore the alpha mask we just created.
    alpha = Image.new('L', img.size, 255)
    mask_pixels = []
    for r, g, b, a in img.getdata():
        mask_pixels.append(255 if a > 0 else 0)
    alpha.putdata(mask_pixels)
    img.putalpha(alpha)

    img.save(path)
    print(f'updated {path}')
