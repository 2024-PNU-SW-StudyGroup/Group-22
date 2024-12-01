# models.py


# __all__의 값은 모듈에서 이부로 공개된 API로 export할 모든 이름이 들어 있는 리스트다.
__all__ = ['Projectile']

class Projectile:
    def __init__(self, mass, velocity):
        self.mass = mass
        self.velocity = velocity
