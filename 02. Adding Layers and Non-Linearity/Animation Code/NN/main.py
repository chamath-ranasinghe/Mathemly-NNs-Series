from manim import *
import numpy as np

class LinearBoundaryDemo(Scene):
    def construct(self):
        # Title
        title = Text("Linear Decision Boundaries", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": False},
        )
        axes.to_edge(DOWN)
        self.play(Create(axes))
        self.wait(1)

        # Formula z = x^T w + b
        formula = MathTex("z = x^T w + b")
        formula.next_to(title, DOWN)
        self.play(Write(formula))
        self.wait(1)

        # First: Linearly separable points
        np.random.seed(0)
        blue_points = [axes.c2p(x, y) for x, y in np.random.randn(10, 2) + np.array([-2, -2])]
        red_points = [axes.c2p(x, y) for x, y in np.random.randn(10, 2) + np.array([2, 2])]

        blue_dots = VGroup(*[Dot(p, color=BLUE) for p in blue_points])
        red_dots = VGroup(*[Dot(p, color=RED) for p in red_points])

        self.play(FadeIn(blue_dots), FadeIn(red_dots))
        self.wait(1)

        # Slanted line decision boundary: y = x
        line = Line(
            start=axes.c2p(-3,3),  # since y = x
            end=axes.c2p(3, -3),
            color=YELLOW
        )
        self.play(Create(line))
        self.wait(2)

        # Now introduce curved data
        self.play(FadeOut(blue_dots), FadeOut(red_dots), FadeOut(line))
        self.wait(1)

        # New data: Blue in a circle, red outside
        theta = np.linspace(0, 2 * np.pi, 20)
        blue_circle = [axes.c2p(np.cos(t), np.sin(t)) for t in theta]
        red_outside = [axes.c2p(r*np.cos(t), r*np.sin(t)) for t in theta for r in [2]]

        blue_dots2 = VGroup(*[Dot(p, color=BLUE) for p in blue_circle])
        red_dots2 = VGroup(*[Dot(p, color=RED) for p in red_outside])

        self.play(FadeIn(blue_dots2), FadeIn(red_dots2))
        self.wait(1)

        # Try the same straight line again
        line2 = Line(
            start=axes.c2p(-3, 3),
            end=axes.c2p(3, -3),
            color=YELLOW
        )
        self.play(Create(line2))
        self.wait(2)

        self.play(FadeOut(axes), FadeOut(title), FadeOut(formula), FadeOut(blue_dots2), FadeOut(red_dots2), FadeOut(line2))

        # Highlight failure
        fail_text = Text("Straight line fails!", color=YELLOW)
        self.play(Write(fail_text))
        self.wait(3)

