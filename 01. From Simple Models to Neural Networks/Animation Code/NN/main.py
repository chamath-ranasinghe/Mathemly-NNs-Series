from manim import *
import numpy as np

class DecisionBoundary(Scene):
    def construct(self):
        # Axes: Weight (x) vs Height (y)
        axes = Axes(
            x_range=[40, 120, 10],
            y_range=[140, 200, 10],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN)

        x_label = axes.get_x_axis_label("Weight (kg)")
        y_label = axes.get_y_axis_label("Height (cm)")

        title = Text("Group of Patients", font_size=72)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(title.animate.scale(0.6).to_edge(UP), run_time=1)

        self.play(Create(axes.x_axis), Write(x_label))
        self.wait(1)
        self.play(Create(axes.y_axis), Write(y_label))

        # Example data points (weight, height)
        high_risk = [(95, 185), (100, 190), (110, 195), (105, 180)]
        low_risk = [(50, 150), (55, 160), (65, 155), (70, 165)]

        # Plot points
        high_dots = VGroup(*[Dot(axes.c2p(x, y), color=RED) for x, y in high_risk])
        low_dots = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in low_risk])
        
        # Add labels
        high_label = Text("High Risk", color=RED).next_to(high_dots, RIGHT)
        low_label = Text("Low Risk", color=BLUE).next_to(low_dots, RIGHT)

        self.play(FadeIn(high_dots))
        self.play(Write(high_label))
        self.wait(1)

        self.play(FadeIn(low_dots))
        self.play(Write(low_label))
        self.wait(1)

        # Animate decision boundary (model learning)
        # Start with a random line
        final_line = axes.plot(lambda x: -0.3 * x + 200, color=YELLOW)
        start_line = axes.plot(lambda x: 0.5 * x + 135, color=YELLOW)


        self.play(Create(start_line))
        self.wait(1)
        self.play(Transform(start_line, final_line), run_time=3)

        self.wait(10)

class NeuralNetworksIntro(Scene):
    def construct(self):
        # --- Title ---
        title = Text("Neural Networks", font_size=72)
        self.play(FadeIn(title, scale=0.8))
        self.wait(10)
        self.play(FadeOut(title))

        # --- Scatter Plot ---
        axes = Axes(
            x_range=[40, 100, 10],
            y_range=[140, 200, 10],
            axis_config={"include_numbers": True},
        )
        labels = axes.get_axis_labels("Weight", "Height")

        high_risk = [axes.c2p(x, y) for x, y in [(85, 180), (90, 185), (95, 190)]]
        low_risk = [axes.c2p(x, y) for x, y in [(50, 150), (55, 155), (60, 160)]]

        high_dots = VGroup(*[Dot(p, color=RED) for p in high_risk])
        low_dots = VGroup(*[Dot(p, color=BLUE) for p in low_risk])

        # Simple model line
        line = axes.plot(lambda x: 0.5*x + 120, x_range=[40,100], color=YELLOW)
        simple_label = Text("Simple Model", font_size=28, color=YELLOW).next_to(line, UP)

        # Advanced model curve
        curve = axes.plot(lambda x: 0.01*(x-70)**2 + 150, x_range=[40,100], color=GREEN)
        advanced_label = Text("Advanced Model", font_size=28, color=GREEN).next_to(curve, UP)

        # Animate scatter + simple model
        self.play(Create(axes), Write(labels))
        self.play(FadeIn(high_dots), FadeIn(low_dots))
        self.play(Create(line), FadeIn(simple_label))
        self.wait(2)

        # Morph line into curve + change label
        self.play(Transform(line, curve), Transform(simple_label, advanced_label))
        self.wait(2)

        # Fade out plot
        self.play(FadeOut(VGroup(axes, labels, high_dots, low_dots, line, simple_label)))

        # --- Closing text ---
        closing = Text("Let's dive in!", font_size=64)
        self.play(FadeIn(closing, scale=1.2))
        self.wait(1)

class ClassificationIntro(Scene):
    def construct(self):
        # Title
        title = Text("Classification", font_size=72)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(title.animate.scale(0.6).to_edge(UP), run_time=1)

        # Logistic Regression Panel (Left)
        axes_lr = Axes(x_range=[0,10], y_range=[0,10], x_length=4, y_length=4).to_edge(LEFT).shift(DOWN*0.5)
        lr_red = VGroup(*[Dot(axes_lr.c2p(x,y), color=RED) for x,y in [(2,2),(3,3),(2,4)]])
        lr_blue = VGroup(*[Dot(axes_lr.c2p(x,y), color=BLUE) for x,y in [(7,7),(8,6),(6,8)]])
        lr_line = axes_lr.plot(lambda x: x, color=YELLOW)
        lr_label = Text("Logistic Regression", font_size=28).next_to(axes_lr, UP)
        self.play(Create(axes_lr), Write(lr_label))
        self.play(FadeIn(lr_red), FadeIn(lr_blue), Create(lr_line))

        # Perceptron Panel (Right)
        # Input nodes for points
        input_nodes = VGroup(*[Circle(radius=0.15, color=RED).move_to(RIGHT*3 + UP*1.5),
                               Circle(radius=0.15, color=BLUE).move_to(RIGHT*3 + UP*0.5),
                               Circle(radius=0.15, color=RED).move_to(RIGHT*3 + DOWN*0.5),
                               Circle(radius=0.15, color=BLUE).move_to(RIGHT*3 + DOWN*1.5)])
        input_labels = VGroup(*[Text("x1", font_size=20).next_to(input_nodes[0], LEFT),
                                Text("x2", font_size=20).next_to(input_nodes[1], LEFT),
                                Text("x3", font_size=20).next_to(input_nodes[2], LEFT),
                                Text("x4", font_size=20).next_to(input_nodes[3], LEFT)])
        # Neuron
        neuron = Circle(radius=0.3, color=GREEN).move_to(RIGHT*5)
        neuron_label = Text("Perceptron", font_size=24).next_to(neuron, UP)

        # Connections
        connections = VGroup()
        for inp in input_nodes:
            line = Line(inp.get_right(), neuron.get_left(), color=WHITE)
            connections.add(line)

        # Animate Perceptron
        self.play(FadeIn(input_nodes), Write(input_labels))
        self.play(FadeIn(neuron), Write(neuron_label))
        self.play(Create(connections))

        # Optional: animate neuron firing (change color)
        self.play(neuron.animate.set_fill(YELLOW, opacity=0.5), run_time=1)
        self.wait(2)

