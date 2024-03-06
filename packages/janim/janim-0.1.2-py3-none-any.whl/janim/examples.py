# flake8: noqa
from janim.imports import *


class SimpleCurveExample(Timeline):
    def construct(self) -> None:
        item1 = VItem(
            LEFT * 2, DR, UR * 3 + UP, RIGHT * 4, DR * 2, DOWN * 2, LEFT * 2,
            NAN_POINT,
            DL * 3, DL * 2, DOWN * 3, DL * 4, DL * 3,
        )
        item1.fill.set(alpha=0.5)
        item1.show()

        self.forward(0.5)
        self.play(item1.anim.color.set(BLUE))
        self.play(Rotate(item1, -90 * DEGREES))
        self.forward(0.5)

        item2 = VItem(LEFT, UP, RIGHT, DOWN, LEFT)
        item2.color.set(BLUE)
        item2.fill.set(alpha=0.2)

        state = self.camera.store_data()
        self.play(self.camera.anim.points.scale(0.5))
        self.play(self.camera.anim.become(state))

        self.play(
            Transform(item1, item2),
            duration=2
        )
        self.forward(1)