class ActivationDemo(Scene):
    def construct(self):
        # --- Title & axes ---
        title = Text("Activation functions", font_size=32)
        self.play(Write(title), run_time=1)
        self.wait(1)
        self.play(title.animate.to_edge(UP), run_time=1)
        self.wait(0.2)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": False},
        ).to_edge(DOWN)
        self.play(Create(axes), run_time=1)
        self.wait(0.2)

        # --- Formula ---
        formula = MathTex("y = A(x^T w)")
        formula.next_to(title, DOWN, buff=0.5)
        self.play(Write(formula), run_time=1)
        self.wait(0.2)

        # --- Data (blue inside, red outside) ---
        theta = np.linspace(0, 2 * np.pi, 24)
        blue_pts = [axes.c2p(np.cos(t), np.sin(t)) for t in theta]
        red_pts = [axes.c2p(2 * np.cos(t), 2 * np.sin(t)) for t in theta]

        blue_dots = VGroup(*[Dot(p, color=BLUE) for p in blue_pts])
        red_dots = VGroup(*[Dot(p, color=RED) for p in red_pts])

        self.play(FadeIn(blue_dots), FadeIn(red_dots), run_time=1)
        self.wait(0.2)

        # --- Initial vertical segment (we pick the y-range [-1,1] to match final curve domain) ---
        initial_line = Line(axes.c2p(0, -1.5), axes.c2p(0, 1.5), color=YELLOW)
        self.play(Create(initial_line), run_time=1)
        self.wait(0.5)

        # --- ValueTracker controlling the bend ---
        factor = ValueTracker(0.0)

        # Helper that returns an always_redraw VMobject representing one side (top or bottom).
        def make_bending_mobject(sign=1, samples=120):
            def _mobject():
                s_vals = np.linspace(-1.5, 1.5, samples)
                pts = []
                for s in s_vals:
                    # final curve (circle of radius 1.5): y = ±sqrt(1.5 - s^2)
                    y_final = sign * np.sqrt(max(0.0, 1.5**2 - s * s))
                    p_final = np.array(axes.c2p(s, y_final))
                    # initial vertical segment point (x = 0, y = s)
                    p_initial = np.array(axes.c2p(0.0, s))
                    t = factor.get_value()
                    p = (1 - t) * p_initial + t * p_final
                    pts.append(p)
                vm = VMobject()
                # create a smooth curve through the sampled points
                vm.set_points_smoothly(pts)
                vm.set_color(YELLOW)
                return vm
            return always_redraw(_mobject)

        top_curve = make_bending_mobject(sign=1)
        bottom_curve = make_bending_mobject(sign=-1)

        # Replace the initial line with the top curve object (at factor=0 they coincide),
        # add the bottom curve (it will also coincide at factor=0).
        # We call Transform with the current top_curve state (factor=0) so the morph looks natural.
        static_top = top_curve.copy()
        self.play(Transform(initial_line, static_top), run_time=1)

        # Now replace static_top with the real updating top_curve
        self.remove(initial_line, static_top)
        self.add(top_curve, bottom_curve)

        # Animate the bending
        self.play(factor.animate.set_value(1.0), run_time=5)

        self.play(FadeOut(blue_dots), FadeOut(red_dots), FadeOut(axes), FadeOut(title), FadeOut(formula), FadeOut(top_curve), FadeOut(bottom_curve))

        # Final text
        success = Text("Non-linear Boundary", color=YELLOW)
        self.play(Write(success), run_time=1)
        self.wait(4.5)

class ActivationFunctions(Scene):
    def construct(self):
        title = Text("Activation Functions")
        self.play(Write(title))
        self.wait(8)

class StepFunctionDemo(Scene):
    def construct(self):
        # 1. Title at center
        title = Text("Step or Sign Function", font_size=40)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2. Move title to top with smaller size
        self.play(title.animate.scale(0.7).to_edge(UP), run_time=1.5)
        self.wait(0.5)

        # 3. Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        self.play(Create(axes), run_time=1.5)
        self.wait(0.5)

        # 4. Step function: two horizontal lines
        left_line = axes.plot(lambda x: -1, x_range=[-4, 0], color=YELLOW)
        right_line = axes.plot(lambda x: 1, x_range=[0, 4], color=YELLOW)
        self.play(Create(left_line), Create(right_line), run_time=1.5)

        # Add open and closed circles at x=0
        open_dot = Dot(axes.c2p(0, -1), color=YELLOW, fill_opacity=0)  # open circle
        closed_dot = Dot(axes.c2p(0, 1), color=YELLOW, fill_opacity=1) # closed circle
        self.play(FadeIn(open_dot), FadeIn(closed_dot), run_time=0.8)
        self.wait(0.5)

        # 5. Highlight above the threshold: x>=0
        above_line = axes.plot(lambda x: 1, x_range=[0, 4], color=GREEN, stroke_width=6)
        self.play(ReplacementTransform(right_line.copy(), above_line), run_time=1)
        self.wait(0.5)

        # 6. Highlight below the threshold: x<0
        below_line = axes.plot(lambda x: -1, x_range=[-4, 0], color=RED, stroke_width=6)
        self.play(ReplacementTransform(left_line.copy(), below_line), run_time=1)
        self.wait(0.5)

        # 7. Display "Hard to learn"
        hard_text = Text("Hard to learn", color=RED, font_size=32)
        hard_text.next_to(axes, DOWN)
        self.play(Write(hard_text), run_time=1.5)
        self.wait(2)  # pause to make total runtime ≈ 16s