class DecisionBoundaryIntro(Scene):
    def construct(self):
        # Axes: Weight (x) vs Height (y)
        axes = Axes(
            x_range=[40, 120, 10],
            y_range=[140, 200, 10],
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN)

        x_label = axes.get_x_axis_label("Weight (kg)")
        y_label = axes.get_y_axis_label("Height (cm)")

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Example data points (weight, height)
        high_risk = [(95, 185), (100, 190), (110, 195), (105, 180)]
        low_risk = [(50, 150), (55, 160), (65, 155), (70, 165)]

        # Plot points
        high_dots = VGroup(*[Dot(axes.c2p(x, y), color=RED) for x, y in high_risk])
        low_dots = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in low_risk])

        self.play(FadeIn(high_dots), FadeIn(low_dots))

        # Animate decision boundary (model learning)
        # Start with a random line
        final_line = axes.plot(lambda x: -0.3 * x + 210, color=YELLOW)
        start_line = axes.plot(lambda x: 0.5 * x + 135, color=YELLOW)

        line_label = Text("Decision Boundary", font_size=24, color=YELLOW).next_to(final_line, DOWN)

        self.play(Create(start_line))
        self.wait(1)
        self.play(Transform(start_line, final_line), run_time=3)
        self.play(Write(line_label))

        self.wait(10)

class SimpleAndLinear(Scene):
    def construct(self):
        simple_text = Text("Simple", color=YELLOW_A)
        linear_text = Text("Linearly Separable", color=YELLOW_D).next_to(simple_text, DOWN)

        # Position as a group (optional if you want them centered)
        label_group = VGroup(simple_text, linear_text).arrange(DOWN, center=True).move_to(ORIGIN)

        # Animate one after the other
        self.play(Write(simple_text))
        self.wait(0.5)
        self.play(Write(linear_text))

        self.wait(5) 

class Intuitive(Scene):
    def construct(self):
        simple_text = Text("Intuitive", color=YELLOW_A)
        linear_text = Text("Easy to Visualize", color=YELLOW_D).next_to(simple_text, DOWN)

        # Position as a group (optional if you want them centered)
        label_group = VGroup(simple_text, linear_text).arrange(DOWN, center=True).move_to(ORIGIN)

        # Animate one after the other
        self.play(Write(simple_text))
        self.wait(0.5)
        self.play(Write(linear_text))

        self.wait(5) 

class FeaturesToOutcomes(Scene):
    def construct(self):
        # Feature nodes (left side)
        f1 = Circle(color=BLUE).scale(0.6).shift(LEFT*4 + UP*2)
        f2 = Circle(color=BLUE).scale(0.6).shift(LEFT*4)
        f3 = Circle(color=BLUE).scale(0.6).shift(LEFT*4 + DOWN*2)

        f1_label = Text("Feature 1", font_size=15).move_to(f1.get_center())
        f2_label = Text("Feature 2", font_size=15).move_to(f2.get_center())
        f3_label = Text("Feature 3", font_size=15).move_to(f3.get_center())

        # Outcome node (right side)
        outcome = Circle(color=GREEN).scale(1).shift(RIGHT*4)
        outcome_label = Text("Outcome", font_size=32).move_to(outcome.get_center())

        # Arrows
        arrows = VGroup(
            Arrow(f1.get_right(), outcome.get_left(), buff=0.2, stroke_width=4, color=YELLOW),
            Arrow(f2.get_right(), outcome.get_left(), buff=0.2, stroke_width=4, color=YELLOW),
            Arrow(f3.get_right(), outcome.get_left(), buff=0.2, stroke_width=4, color=YELLOW),
        )

        # Animate appearance
        self.play(Create(f1), Write(f1_label))
        self.play(Create(f2), Write(f2_label))
        self.play(Create(f3), Write(f3_label))
        self.wait(0.2)

        self.play(Create(outcome), Write(outcome_label))
        self.wait(0.2)

        self.play(LaggedStartMap(Create, arrows, lag_ratio=0.2))
        self.wait(0.2)

        self.wait(2)

