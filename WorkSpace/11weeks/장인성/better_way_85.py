# 패키지를 사용해 모듈을 체계화하고 안정적인 API를 제공하라

from mypackage import *

a = Projectile(1.5, 3)
b = Projectile(4, 1.7)
after_a, after_b = simulate_collision(a, b)

# _ = _dot_product(a, b) import되지 않음