class SigmoidFunctionDemo(Scene):
    def construct(self):
        # 1. Title at center
        title = Text("Sigmoid Function", font_size=40)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2. Move title to top with smaller size
        self.play(title.animate.scale(0.7).to_edge(UP), run_time=1.5)

        # 3. Create axes
        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[-0.2, 1.2, 0.2],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        self.play(Create(axes), run_time=1.5)

        # 4. Define sigmoid function
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        # 5. Plot sigmoid curve
        sigmoid_graph = axes.plot(sigmoid, x_range=[-6, 6], color=YELLOW)
        self.play(Create(sigmoid_graph), run_time=1.5)

        # 6. Highlight middle steep part
        steep_part = axes.plot(sigmoid, x_range=[-2, 2], color=GREEN, stroke_width=6)
        self.play(ReplacementTransform(sigmoid_graph.copy(), steep_part), run_time=1)

        # 7. Highlight squashing regions
        left_squash = axes.plot(sigmoid, x_range=[-6, -3], color=BLUE, stroke_width=6)
        right_squash = axes.plot(sigmoid, x_range=[3, 6], color=BLUE, stroke_width=6)
        self.play(ReplacementTransform(sigmoid_graph.copy(), left_squash), run_time=0.8)
        self.play(ReplacementTransform(sigmoid_graph.copy(), right_squash), run_time=0.8)
        self.wait(0.5)

        # 8. Text: Perfect for probabilities
        prob_text = Text("Perfect for probabilities", color=YELLOW, font_size=32)
        prob_text.next_to(axes, DOWN, buff=0.5)
        self.play(Write(prob_text), run_time=1.5)
        self.wait(3)  # pause to make total runtime ≈ 15s

class TanhFunctionDemo(Scene):
    def construct(self):
        # 1. Title at center
        title = Text("Tanh Function", font_size=40)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2. Move title to top
        self.play(title.animate.scale(0.7).to_edge(UP), run_time=1.5)
        self.wait(0.5)

        # 3. Create axes
        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[-1.2, 1.2, 0.5],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        self.play(Create(axes), run_time=1.5)

        # 4. Define tanh function
        def tanh_fn(x):
            return np.tanh(x)

        # 5. Plot tanh curve
        tanh_graph = axes.plot(tanh_fn, x_range=[-6, 6], color=YELLOW)
        self.play(Create(tanh_graph), run_time=1.5)

        # 6. Highlight center steep region
        center_region = axes.plot(tanh_fn, x_range=[-2, 2], color=GREEN, stroke_width=6)
        self.play(ReplacementTransform(tanh_graph.copy(), center_region), run_time=1)

        # 7. Highlight squashing regions
        left_squash = axes.plot(tanh_fn, x_range=[-6, -3], color=BLUE, stroke_width=6)
        right_squash = axes.plot(tanh_fn, x_range=[3, 6], color=BLUE, stroke_width=6)
        self.play(ReplacementTransform(tanh_graph.copy(), left_squash), run_time=0.8)
        self.play(ReplacementTransform(tanh_graph.copy(), right_squash), run_time=0.8)

        # 8. Add explanatory text
        text = Text("Centered at zero → helps learning smoothly", font_size=32, color=YELLOW)
        text.next_to(axes, DOWN)
        self.play(Write(text), run_time=1.5)
        self.wait(2)  # pause to make total runtime ≈ 15s

class ReLUFunctionDemo(Scene):
    def construct(self):
        # 1. Title at center
        title = Text("ReLU (Rectified Linear Unit)", font_size=40)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2. Move title to top
        self.play(title.animate.scale(0.7).to_edge(UP), run_time=1.5)
        self.wait(0.5)

        # 3. Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 4, 1],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        self.play(Create(axes), run_time=1.5)
        self.wait(0.5)

        # 4. Define ReLU function
        def relu_fn(x):
            return np.maximum(0, x)

        # 5. Plot ReLU curve
        relu_graph = axes.plot(relu_fn, x_range=[-4, 4], color=YELLOW)
        self.play(Create(relu_graph), run_time=1.5)
        self.wait(0.5)

        # 6. Highlight zero region (negative x)
        zero_region = axes.plot(relu_fn, x_range=[-4, 0], color=BLUE, stroke_width=6)
        self.play(ReplacementTransform(relu_graph.copy(), zero_region), run_time=1)
        self.wait(0.5)

        # 7. Highlight linear growth region (positive x)
        linear_region = axes.plot(relu_fn, x_range=[0, 4], color=GREEN, stroke_width=6)
        self.play(ReplacementTransform(relu_graph.copy(), linear_region), run_time=1)
        self.wait(0.5)

        # 8. Add explanatory text
        text = Text("Simple, efficient, and powerful", font_size=32, color=YELLOW)
        text.next_to(axes, DOWN)
        self.play(Write(text), run_time=1.5)
        self.wait(2)  # pause to make total runtime ≈ 15s