class SimpleCase(ThreeDScene):
    def construct(self):
        # Simple 2D scatter with linear separation
        axes = Axes(
            x_range=[40, 120, 10],
            y_range=[140, 200, 10],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True},
        ).to_edge(DOWN)

        title = Text("Simple Case").scale(0.7).to_edge(UP)

        # Define raw points
        points_class1_coords = [(50, 150), (60, 160), (55, 170)]
        points_class2_coords = [(90, 180), (100, 190), (85, 175)]

        # Convert to Dots
        points_class1 = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in points_class1_coords])
        points_class2 = VGroup(*[Dot(axes.c2p(x, y), color=RED) for x, y in points_class2_coords])

        # Linear separator line
        line = axes.plot_line_graph(
            x_values=[40, 120],
            y_values=[190, 140],
            add_vertex_dots=False,
            line_color=YELLOW
        )

        # Animations
        self.play(Create(axes), Write(title))
        self.play(FadeIn(points_class1), FadeIn(points_class2))
        self.play(Create(line))
        self.wait(2)

        # Add "misplaced" points that break the line
        extra_points = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in [(95, 155), (70, 145)]]) 

        new_title = Text("Not Always Linearly Separable").scale(0.7).to_edge(UP)

        self.play(FadeIn(extra_points))
        self.play(Transform(title, new_title))
        self.play(line.animate.set_color(GRAY).set_opacity(0.3))  # weaken the line
        self.wait(2)

        # 2D Axes
        axes2d = Axes(
            x_range=[40, 120, 10],
            y_range=[140, 200, 10],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True},
        ).to_edge(DOWN)

        # 2D points
        points2d = VGroup(
            Dot(axes2d.c2p(50, 150), color=BLUE),
            Dot(axes2d.c2p(60, 160), color=BLUE),
            Dot(axes2d.c2p(55, 170), color=BLUE),
            Dot(axes2d.c2p(90, 180), color=RED),
            Dot(axes2d.c2p(100, 190), color=RED),
            Dot(axes2d.c2p(85, 175), color=RED)
        )

        # Show 2D plot
        self.play(Create(axes2d), LaggedStartMap(GrowFromCenter, points2d, lag_ratio=0.2))
        self.wait(1)

        # Fade out 2D axes and points before showing 3D
        self.play(FadeOut(points2d), FadeOut(axes2d), run_time=1.5)

class ComplexCase(ThreeDScene):
    def construct(self):
        title = Text("For Example")
        self.play(FadeIn(title))
        self.wait(2)
        self.play(title.animate.scale(0.6).to_edge(UP), run_time=1)
        # 3D Axes
        axes3d = ThreeDAxes(
            x_range=[40, 120, 20],
            y_range=[140, 200, 20],
            z_range=[20, 80, 10],
            x_length=5, y_length=4, z_length=3
        ).to_edge(DOWN)

        # 3D points
        points3d = VGroup(
            Sphere(radius=0.05, color=BLUE).move_to(axes3d.c2p(50, 150, 30)),
            Sphere(radius=0.05, color=BLUE).move_to(axes3d.c2p(60, 160, 40)),
            Sphere(radius=0.05, color=BLUE).move_to(axes3d.c2p(55, 170, 35)),
            Sphere(radius=0.05, color=RED).move_to(axes3d.c2p(90, 180, 50)),
            Sphere(radius=0.05, color=RED).move_to(axes3d.c2p(100, 190, 60)),
            Sphere(radius=0.05, color=RED).move_to(axes3d.c2p(85, 175, 45))
        )

        # Labels
        x_label = Text("Height").scale(0.3).next_to(axes3d.get_x_axis(), DOWN)
        y_label = Text("Weight").scale(0.3).next_to(axes3d.get_y_axis(), LEFT)
        z_label = Text("Age").scale(0.3).next_to(axes3d.get_z_axis(), OUT)

        self.play(Create(axes3d.x_axis))
        self.play(FadeIn(x_label))
        self.wait(0.5)
        self.play(Create(axes3d.y_axis))
        self.play(FadeIn(y_label))
        self.wait(0.5)
        self.play(Create(axes3d.z_axis))
        self.play(FadeIn(z_label))

        self.play(LaggedStartMap(FadeIn, points3d, lag_ratio=0.2), run_time=2)
        # Rotate camera to show 3D perspective
        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.wait(2)

        # Curved non-linear surface
        surface = Surface(
            lambda u, v: axes3d.c2p(u, v, 40 + 10 * np.sin(u/10) * np.cos(v/20)),
            u_range=[40, 120], v_range=[140, 200],
            resolution=(12, 12),
            fill_opacity=0.4,
            checkerboard_colors=[PURPLE, PURPLE],
        )

        #self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, run_time=2)
        self.play(FadeIn(surface))
        self.wait(3)

class BeyondStraightLines(Scene):
    def construct(self):
        # Step 1: Display question in center
        question_text = Text("How do we go beyond straight lines?", font_size=48)
        self.play(Write(question_text))
        self.wait(1)

        # Step 2: Move text up and transform into simpler title
        title_text = Text("Neural Networks", font_size=48)
        self.play(Transform(question_text, title_text))
        self.wait(0.2)

        # Step 3: Move and scale the transformed text
        self.play(question_text.animate.scale(0.5).to_edge(UP))
        self.wait(0.5)

        # Step 3: Add a sample neural network below
        input_layer = VGroup(*[Circle(radius=0.2, color=BLUE).shift(LEFT*3 + UP*(i-1)) for i in range(3)])
        hidden_layer = VGroup(*[Circle(radius=0.2, color=GREEN).shift(ORIGIN + UP*(i-1)) for i in range(4)])
        output_layer = VGroup(*[Circle(radius=0.2, color=RED).shift(RIGHT*3 + UP*0)])

        # Connections
        connections = VGroup()
        for inp in input_layer:
            for hid in hidden_layer:
                connections.add(Line(inp.get_center(), hid.get_center(), stroke_width=1))
        for hid in hidden_layer:
            for out in output_layer:
                connections.add(Line(hid.get_center(), out.get_center(), stroke_width=1))

        # Animate layers and connections
        self.play(FadeIn(input_layer), FadeIn(hidden_layer), FadeIn(output_layer))
        self.play(LaggedStartMap(Create, connections, lag_ratio=0.05))
        self.wait(1)
        non_linear = Text("Non-linearity", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(non_linear))
        self.wait(5)

