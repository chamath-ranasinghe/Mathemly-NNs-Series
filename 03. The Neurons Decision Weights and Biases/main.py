from manim import *

# ---------------------- 2D Scene ----------------------
class NeuronLinearModel2D(ThreeDScene):
    def construct(self):
        title = Text("A Neuron as a Linear Model", font_size=36).to_edge(UP)
        self.play(Write(title))

        neuron = Circle(radius=0.5, color=BLUE).shift(RIGHT*2)
        x1 = MathTex("x_1").shift(LEFT*4 + UP*1)
        x2 = MathTex("x_2").shift(LEFT*4 + DOWN*1)
        w1 = MathTex("w_1").next_to(Line(x1.get_right(), neuron.get_left()).get_center(), UP)
        w2 = MathTex("w_2").next_to(Line(x2.get_right(), neuron.get_left()).get_center(), DOWN)

        arrow1 = Arrow(x1.get_right(), neuron.get_left() + UP*0.3, buff=0.1, color=GREEN)
        arrow2 = Arrow(x2.get_right(), neuron.get_left() + DOWN*0.3, buff=0.1, color=GREEN)

        self.play(Create(neuron), Write(x1), Write(x2))
        self.play(GrowArrow(arrow1), GrowArrow(arrow2))
        self.play(Write(w1), Write(w2))
        self.wait(0.5)

        eq = MathTex("z = w_1x_1 + w_2x_2 + b").next_to(neuron, RIGHT, buff=1)
        self.play(Write(eq))
        self.wait(1)

        contrib_text = Text("Each input contributes proportionally based on its weight.", font_size=26).next_to(eq, DOWN)
        self.play(Write(contrib_text))

        # Arrows brighten to show "inputs increase"
        self.play(arrow1.animate.set_color(YELLOW), arrow2.animate.set_color(YELLOW), run_time=1)
        self.play(arrow1.animate.scale(1.2), arrow2.animate.scale(1.2), run_time=1)
        self.play(arrow1.animate.scale(1/1.2).set_color(GREEN), arrow2.animate.scale(1/1.2).set_color(GREEN), run_time=1)
        self.wait(1)
        self.play(FadeOut(contrib_text))

        pos_text = Text("If both weights are positive, output increases as inputs increase.", font_size=24).next_to(eq, DOWN)
        self.play(Write(pos_text))
        self.wait(1.5)
        self.play(FadeOut(pos_text))

        neg_text = Text("If one weight is negative, that input reduces the output.", font_size=24).next_to(eq, DOWN)
        self.play(Write(neg_text))
        self.wait(1.5)
        self.play(FadeOut(neg_text))

        # Transition note
        next_text = Text("Let's see how the bias changes the prediction...", font_size=26).next_to(eq, DOWN)
        self.play(Write(next_text))
        self.wait(1.5)
        self.play(FadeOut(next_text), FadeOut(eq), FadeOut(neuron), FadeOut(x1), FadeOut(x2), FadeOut(arrow1), FadeOut(arrow2), FadeOut(w1), FadeOut(w2), FadeOut(title))
        self.wait(0.5)

# ---------------------- 3D Scene ----------------------
class NeuronBias3D(ThreeDScene):
    def construct(self):
        bias_text = Text("Bias shifts the output up or down — like moving the regression line.", font_size=26).to_edge(UP)
        self.add_fixed_in_frame_mobjects(bias_text)
        self.play(Write(bias_text))

        # Axes
        axes = ThreeDAxes(x_range=[-2, 2], y_range=[-2, 2], z_range=[-2, 2])
        self.add(axes)

        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.bias = 0

        def plane_func(u, v):
            return np.array([u, v, 0.5*u + 0.5*v + self.bias])

        surface = always_redraw(lambda: Surface(
            plane_func,
            u_range=[-2, 2],
            v_range=[-2, 2],
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_E, BLUE_D]
        ))
        self.add(surface)

        self.wait(1)
        # Tilt and shift
        self.move_camera(theta=75 * DEGREES, run_time=2)
        self.play(self.shift_bias(1), run_time=2)
        self.play(self.shift_bias(-1), run_time=2)
        self.wait(1)

        self.play(FadeOut(surface), FadeOut(axes), FadeOut(bias_text))
        self.wait(0.5)

        eq = MathTex("z = w_1x_1 + w_2x_2 + b", color=WHITE).scale(1.2)
        self.add_fixed_in_frame_mobjects(eq)
        self.play(Write(eq))
        box = SurroundingRectangle(eq, color=YELLOW)
        self.play(Create(box))
        msg = Text("Just like Linear Regression!", color=GREEN, font_size=32).next_to(eq, DOWN)
        self.add_fixed_in_frame_mobjects(msg)
        self.play(Write(msg))
        self.wait(2)

    def shift_bias(self, target_bias):
        """Smoothly animate the bias variable to move the plane."""
        return UpdateFromAlphaFunc(self, lambda mob, alpha: setattr(mob, "bias", interpolate(self.bias, target_bias, alpha)))