class GaussianFunctionDemo(Scene):
    def construct(self):
        # 1. Title at center
        title = Text("Gaussian Function", font_size=40)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2. Move title to top
        self.play(title.animate.scale(0.7).to_edge(UP), run_time=1)

        # 3. Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-0.5, 1.5, 0.5],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        self.play(Create(axes), run_time=1)

        # 4. Define Gaussian function
        def gaussian_fn(x):
            return np.exp(-x**2)

        # 5. Plot Gaussian curve
        gaussian_graph = axes.plot(gaussian_fn, x_range=[-4, 4], color=YELLOW)
        self.play(Create(gaussian_graph), run_time=1)

        # 6. Highlight main peak around x = 0
        peak_region = axes.plot(gaussian_fn, x_range=[-1, 1], color=GREEN, stroke_width=6)
        self.play(ReplacementTransform(gaussian_graph.copy(), peak_region), run_time=1)

        # 7. Add explanatory text
        text = Text("Great for detecting localized patterns", font_size=32, color=YELLOW)
        text.next_to(axes, DOWN)
        self.play(Write(text), run_time=1.5)
        self.wait(6)  # pause for total runtime ≈ 15s

class NeuralNetworkStackDemo(Scene):
    def construct(self):
        # 1. Title
        title = Text("Power of Stacked Layers", font_size=40)
        self.play(Write(title), run_time=2)
        self.wait(0.5)
        self.play(title.animate.scale(0.7).to_edge(UP), run_time=1.5)
        self.wait(0.5)

        # 2. Draw input layer
        input_text = Text("Input", font_size=30)
        input_text.to_edge(LEFT).shift(UP*0.5)
        self.play(FadeIn(input_text), run_time=1)

        input_nodes = VGroup(*[Circle(radius=0.2, color=BLUE).next_to(input_text, RIGHT, buff=1.0*i) for i in range(2)])
        self.play(FadeIn(input_nodes), run_time=1)

        # 3. Single neuron
        single_neuron = Circle(radius=0.3, color=YELLOW).shift(RIGHT*3)
        neuron_text = Text("Activation", font_size=24).move_to(single_neuron.get_center())
        self.play(FadeIn(single_neuron), Write(neuron_text), run_time=1.5)
        self.wait(0.5)

        # 4. Show arrows (weighted sum)
        arrows = VGroup()
        for node in input_nodes:
            arr = Arrow(start=node.get_right(), end=single_neuron.get_left(), buff=0.05, color=WHITE)
            arrows.add(arr)
        self.play(*[GrowArrow(a) for a in arrows], run_time=2)
        self.wait(0.5)

        # 5. Text: Single neuron bends decision boundary
        single_text = Text("Single neuron: bends boundary once", font_size=28)
        single_text.next_to(single_neuron, DOWN)
        self.play(Write(single_text), run_time=1.5)
        self.wait(1)

        # 6. Introduce multiple layers
        layers_text = Text("Stacking multiple layers", font_size=32).to_edge(LEFT).shift(DOWN*3)
        self.play(Write(layers_text), run_time=1)
        self.wait(0.5)

        # 7. Draw 3 layers of neurons
        layers = VGroup()
        n_neurons_per_layer = [3, 3, 2]
        x_start = 2
        for i, n in enumerate(n_neurons_per_layer):
            layer = VGroup(*[Circle(radius=0.25, color=ORANGE).shift(RIGHT*(x_start + i*2) + UP*(j-1)*1.5) for j in range(n)])
            layers.add(layer)
        self.play(FadeIn(layers), run_time=2)
        self.wait(0.5)

        # 8. Draw arrows between layers
        arrows_layers = VGroup()
        for i in range(len(layers)-1):
            for src in layers[i]:
                for dst in layers[i+1]:
                    arrows_layers.add(Arrow(src.get_right(), dst.get_left(), buff=0.05, color=WHITE))
        self.play(*[GrowArrow(a) for a in arrows_layers], run_time=3)
        self.wait(0.5)

        # 9. Text explanation
        final_text = Text(
            "Each layer applies weighted sum + activation → builds on previous transformations",
            font_size=26
        )
        final_text.next_to(layers, DOWN)
        self.play(Write(final_text), run_time=3)
        self.wait(3)