class NeuronVisualization(Scene):
    def construct(self):
        # Step 1: Draw the neuron
        neuron = Circle(radius=0.5, color=BLUE).shift(RIGHT)
        neuron_label = Text("Neuron", font_size=18).move_to(neuron.get_center())
        self.play(Create(neuron), Write(neuron_label))
        self.wait(5)

        # Step 2: Add inputs
        inputs = VGroup(
            Dot(LEFT*3 + UP*0.5, color=GREEN),
            Dot(LEFT*3 + DOWN*0.5, color=GREEN)
        )
        input_labels = VGroup(
            Text("x1", font_size=20).next_to(inputs[0], LEFT),
            Text("x2", font_size=20).next_to(inputs[1], LEFT)
        )
        self.play(FadeIn(inputs), Write(input_labels))

        # Step 3: Draw arrows for weights
        weights = VGroup(
            Arrow(inputs[0].get_right(), neuron.get_left(), buff=0.1),
            Arrow(inputs[1].get_right(), neuron.get_left(), buff=0.1)
        )
        weight_labels = VGroup(
            Text("w1", font_size=20).next_to(weights[0].get_center(), UP),
            Text("w2", font_size=20).next_to(weights[1].get_center(), DOWN)
        )
        self.play(LaggedStartMap(Create, weights), Write(weight_labels))

        # Step 4: Add bias
        bias = Text("bias", font_size=20, color=ORANGE).next_to(neuron, DOWN)
        self.play(FadeIn(bias))

        self.wait(3)
        # Step 5: Add activation function curve
        axes = Axes(
            x_range=[-3,3,1],
            y_range=[-1,1,0.5],
            x_length=4, y_length=2
        ).shift(RIGHT*5)
        sigmoid_graph = axes.plot(lambda x: 1/(1+np.exp(-x)), color=YELLOW)
        axes_labels = axes.get_axis_labels(x_label="z", y_label="Activation")
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(sigmoid_graph))

        self.wait(5)

        upcoming = Text("Discussed in upcoming videos", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(upcoming))
        self.wait(5)

class OutroTakeaways(Scene):
    def construct(self):
        title = Text("Key Takeaways", font_size=36, color=YELLOW).to_edge(UP)
        self.play(FadeIn(title), run_time=0.2)
        takeaways = [
            "• Journey from simple linear models to neural networks",
            "• Linear models struggle with complex, non-linear data",
            "• Neural networks provide a flexible, powerful solution"
        ]
        tex_objs = VGroup(*[Text(t, font_size=30) for t in takeaways])
        tex_objs.arrange(DOWN, center=True, buff=0.5)
        tex_objs.to_edge(UP*4)

        for obj in tex_objs:
            self.play(FadeIn(obj))
            self.wait(3)
        self.wait(1)

class OutroComparison(Scene):
    def construct(self):
        # Left: Linear model
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=3, y_length=3
        ).to_edge(LEFT, buff=1)
        points_linear = VGroup(
            Dot(axes.c2p(2, 3), color=BLUE),
            Dot(axes.c2p(3, 2), color=BLUE),
            Dot(axes.c2p(7, 8), color=RED),
            Dot(axes.c2p(8, 7), color=RED)
        )
        line = axes.plot_line_graph(x_values=[0,10], y_values=[0,10], add_vertex_dots=False, line_color=YELLOW)

        # Right: Neural network
        input_layer = VGroup(*[Circle(radius=0.15, color=BLUE).shift(RIGHT*2 + UP*(i-0.5)) for i in range(2)])
        hidden_layer = VGroup(*[Circle(radius=0.15, color=GREEN).shift(RIGHT*3 + UP*(i-0.5)) for i in range(3)])
        output_layer = Circle(radius=0.15, color=RED).shift(RIGHT*4 + UP*0)
        connections = VGroup()
        for inp in input_layer:
            for hid in hidden_layer:
                connections.add(Line(inp.get_center(), hid.get_center()))
        for hid in hidden_layer:
            connections.add(Line(hid.get_center(), output_layer.get_center()))

        # Play animations
        self.play(Create(axes), FadeIn(points_linear), Create(line))
        self.wait(1)
        self.play(FadeIn(input_layer), FadeIn(hidden_layer), FadeIn(output_layer))
        self.play(LaggedStartMap(Create, connections, lag_ratio=0.1))
        self.wait(2)

class OutroNextVideo(Scene):
    def construct(self):
        teaser = Text(
            "Next, we'll explore hidden layers, neurons,\n"
            "and activation functions!", font_size=36, color=ORANGE
        ).move_to(ORIGIN)
        self.play(FadeIn(teaser))
        self.wait(7)

class CircularPattern(Scene):
    def construct(self):
        # --- Part 1: Circular pattern data ---
        inner_points = VGroup(*[
            Dot([0.3*np.cos(a) + 0.2*np.random.randn(),
                 0.3*np.sin(a) + 0.2*np.random.randn(), 0], 
                 color=BLUE)
            for a in np.linspace(0, 2*np.pi, 20)
        ])

        # Outer cluster (red, noisy ring)
        outer_points = VGroup(*[
            Dot([1.5*np.cos(a) + 0.3*np.random.randn(),
                 1.5*np.sin(a) + 0.3*np.random.randn(), 0], 
                 color=RED)
            for a in np.linspace(0, 2*np.pi, 40)
        ])

        self.play(FadeIn(inner_points), FadeIn(outer_points))
        self.wait(5)

        # Animate wrong straight lines trying to separate
        lines = VGroup(
            Line([-2, -1, 0], [2, 1, 0], color=YELLOW),
            Line([-2, 1, 0], [2, -1, 0], color=YELLOW),
            Line([0, -2, 0], [0, 2, 0], color=YELLOW)
        )

        for line in lines:
            self.play(Create(line), run_time=1)
            self.wait(1)
            self.play(FadeOut(line))

        # --- Part 2: Text + cross-out ---
        lr_text = Text("Logistic Regression", font_size=36).shift(UP*2)
        perceptron_text = Text("Perceptron", font_size=36).shift(DOWN*2)

        self.play(Write(lr_text), Write(perceptron_text), run_time=2)
        self.wait(1)

        # Red slash to cross them out
        lr_cross = Line(lr_text.get_corner(UL), lr_text.get_corner(DR), color=RED, stroke_width=6)
        perc_cross = Line(perceptron_text.get_corner(UL), perceptron_text.get_corner(DR), color=RED, stroke_width=6)

        self.play(Create(lr_cross), run_time=0.5)
        self.play(Create(perc_cross), run_time=0.5)
        self.wait(2)

