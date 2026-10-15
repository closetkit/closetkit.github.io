# 필름 그레인용 노이즈 타일 8장 (grain/g0.png … g7.png)
import os
import numpy as np
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grain')
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(5)
for i in range(8):
    n = rng.normal(128, 48, (512, 512)).clip(0, 255).astype('uint8')
    Image.fromarray(n, 'L').save(os.path.join(OUT, f'g{i}.png'))
print('grain →', OUT)