class RealLifeExamples(Scene):
    def construct(self):
        title = Text("They power real applications", font_size=36, color=YELLOW)
        self.play(Write(title))
        self.wait(3)
        self.play(FadeOut(title))

class SigmoidEmail(Scene):
    def construct(self):
        # 1. Title at top
        title = Text("Sigmoid", font_size=40).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2. Load SVG email icon
        email_icon = SVGMobject("assets/email.svg").scale(0.5).shift(LEFT*5)
        self.play(FadeIn(email_icon), run_time=1)

        # 3. Animate email moving to center (processed by sigmoid)
        target_point = RIGHT*0.001
        self.play(email_icon.animate.move_to(target_point), run_time=2.5)

        # 4. Show probability output
        prob_text = Text("Spam Probability", font_size=30, color=RED)
        prob_text.next_to(email_icon, DOWN*3)
        self.play(Write(prob_text), run_time=1.5)
        self.wait(2)

class OutroTakeaways(Scene):
    def construct(self):
        title = Text("Key Takeaways", font_size=36, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.2)
        takeaways = [
            "• Non-linearity is what gives neural networks their flexibility",
            "• Activation functions shape how data flows through a network",
            "• Stacking in layers allows models to learn even the most complex patterns"
        ]
        tex_objs = VGroup(*[Text(t, font_size=30) for t in takeaways])
        tex_objs.arrange(DOWN, center=True, buff=0.5)
        tex_objs.to_edge(UP*4)

        count = 0
        for obj in tex_objs:
            self.play(FadeIn(obj))
            count += 1
            if count == 2:
                self.wait(8)
            else:    
                self.wait(3)
        self.wait(2)

class OutroNextVideo(Scene):
    def construct(self):
        teaser = Text(
            "Next, we’ll zoom in on the neuron itself", font_size=36, color=ORANGE
        ).move_to(ORIGIN)
        self.play(FadeIn(teaser))
        self.wait(7)

class OutroVisualization(Scene): 
    def construct(self):
       # 2. Input nodes
        input_text = Text("Inputs", font_size=28).to_edge(LEFT).shift(UP*2)
        self.play(FadeIn(input_text), run_time=1)
        input_nodes = VGroup(
            *[Circle(radius=0.25, color=BLUE).next_to(input_text, DOWN, buff=2.5).shift(UP*(i+ 0.5)) for i in range(2)]
        )   
        self.play(FadeIn(input_nodes), run_time=1)

        # 3. Neuron
        neuron = Circle(radius=0.8, color=YELLOW)
        neuron_text = Text("Neuron", font_size=24).move_to(neuron.get_center())
        self.play(FadeIn(neuron), Write(neuron_text), run_time=1.5)

        # 4. Output node
        output_node = Circle(radius=0.25, color=RED).shift(RIGHT*3)
        output_text = Text("Output", font_size=24).next_to(output_node, RIGHT)
        self.play(FadeIn(output_node), Write(output_text), run_time=1.5)

        # 5. Draw weighted arrows from inputs to neuron
        arrows = VGroup()
        for i, node in enumerate(input_nodes):
            arr = Arrow(start=node.get_right(), end=neuron.get_left(), buff=0.05, color=WHITE)
            weight_label = Text(f"W{i+1}", font_size=20).next_to(arr.get_center(), UP*3 if i == 0 else DOWN*3)
            self.add(weight_label)
            arrows.add(arr)
        self.play(*[GrowArrow(a) for a in arrows], run_time=2)
        self.wait(0.5)

        # 6. Show bias node
        bias_node = Circle(radius=0.4, color=GREEN).shift(DOWN*2)
        bias_text = Text("Bias", font_size=20).move_to(bias_node.get_center())
        bias_arrow = Arrow(start=bias_node.get_top(), end=neuron.get_bottom(), color=WHITE)
        self.play(FadeIn(bias_node), Write(bias_text), GrowArrow(bias_arrow), run_time=1.5)
        self.wait(0.5)

        # 7. Show output glowing after neuron computation
        glow = SurroundingRectangle(output_node, color=YELLOW, buff=0.1)
        self.play(FadeIn(glow), run_time=1)
        self.wait(0.5)

        # 8. Add explanation text
        explanation = Text(
            "Inputs × Weights + Bias → Neuron output",
            font_size=18, color=YELLOW
        ).next_to(output_node, UP * 2)
        self.play(Write(explanation), run_time=1.5)
        self.wait(2)