class NonLinear3D(ThreeDScene):
    def construct(self):
        # Axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )

        labels = axes.get_axis_labels(x_label="x", y_label="y", z_label="z")
        self.play(Create(axes), Write(labels))

        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES)

        # Define nonlinear clusters
        np.random.seed(1)
        inner_points = np.random.randn(20, 3) * 0.5   # cluster near origin
        outer_points = np.array([
            [2*np.cos(a) + 0.3*np.random.randn(),
             2*np.sin(a) + 0.3*np.random.randn(),
             np.sin(2*a) + 0.3*np.random.randn()]
            for a in np.linspace(0, 2*np.pi, 30)
        ])

        # Convert to Dots
        inner_group = VGroup(*[Dot3D(point, color=BLUE, radius=0.05) for point in inner_points])
        outer_group = VGroup(*[Dot3D(point, color=RED, radius=0.05) for point in outer_points])

        self.play(LaggedStartMap(FadeIn, inner_group, lag_ratio=0.1, run_time=2))
        self.play(LaggedStartMap(FadeIn, outer_group, lag_ratio=0.1, run_time=2))
        self.wait(1)

        # Add linear plane (starts flat)
        plane = Surface(
            lambda u, v: axes.c2p(u, v, 0),  # z = 0
            u_range=[-3, 3],
            v_range=[-3, 3],
            fill_opacity=0.3,
            checkerboard_colors=[YELLOW, YELLOW]
        )

        self.play(Create(plane), run_time=2)
        self.wait(1)

        # Try moving/tilting plane to separate (but fail)
        self.play(plane.animate.shift(OUT*1.5), run_time=2)
        self.play(Rotate(plane, angle=PI/4, axis=RIGHT), run_time=2)
        self.play(Rotate(plane, angle=PI/4, axis=OUT), run_time=2)
        self.wait(3)

class NonLinearBoundary(Scene):
    def construct(self):
        # Generate data points in circular halves
        np.random.seed(1)
        n_points = 600
        radius = 3
        
        # Define wavy boundary function
        def boundary(x):
            return 0.7 * np.sin(1.5 * x)

        blue_points, orange_points = [], []
        while len(blue_points) + len(orange_points) < n_points:
            x, y = np.random.uniform(-radius, radius, 2)
            if x**2 + y**2 <= radius**2:  # inside circle
                if y < boundary(x):
                    blue_points.append([x, y, 0])
                else:
                    orange_points.append([x, y, 0])
        
        blue_dots = VGroup(*[Dot(point, radius=0.04, color=BLUE) for point in blue_points])
        orange_dots = VGroup(*[Dot(point, radius=0.04, color=ORANGE) for point in orange_points])

        # Add data points
        self.play(FadeIn(blue_dots), FadeIn(orange_dots))
        self.wait(1)

        # Straight line attempt (bad separator)
        straight_line = Line([-3.5, 0, 0], [3.5, 0, 0], color=RED, stroke_width=6)
        self.play(Create(straight_line))
        self.wait(1)

        # Wavy boundary that actually separates the groups
        def wavy_function(x):
            return 0.7 * np.sin(1.5 * x)  # adjust amplitude & frequency for nice curve

        wavy_points = [
            [x, wavy_function(x), 0]
            for x in np.linspace(-3.5, 3.5, 100)
        ]
        
        wavy_curve = VMobject(color=RED, stroke_width=6)
        wavy_curve.set_points_smoothly(wavy_points)

        # Animate transformation to wavy separator
        self.play(Transform(straight_line, wavy_curve))
        self.wait(2)