class ReLUComputerVision(Scene):
    def construct(self):
        # 1. Title at top
        title = Text("ReLU in Computer Vision", font_size=40).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2. Load SVG icons
        car_icon = SVGMobject("assets/car_icon.svg").scale(0.7).shift(LEFT*2)
        face_icon = SVGMobject("assets/face_icon.svg").scale(0.7).shift(RIGHT*2)
        self.play(FadeIn(car_icon), FadeIn(face_icon), run_time=2)

        # 3. Add texts below each icon
        car_text = Text("Self-Driving Cars", font_size=28).next_to(car_icon, DOWN*2)
        face_text = Text("Facial Recognition", font_size=28).next_to(face_icon, DOWN*2)
        self.play(Write(car_text), Write(face_text), run_time=1.5)
        self.wait(2)

        # 4. Optional: Highlight both icons to show activation
        car_glow = SurroundingRectangle(car_icon, color=YELLOW, buff=0.1)
        face_glow = SurroundingRectangle(face_icon, color=YELLOW, buff=0.1)
        self.play(FadeIn(car_glow), FadeIn(face_glow), run_time=1)
        self.wait(2)

class TanhSequenceDemo(Scene):
    def construct(self):
        # 1. Title at top
        title = Text("Tanh", font_size=40).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # 2. Create sequence of boxes to represent time steps
        seq_boxes = VGroup(*[Square(side_length=0.7, color=BLUE) for _ in range(5)])
        seq_boxes.arrange(RIGHT, buff=0.5)
        self.play(FadeIn(seq_boxes), run_time=1.5)

        # 3. Add arrows between boxes to indicate sequence
        arrows = VGroup(*[Arrow(seq_boxes[i].get_right(), seq_boxes[i+1].get_left(), buff=0.1) for i in range(4)])
        self.play(*[GrowArrow(a) for a in arrows], run_time=1)

        # 4. Add explanatory text below sequence
        explanation = Text("Zero-centered outputs → helps sequence models learn better", font_size=28, color=YELLOW)
        explanation.next_to(seq_boxes, DOWN*2)
        self.play(Write(explanation), run_time=1.5)
        self.wait(2)

class GaussianActivationDemo(Scene):
    def construct(self):
        # 1. Title at top
        title = Text("Gaussian / Specialized Activations", font_size=36).to_edge(UP)
        self.play(Write(title), run_time=1.5)

        # 2. Create a grid of dots to represent normal patterns
        normal_dots = VGroup(*[Dot(point=np.array([x, y, 0]), color=BLUE) 
                               for x in np.arange(-3, 3, 1) 
                               for y in np.arange(-1, 2, 1)])
        self.play(FadeIn(normal_dots), run_time=2)

        # 3. Highlight one “anomaly” dot in red
        anomaly_dot = Dot(point=np.array([1.5, 1, 0]), color=RED)
        self.play(FadeIn(anomaly_dot), run_time=1)

        # 4. Add explanatory text
        explanation = Text("Used in anomaly detection or pattern matching", font_size=28, color=YELLOW)
        explanation.next_to(normal_dots, DOWN*2)
        self.play(Write(explanation), run_time=1.5)
        self.wait(2) 

class CircularDatasetDemo(Scene):
    def construct(self):
        # 2. Generate circular dataset
        n_points = 40
        radius = 2
        inner_points = [Dot(point=np.array([np.random.uniform(-1, 1)*radius*0.5,
                                           np.random.uniform(-1, 1)*radius*0.5, 0]), color=BLUE) for _ in range(n_points//2)]
        outer_points = [Dot(point=np.array([np.random.uniform(-1, 1)*radius*1.5,
                                           np.random.uniform(-1, 1)*radius*1.5, 0]), color=RED) for _ in range(n_points//2)]
        dataset = VGroup(*inner_points, *outer_points)
        self.play(FadeIn(dataset), run_time=2)
        self.wait(0.5)

        # 3. Single neuron boundary (straight line)
        line_boundary = Line(LEFT*3, RIGHT*3, color=YELLOW)
        boundary_label1 = Text("Single neuron: limited bending → misclassification", font_size=24).shift(DOWN*3.3)
        self.play(Create(line_boundary), Write(boundary_label1), run_time=2)
        self.wait(1.5)

        # 4. First layer: slight curve
        factor_tracker = ValueTracker(0.0)
        def make_boundary_curve(t):
            pts = [np.array([x, np.sin(x*1.5)*t, 0]) for x in np.linspace(-3,3,60)]
            vm = VMobject()
            vm.set_points_smoothly(pts)
            vm.set_color(YELLOW)
            return vm

        boundary_curve1 = always_redraw(lambda: make_boundary_curve(factor_tracker.get_value()))
        self.play(Transform(line_boundary, boundary_curve1), run_time=2)
        self.play(factor_tracker.animate.set_value(0.5), run_time=2)
        self.wait(0.5)

        # 5. Add more layers → boundary adapts
        self.play(factor_tracker.animate.set_value(1.0), run_time=2)
        boundary_label2 = Text("Multiple neurons/layers → boundary adapts", font_size=24).shift(DOWN*3.3)
        self.play(Transform(boundary_label1, boundary_label2), run_time=1)
        self.wait(1)

        # 6. Final smooth boundary perfectly wraps circular dataset
        def final_boundary_curve():
            pts = []
            theta = np.linspace(0, 2*np.pi, 100)
            for t in theta:
                x = radius*np.cos(t)
                y = radius*np.sin(t)
                pts.append(np.array([x,y,0]))
            vm = VMobject()
            vm.set_points_smoothly(pts)
            vm.set_color(GREEN)
            return vm

        boundary_final = always_redraw(final_boundary_curve)
        self.play(Transform(line_boundary, boundary_final), run_time=2)
        self.wait(3)

class NeuralNetworkDepthSummary(Scene):
    def construct(self): 
        # 2. Draw stacked layers of neurons
        layers = VGroup()
        n_neurons_per_layer = [3, 4, 3, 2]  # Example layers
        x_start = -2
        for i, n in enumerate(n_neurons_per_layer):
            layer = VGroup(*[Circle(radius=0.25, color=BLUE).shift(RIGHT*(x_start + i*2) + UP*(j-(n-1)/2)*1.2) for j in range(n)])
            layers.add(layer)
        self.play(FadeIn(layers), run_time=2)

        # 3. Draw arrows between layers
        arrows = VGroup()
        for i in range(len(layers)-1):
            for src in layers[i]:
                for dst in layers[i+1]:
                    arrows.add(Arrow(src.get_right(), dst.get_left(), buff=0.05, color=WHITE, tip_length=0.1))
        self.play(*[GrowArrow(a) for a in arrows], run_time=3)
        self.wait(0.5)

        # 4. Add explanatory texts sequentially
        text1 = Text("Layers give neural networks their depth", font_size=28, color=YELLOW).next_to(layers, DOWN)
        text2 = Text("Depth allows learning patterns beyond simple models", font_size=28, color=YELLOW).next_to(text1, DOWN)
        self.play(Write(text1), run_time=2)
        self.wait(1.5)
        self.play(Write(text2), run_time=2)
        self.wait(2)

        # 5. Optional: Highlight all layers to emphasize depth
        highlights = VGroup(*[SurroundingRectangle(layer, color=GREEN, buff=0.1) for layer in layers])
        self.play(*[FadeIn(h) for h in highlights], run_time=2)
        self.wait(2)

class ActivationDepthDemo(Scene):
    def construct(self):
        # 1. Title
        title = Text("Stacking Layers for Non-Linearity", font_size=36).to_edge(UP)
        self.play(Write(title), run_time=1.5)

        # 2. Circular dataset
        n_points = 30
        inner_points = [Dot(point=0.8*UP*np.random.rand() + 0.8*RIGHT*np.random.rand(), color=BLUE) for _ in range(n_points//2)]
        outer_points = [Dot(point=1.5*UP*np.random.rand() + 1.5*RIGHT*np.random.rand(), color=RED) for _ in range(n_points//2)]
        dataset = VGroup(*inner_points, *outer_points)
        self.play(FadeIn(dataset), run_time=2)

        # 3. Single neuron boundary (slightly bent)
        single_boundary = VMobject()
        single_boundary.set_points_as_corners([LEFT*3 + DOWN, LEFT*1 + UP, RIGHT*3 + UP])
        single_boundary.set_color(YELLOW)
        self.play(Create(single_boundary), run_time=2)
        single_text = Text("Single neuron: limited bending", font_size=24).next_to(single_boundary, DOWN*2)
        self.play(Write(single_text), run_time=1.5)
        self.wait(1)

        # 4. Multiple layers: boundary adapts to dataset
        final_boundary = VMobject()
        theta = np.linspace(0, 2*np.pi, 100)
        pts = [np.array([np.cos(t)*1.2, np.sin(t)*1.2, 0]) for t in theta]
        final_boundary.set_points_smoothly(pts)
        final_boundary.set_color(GREEN)
        self.play(Transform(single_boundary, final_boundary), run_time=2)
        final_text = Text("Multiple layers → flexible decision boundary", font_size=24).next_to(single_boundary, DOWN*2)
        self.play(Transform(single_text, final_text), run_time=1.5)
        self.wait(2)

class NeuronStepAnimation(Scene):
    def construct(self):

        # 2. Input Node
        input_node = Circle(radius=0.3, color=BLUE)
        input_node.shift(LEFT*3)
        input_text = Text("Input x", font_size=24).next_to(input_node, DOWN * 2) 
        self.play(FadeIn(input_node), Write(input_text), run_time=1.5)
        self.wait(0.5)

        # 3. Weighted sum calculation
        sum_node = Circle(radius=0.3, color=ORANGE)
        sum_text = Text("Σ w·x + b", font_size=28).next_to(sum_node, DOWN * 2)
        arrow1 = Arrow(start=input_node.get_right(), end=sum_node.get_left(), buff=0.1)
        self.play(GrowArrow(arrow1), FadeIn(sum_node), Write(sum_text), run_time=2)
        self.wait(0.5)

        # 4. Activation function applied
        act_node = Circle(radius=0.4, color=YELLOW).shift(RIGHT*3)
        act_text = Text("A(z)", font_size=24).move_to(act_node.get_center())
        arrow2 = Arrow(start=sum_node.get_right(), end=act_node.get_left(), buff=0.1)
        self.play(GrowArrow(arrow2), FadeIn(act_node), Write(act_text), run_time=2)
        self.wait(0.5)

        # 5. Output/result passed forward
        output_text = Text("Output → next layer", font_size=24, color=GREEN).next_to(act_node, DOWN * 2)
        self.play(Write(output_text), run_time=1.5)
        self.wait(2)

class LayerStackDemo(Scene):
    def construct(self):
        # 2. Create stacked layers
        layers = VGroup()
        n_neurons_per_layer = [3, 4, 3]  # Example: 3 layers
        layer_spacing = 2  # Horizontal spacing between layers

        # Compute total width for centering
        total_width = (len(n_neurons_per_layer)-1) * layer_spacing
        x_start = -total_width/2  # shift so center is at x=0

        for i, n in enumerate(n_neurons_per_layer):
            layer = VGroup(*[
                Circle(radius=0.25, color=BLUE).shift(RIGHT*(x_start + i*layer_spacing) + UP*(j-(n-1)/2)*0.8)
                for j in range(n)
            ])
            layers.add(layer)

        self.play(FadeIn(layers), run_time=1.5)

        # 3. Draw arrows between layers
        arrows = VGroup()
        for i in range(len(layers)-1):
            for src in layers[i]:
                for dst in layers[i+1]:
                    arrows.add(Arrow(
                        src.get_right(), dst.get_left(),
                        buff=0.05, color=WHITE, tip_length=0.1
                    ))
        self.play(*[GrowArrow(a) for a in arrows], run_time=2)

        # 4. Highlight flow through layers
        highlight = VGroup(*[SurroundingRectangle(layer, color=YELLOW, buff=0.1) for layer in layers])
        self.play(*[FadeIn(h) for h in highlight], run_time=0.7)
        self.wait(1)