class CurvedGlassLayers(ThreeDScene):
    def construct(self):
        # --- Step 0: 3D Axes ---
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )
        self.set_camera_orientation(phi=70 * DEGREES, theta=40 * DEGREES)
        self.play(Create(axes), run_time=2)

        # --- Step 1: Non-linear data points ---
        np.random.seed(2)
        # Inner cluster
        inner = np.random.randn(20, 3) * 0.5
        # Outer cluster (non-linear)
        outer = np.array([
            [2*np.cos(a) + 0.2*np.random.randn(),
             2*np.sin(a) + 0.2*np.random.randn(),
             np.sin(2*a) + 0.2*np.random.randn()]
            for a in np.linspace(0, 2*np.pi, 30)
        ])

        inner_dots = VGroup(*[Dot3D(pt, color=BLUE, radius=0.05) for pt in inner])
        outer_dots = VGroup(*[Dot3D(pt, color=RED, radius=0.05) for pt in outer])

        self.play(LaggedStartMap(FadeIn, inner_dots, lag_ratio=0.05), 
                  LaggedStartMap(FadeIn, outer_dots, lag_ratio=0.05), run_time=3)
        self.wait(1)

        # --- Step 2: Flat plane (linear model) ---
        plane = Surface(
            lambda u, v: axes.c2p(u, v, 0),
            u_range=[-3, 3],
            v_range=[-3, 3],
            checkerboard_colors=[YELLOW, YELLOW],
            fill_opacity=0.3,
        )
        self.play(Create(plane), run_time=2)
        self.wait(1)

        # --- Step 3: Curved layers sequentially replacing each other ---
        curved1 = Surface(
            lambda u, v: axes.c2p(u, v, 0.3*np.sin(u)*np.cos(v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            fill_opacity=0.25,
            checkerboard_colors=[GREEN, GREEN],
        )
        curved2 = Surface(
            lambda u, v: axes.c2p(u, v, 0.5*np.sin(u+v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            fill_opacity=0.25,
            checkerboard_colors=[TEAL, TEAL],
        )
        curved3 = Surface(
            lambda u, v: axes.c2p(u, v, 0.7*np.cos(u)*np.sin(v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            fill_opacity=0.25,
            checkerboard_colors=[PURPLE, PURPLE],
        )

        # Step 3a: Replace flat plane with first curve
        self.play(ReplacementTransform(plane, curved1), run_time=3)
        self.wait(0.5)

        # Step 3b: Replace first curve with second curve
        self.play(ReplacementTransform(curved1, curved2), run_time=3)
        self.wait(0.5)

        # Step 3c: Replace second curve with third curve
        self.play(ReplacementTransform(curved2, curved3), run_time=3)
        self.wait(0.5)

        # Hold final view
        self.wait(5)

class NeuralNetworkLayers(Scene):
    def construct(self):
        # --- Step 1: Parameters ---
        layer_distance = 1.5  # horizontal distance between layers
        neuron_radius = 0.15
        layers_neurons = [3, 4, 5]  # number of neurons in each layer
        colors = [BLUE, GREEN, PURPLE]

        network_layers = VGroup()
        edges_group = VGroup()

        # --- Step 2: Create layers offscreen (initially invisible) ---
        for i, n_neurons in enumerate(layers_neurons):
            layer = VGroup(*[
                Circle(radius=neuron_radius, color=colors[i], fill_opacity=1).shift(
                    RIGHT * i * layer_distance + UP * (j - (n_neurons-1)/2) * 0.7
                ) for j in range(n_neurons)
            ])
            network_layers.add(layer)

        # --- Step 3: Add first layer ---
        self.play(FadeIn(network_layers[0]))
        self.wait(0.5)

        # --- Step 4: Sequentially add layers and edges ---
        for i in range(1, len(network_layers)):
            # Fade in new layer
            self.play(FadeIn(network_layers[i]), run_time=2)

            # Connect previous layer to this layer
            edges = VGroup()
            for prev_neuron in network_layers[i-1]:
                for curr_neuron in network_layers[i]:
                    edge = Line(prev_neuron.get_center(), curr_neuron.get_center(), stroke_width=2, color=WHITE)
                    edges.add(edge)
            edges_group.add(edges)
            self.play(Create(edges), run_time=2)
            self.wait(0.5)

        self.wait(7)

class NeuralNetworkCircularBoundary(Scene):
    def construct(self):
        np.random.seed(4)
        # --- Data points ---
        inner_points = VGroup(*[
            Dot([0.3*np.cos(a) + 0.2*np.random.randn(),
                 0.3*np.sin(a) + 0.2*np.random.randn(), 0], 
                 color=BLUE)
            for a in np.linspace(0, 2*np.pi, 20)
        ])

        outer_points = VGroup(*[
            Dot([1.5*np.cos(a) + 0.3*np.random.randn(),
                 1.5*np.sin(a) + 0.3*np.random.randn(), 0], 
                 color=RED)
            for a in np.linspace(0, 2*np.pi, 40)
        ])

        self.play(LaggedStartMap(FadeIn, inner_points, lag_ratio=0.05),
                  LaggedStartMap(FadeIn, outer_points, lag_ratio=0.03), run_time=3)
        self.wait(0.5)

        # --- Step 1: Linear line (starting point) ---
        line = Line([-2, 0, 0], [2, 0, 0], color=YELLOW, stroke_width=3)
        self.play(Create(line), run_time=1.5)
        self.wait(0.5)

        # --- Step 2: Morph line into a curved boundary ---
        # Create a circular boundary shape
        boundary_curve = VMobject()
        boundary_curve.set_points_as_corners([
            np.array([0.7*np.cos(a), 0.7*np.sin(a), 0]) for a in np.linspace(0, 2*np.pi, 50)
        ])
        boundary_curve.set_color(GREEN)
        boundary_curve.set_stroke(width=3)

        # Animate line transforming into the circular-like curve
        self.play(Transform(line, boundary_curve), run_time=6)
        self.wait(1)

        # --- Step 3: Emphasize the neural network effect ---
        caption = Text(
            "Neural networks can create flexible, curved boundaries,\n"
            "perfectly separating complex data.",
            font_size=24
        ).next_to(boundary_curve, DOWN * 6)
        self.play(Write(caption))
        self.wait(4)

class NeuralNetworkPower(Scene):
    def construct(self):
        # --- Step 0: Title ---
        title = Text("Neural Networks: Beyond Linear Models", font_size=36).to_edge(UP)
        self.play(Write(title))

        # --- Step 1: Create stacked layers of neurons ---
        layers_neurons = [3, 4, 5]  # neurons per layer
        layer_distance = 1.5
        neuron_radius = 0.15
        colors = [BLUE, GREEN, PURPLE]

        network_layers = VGroup()
        edges_group = VGroup()

        total_width = (len(layers_neurons) - 1) * layer_distance
        for i, n_neurons in enumerate(layers_neurons):
            layer = VGroup(*[
                Circle(radius=neuron_radius, color=colors[i], fill_opacity=1).shift(
                    RIGHT * (i * layer_distance - total_width/2) + UP * (j - (n_neurons-1)/2) * 0.7
                )
                for j in range(n_neurons)
            ])
            network_layers.add(layer)

        # Animate layers appearing sequentially
        for i, layer in enumerate(network_layers):
            self.play(FadeIn(layer), run_time=0.5)
            # Connect edges to previous layer
            if i > 0:
                edges = VGroup(*[
                    Line(prev.get_center(), curr.get_center(), stroke_width=2, color=WHITE)
                    for prev in network_layers[i-1] for curr in layer
                ])
                edges_group.add(edges)
                self.play(Create(edges), run_time=0.5)
        self.wait(0.5)

        # --- Step 2: Highlight non-linear activations ---
        glow_arcs = VGroup()
        for layer in network_layers[1:]:  # skip input layer
            for neuron in layer:
                arc = Arc(radius=0.25, start_angle=PI/2, angle=PI, color=YELLOW).move_to(neuron.get_center())
                glow_arcs.add(arc)
        self.play(LaggedStartMap(Create, glow_arcs, lag_ratio=0.1), run_time=1)
        self.wait(0.5)

        caption1 = Text(
            "Stacking layers and adding non-linear activations\n"
            "lets neural networks go far beyond linear models",
            font_size=24
        ).next_to(network_layers, DOWN)
        self.play(Write(caption1))
        self.wait(1)

        # --- Step 3: Show applications (8-18s) ---
        self.play(FadeOut(caption1))

        apps = ["Vision", "Language", "Medicine", "AI Everywhere"]
        app_texts = VGroup(*[Text(app, font_size=28, color=ORANGE) for app in apps])

        positions = [UP*2 + LEFT*3, UP*2 + RIGHT*3, DOWN*2 + LEFT*2, DOWN*2 + RIGHT*2]
        for txt, pos in zip(app_texts, positions):
            txt.move_to(pos)

        self.play(LaggedStartMap(FadeIn, app_texts, lag_ratio=0.5), run_time=4)

        caption2 = Text(
            "This is what makes them so powerful\nfor modern AI applications",
            font_size=24
        ).next_to(app_texts, DOWN)
        self.play(Write(caption2))
        self.wait(3)

class VoiceAssistantNN(Scene):
    def construct(self):
        # --- Step 1: Voice assistant icon ---
        assistant_icon = SVGMobject("assets/smartphone_icon.svg")  # Replace with your icon
        assistant_icon.scale(1).to_edge(LEFT, buff=2)
        self.play(FadeIn(assistant_icon), run_time=0.5)

        # --- Step 2: Text label ---
        label = Text("Voice Assistants", font_size=36).next_to(assistant_icon, UP)
        self.play(Write(label), run_time = 0.5)

        # --- Step 3: Sound waves ---
        waves = VGroup(*[
            Arc(radius=r, start_angle=-PI/2, angle=PI, color=BLUE)
            for r in [0.5, 0.7, 0.9]
        ])
        waves.arrange(RIGHT, buff=0.2).next_to(assistant_icon, RIGHT, buff=0.5)

        self.play(LaggedStartMap(Create, waves, lag_ratio=0.3))
        
        # --- Step 4: Neural network ---
        layers_neurons = [2, 3, 2]
        layer_distance = 1.5
        neuron_radius = 0.15
        colors = [GREEN, ORANGE, PURPLE]
        total_width = (len(layers_neurons)-1)*layer_distance
        network_layers = VGroup()
        
        for i, n_neurons in enumerate(layers_neurons):
            layer = VGroup(*[
                Circle(radius=neuron_radius, color=colors[i], fill_opacity=1).shift(
                    RIGHT*(i*layer_distance - total_width/2) + UP*(j-(n_neurons-1)/2)*0.7
                )
                for j in range(n_neurons)
            ])
            network_layers.add(layer)
        
        # Connect edges
        edges_group = VGroup()
        for i in range(1, len(network_layers)):
            edges = VGroup(*[
                Line(prev.get_center(), curr.get_center(), stroke_width=2, color=WHITE)
                for prev in network_layers[i-1] for curr in network_layers[i]
            ])
            edges_group.add(edges)
        
        # Position network on the right
        network_layers.move_to(RIGHT*3)
        edges_group.move_to(RIGHT*3)
        
        self.play(LaggedStartMap(FadeIn, network_layers, lag_ratio=0.3))
        self.play(LaggedStartMap(Create, edges_group, lag_ratio=0.2), run_time = 1)
        
        # --- Step 5: Glow activations ---
        glow_arcs = VGroup()
        for layer in network_layers[1:]:
            for neuron in layer:
                arc = Arc(radius=0.25, start_angle=PI/2, angle=PI, color=YELLOW).move_to(neuron.get_center())
                glow_arcs.add(arc)
        self.play(LaggedStartMap(Create, glow_arcs, lag_ratio=0.1))

        spoken = Text("Spoken language", font_size=24)
        accents = Text("Recognize accents", font_size=24)
        context = Text("Pick up context from conversations", font_size=24)

        # Group them together
        labels = VGroup(spoken, accents, context)

        # Arrange vertically
        labels.arrange(DOWN, buff=0.3)

        # Move the group to the bottom center
        labels.to_edge(DOWN, buff=0.5)  # buff adds some space from the bottom edge

        # Animate them
        self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.5))
        self.wait(2)

class ImageRecognitionDemo(Scene):
    def construct(self):
        # --- Step 1: Title ---
        title = Text("Image Recognition", font_size=36).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # --- Step 2: Icons and labels ---
        icons = [
            ("assets/face_icon.svg", "Facial Recognition"),
            ("assets/medical_icon.svg", "Medical Scans"),
            ("assets/car_icon.svg", "Self-Driving Cars")
        ]

        icon_objects = VGroup()
        labels = VGroup()
        positions = [LEFT*4, ORIGIN, RIGHT*4]

        for (icon_path, label_text), pos in zip(icons, positions):
            icon = SVGMobject(icon_path).scale(1).move_to(pos + DOWN*0.5)
            text = Text(label_text, font_size=24).next_to(icon, DOWN, buff=0.3)
            icon_objects.add(icon)
            labels.add(text)

        self.play(LaggedStartMap(FadeIn, icon_objects, lag_ratio=0.3, run_time=3))
        self.play(LaggedStartMap(Write, labels, lag_ratio=0.3, run_time=2))
        self.wait(1)

        # --- Step 3: Show neural network connection ---
        # Mini neural network diagram
        layers_neurons = [2, 3, 2]
        layer_distance = 1.2
        neuron_radius = 0.12
        colors = [GREEN, ORANGE, PURPLE]
        total_width = (len(layers_neurons)-1)*layer_distance

        network_layers = VGroup()
        edges_group = VGroup()

        for i, n_neurons in enumerate(layers_neurons):
            layer = VGroup(*[
                Circle(radius=neuron_radius, color=colors[i], fill_opacity=1).shift(
                    RIGHT*(i*layer_distance - total_width/2) + UP*(j-(n_neurons-1)/2)*0.5
                )
                for j in range(n_neurons)
            ])
            network_layers.add(layer)

        # Connect edges
        for i in range(1, len(network_layers)):
            edges = VGroup(*[
                Line(prev.get_center(), curr.get_center(), stroke_width=2, color=WHITE)
                for prev in network_layers[i-1] for curr in network_layers[i]
            ])
            edges_group.add(edges)

        # Position network above icons
        network_layers.move_to(UP*1.5)
        edges_group.move_to(UP*1.5)

        self.play(LaggedStartMap(FadeIn, network_layers, lag_ratio=0.2, run_time=2))
        self.play(LaggedStartMap(Create, edges_group, lag_ratio=0.2, run_time=2))

        # --- Step 4: Caption ---
        caption = Text(
            "Linear models fail for complex patterns.\nNeural networks handle non-linear image data",
            font_size=20
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(caption))
        self.wait(3)

        # --- Step 5: Emphasize neural network activation ---
        glow_arcs = VGroup()
        for layer in network_layers[1:]:
            for neuron in layer:
                arc = Arc(radius=0.2, start_angle=PI/2, angle=PI, color=YELLOW).move_to(neuron.get_center())
                glow_arcs.add(arc)

        self.play(LaggedStartMap(Create, glow_arcs, lag_ratio=0.1, run_time=2))
        self.wait(2)

class RecommendationSystems(Scene):
    def construct(self):
        # --- Step 1: Title ---
        title = Text("Recommendation Systems", font_size=36).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # --- Step 2: Icons for Netflix and Amazon ---
        icons = [
            ("assets/netflix_icon.svg", "Netflix"),
            ("assets/amazon_icon.svg", "Amazon")
        ]

        icon_objects = VGroup()
        labels = VGroup()
        positions = [LEFT*2, RIGHT*2]

        for (icon_path, label_text), pos in zip(icons, positions):
            icon = SVGMobject(icon_path).scale(1).move_to(pos + DOWN*0.5)
            text = Text(label_text, font_size=24).next_to(icon, DOWN, buff=0.3)
            icon_objects.add(icon)
            labels.add(text)

        self.play(LaggedStartMap(FadeIn, icon_objects, lag_ratio=0.3, run_time=2))
        self.play(LaggedStartMap(Write, labels, lag_ratio=0.3, run_time=1.5))
        self.wait(0.5)

        # --- Step 3: Neural network ---
        layers_neurons = [2, 3, 2]
        layer_distance = 1.2
        neuron_radius = 0.12
        colors = [GREEN, ORANGE, PURPLE]
        total_width = (len(layers_neurons)-1)*layer_distance

        network_layers = VGroup()
        edges_group = VGroup()

        for i, n_neurons in enumerate(layers_neurons):
            layer = VGroup(*[
                Circle(radius=neuron_radius, color=colors[i], fill_opacity=1).shift(
                    RIGHT*(i*layer_distance - total_width/2) + UP*(j-(n_neurons-1)/2)*0.5
                )
                for j in range(n_neurons)
            ])
            network_layers.add(layer)

        # Connect edges
        for i in range(1, len(network_layers)):
            edges = VGroup(*[
                Line(prev.get_center(), curr.get_center(), stroke_width=2, color=WHITE)
                for prev in network_layers[i-1] for curr in network_layers[i]
            ])
            edges_group.add(edges)

        # Position network above icons
        network_layers.move_to(UP*1.5)
        edges_group.move_to(UP*1.5)

        self.play(LaggedStartMap(FadeIn, network_layers, lag_ratio=0.2, run_time=1.5))
        self.play(LaggedStartMap(Create, edges_group, lag_ratio=0.2, run_time=1.5))

        # --- Step 4: Glow activations for pattern detection ---
        glow_arcs = VGroup()
        for layer in network_layers[1:]:
            for neuron in layer:
                arc = Arc(radius=0.2, start_angle=PI/2, angle=PI, color=YELLOW).move_to(neuron.get_center())
                glow_arcs.add(arc)
        self.play(LaggedStartMap(Create, glow_arcs, lag_ratio=0.1, run_time=2))

        # --- Step 5: Caption ---
        caption = Text(
            "Neural networks analyze millions of data points\nand detect subtle patterns in your behavior",
            font_size=20
            
        ).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(2)

class NeuralNetworkSummary(Scene):
    def construct(self):
        # Key points only
        key_points = [
            "Neural networks",
            "aren’t just “better models”",
            "handle complex real-world data",
            "deliver accurate, meaningful predictions"
        ]

        # Create Text objects
        texts = VGroup(*[Text(p, font_size=36, color=WHITE) for p in key_points])
        texts.arrange(DOWN, center=True, buff=0.8)

        # Animate key points one by one
        for text in texts:
            self.play(FadeIn(text, shift=DOWN), run_time=1.5)
            self.wait(0.5)

        # Optional: highlight each key point briefly
        for text in texts:
            self.play(text.animate.set_color(YELLOW), run_time=0.5)
            self.wait(0.3)
            self.play(text.animate.set_color(WHITE), run_time=0.3)

        self.wait(1)

class RealWorld(Scene):
    def construct(self):
        # Step 1: Display question in center
        text = Text("Real World Examples", font_size=48)
        self.play(Write(text))
        self.wait(9)