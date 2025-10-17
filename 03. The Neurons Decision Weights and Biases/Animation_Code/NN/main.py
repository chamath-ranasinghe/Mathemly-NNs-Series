from manim import *
import numpy as np

class NeuronLinearBehavior(Scene):
    def construct(self):
        # Title
        title = Text("A Neuron Behaves Like Linear Regression", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Show the equation
        equation = MathTex(
            "z", "=", "w_1", "x_1", "+", "w_2", "x_2", "+", "b"
        ).scale(1)
        equation.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(equation))
        self.wait(2)
        
        # Create visual representation of inputs and neuron
        neuron_group = VGroup()
        
        # Input nodes
        x1 = Circle(radius=0.3, color=BLUE, fill_opacity=0.7)
        x1_label = MathTex("x_1", color=WHITE).scale(0.8).move_to(x1)
        x1_group = VGroup(x1, x1_label).shift(LEFT * 4 + UP * 1)
        
        x2 = Circle(radius=0.3, color=BLUE, fill_opacity=0.7)
        x2_label = MathTex("x_2", color=WHITE).scale(0.8).move_to(x2)
        x2_group = VGroup(x2, x2_label).shift(LEFT * 4 + DOWN * 1)
        
        # Neuron
        neuron = Circle(radius=0.5, color=YELLOW, fill_opacity=0.8)
        neuron_label = MathTex("z", color=BLACK).scale(1.2).move_to(neuron)
        neuron_group_main = VGroup(neuron, neuron_label).shift(RIGHT * 1)
        
        # Weight connections
        w1_arrow = Arrow(x1.get_right(), neuron.get_left() + UP*0.3, buff=0.1, color=GREEN)
        w1_label = MathTex("w_1", color=GREEN).scale(0.7).next_to(w1_arrow, UP, buff=0.1)
        
        w2_arrow = Arrow(x2.get_right(), neuron.get_left() + DOWN*0.3, buff=0.1, color=RED)
        w2_label = MathTex("w_2", color=RED).scale(0.7).next_to(w2_arrow, DOWN, buff=0.1)
        
        # Bias
        bias_arrow = Arrow(neuron.get_top() + UP*0.5, neuron.get_top(), buff=0.1, color=PURPLE)
        bias_label = MathTex("b", color=PURPLE).scale(0.7).next_to(bias_arrow, UP, buff=0.1)
        
        network_viz = VGroup(
            x1_group, x2_group, neuron_group_main,
            w1_arrow, w1_label, w2_arrow, w2_label,
            bias_arrow, bias_label
        )
        network_viz.shift(DOWN * 0.75)
        network_viz.shift(RIGHT * 0.5)
        
        self.play(
            FadeIn(x1_group),
            FadeIn(x2_group),
            FadeIn(neuron_group_main)
        )
        self.play(
            GrowArrow(w1_arrow), Write(w1_label),
            GrowArrow(w2_arrow), Write(w2_label),
            GrowArrow(bias_arrow), Write(bias_label)
        )
        self.wait(2)
        
        # Scenario 1: Both weights positive
        scenario1 = Text("Both weights positive → Output increases", font_size=24, color=GREEN)
        scenario1.next_to(equation, DOWN, buff=0.5)
        
        self.play(FadeIn(scenario1))
        
        # Animate increasing inputs
        x1_value = DecimalNumber(0, num_decimal_places=1, color=BLUE).scale(0.6)
        x1_value.next_to(x1_group, LEFT, buff=0.3)
        x2_value = DecimalNumber(0, num_decimal_places=1, color=BLUE).scale(0.6)
        x2_value.next_to(x2_group, LEFT, buff=0.3)
        z_value = DecimalNumber(0, num_decimal_places=1, color=YELLOW).scale(0.6)
        z_value.next_to(neuron_group_main, RIGHT, buff=0.3)
        
        self.play(
            FadeIn(x1_value),
            FadeIn(x2_value),
            FadeIn(z_value)
        )
        
        # Simulate w1=2, w2=1.5, b=0.5
        for i in range(1, 6):
            x1_val = i * 0.5
            x2_val = i * 0.5
            z_val = 2 * x1_val + 1.5 * x2_val + 0.5
            
            self.play(
                x1_value.animate.set_value(x1_val),
                x2_value.animate.set_value(x2_val),
                z_value.animate.set_value(z_val),
                x1.animate.set_fill(BLUE, opacity=0.3 + i*0.14),
                x2.animate.set_fill(BLUE, opacity=0.3 + i*0.14),
                neuron.animate.set_fill(YELLOW, opacity=0.4 + i*0.12),
                run_time=0.5
            )
        self.wait(1)
        
        # Reset for scenario 2
        self.play(
            FadeOut(scenario1),
            x1_value.animate.set_value(0),
            x2_value.animate.set_value(0),
            z_value.animate.set_value(0),
            x1.animate.set_fill(BLUE, opacity=0.7),
            x2.animate.set_fill(BLUE, opacity=0.7),
            neuron.animate.set_fill(YELLOW, opacity=0.8)
        )
        
        # Scenario 2: One weight negative
        scenario2 = Text("One weight negative → Opposite direction", font_size=24, color=RED)
        scenario2.next_to(equation, DOWN, buff=0.5)
        
        self.play(
            FadeIn(scenario2),
            w2_label.animate.set_color(ORANGE),
            w2_arrow.animate.set_color(ORANGE)
        )
        
        # Simulate w1=2, w2=-1.5, b=0.5
        for i in range(1, 6):
            x1_val = i * 0.5
            x2_val = i * 0.5
            z_val = 2 * x1_val - 3 * x2_val + 0.5
            
            self.play(
                x1_value.animate.set_value(x1_val),
                x2_value.animate.set_value(x2_val),
                z_value.animate.set_value(z_val),
                x1.animate.set_fill(BLUE, opacity=0.3 + i*0.14),
                x2.animate.set_fill(BLUE, opacity=0.3 + i*0.14),
                neuron.animate.set_fill(YELLOW, opacity=0.5 + min(0.3, (2-z_val)*0.1)),
                run_time=0.5
            )
        self.wait(1)
        
        # Reset values
        self.play(
            FadeOut(scenario2),
            x1_value.animate.set_value(1),
            x2_value.animate.set_value(1),
            z_value.animate.set_value(1),
            x1.animate.set_fill(BLUE, opacity=0.7),
            x2.animate.set_fill(BLUE, opacity=0.7),
            neuron.animate.set_fill(YELLOW, opacity=0.8)
        )
        
        # Scenario 3: Changing bias
        scenario3 = Text("Changing bias shifts output up or down", font_size=24, color=PURPLE)
        scenario3.next_to(equation, DOWN, buff=0.5)
        
        self.play(FadeIn(scenario3))
        
        # Keep inputs constant, vary bias
        bias_val = DecimalNumber(0, num_decimal_places=1, color=PURPLE).scale(0.6)
        bias_val.next_to(bias_label, RIGHT, buff=0.2)
        self.play(FadeIn(bias_val))
        
        # w1=2, w2=2, vary b from -2 to 2
        x1_val, x2_val = 1, 1
        for b in [-2, -1, 0, 1, 2]:
            z_val = 2 * x1_val + 2 * x2_val + b
            
            self.play(
                bias_val.animate.set_value(b),
                z_value.animate.set_value(z_val),
                bias_arrow.animate.set_color(PURPLE if b >= 0 else ORANGE),
                neuron.animate.set_fill(YELLOW, opacity=0.4 + abs(z_val)*0.08),
                run_time=0.7
            )
        
        self.wait(2)
        
        # Final message
        final_text = Text("Just like shifting the intercept in a regression line", font_size=28, color=GREEN)
        final_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(final_text))
        self.wait(1)
        
        # Fade out neural network visualization
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)
        
        # Create regression line visualization
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-2, 8, 2],
            x_length=8,
            y_length=6,
            axis_config={"color": GRAY, "include_tip": True},
            tips=True
        )
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        self.play(Create(axes), Write(axes_labels))
        
        # Scatter points (example data)
        dots = VGroup(*[
            Dot(axes.c2p(x, 0.5*x + 2 + np.random.uniform(-0.3, 0.3)), color=BLUE, radius=0.08)
            for x in np.linspace(0.5, 4.5, 12)
        ])
        self.play(FadeIn(dots))
        self.wait(0.5)
        
        # Regression line that will shift
        def get_line(intercept):
            return axes.plot(lambda x: 0.5*x + intercept, color=YELLOW, x_range=[0, 5], stroke_width=4)
        
        regression_line = get_line(2)
        
        # Intercept label
        intercept_label = MathTex("b = ", color=PURPLE).scale(0.9)
        intercept_value = DecimalNumber(2, num_decimal_places=1, color=PURPLE).scale(0.9)
        intercept_value.next_to(intercept_label, RIGHT, buff=0.1)
        intercept_group = VGroup(intercept_label, intercept_value)
        intercept_group.to_corner(UR, buff=0.5)
        
        self.play(Create(regression_line), FadeIn(intercept_group))
        self.wait(1)
        
        # Shift the line up and down by changing intercept
        intercepts = [2, 3.5, 5, 3.5, 2, 0.5, 2]
        
        for b in intercepts[1:]:
            new_line = get_line(b)
            self.play(
                Transform(regression_line, new_line),
                intercept_value.animate.set_value(b),
                run_time=0.8
            )
            self.wait(0.3)
        
        self.wait(1)
        
        # Final emphasis
        shift_text = Text("The bias shifts the entire prediction!", font_size=28, color=PURPLE)
        shift_text.to_edge(DOWN, buff=0.5)
        self.play(Write(shift_text))
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

class WeightsAsVolumeKnobs(Scene):
    def construct(self):
        
        # Volume knob graphic
        knob_circle = Circle(radius=0.8, color=BLUE, stroke_width=4)
        knob_circle.shift(LEFT * 2 + UP * 0.5)
        
        # Knob pointer
        knob_pointer = Line(ORIGIN, UP * 0.6, color=YELLOW, stroke_width=6)
        knob_pointer.move_to(knob_circle.get_center())
        
        # Weight value
        weight_label = MathTex("w =", color=WHITE).scale(0.8)
        weight_value = DecimalNumber(0, num_decimal_places=2, color=YELLOW).scale(0.8)
        weight_value.next_to(weight_label, RIGHT, buff=0.15)
        weight_group = VGroup(weight_label, weight_value)
        weight_group.next_to(knob_circle, DOWN, buff=0.5)
        
        # Output visualization - bars showing volume level
        
        output_bars = VGroup()
        bar_start = knob_circle.get_right() + RIGHT * 1.5
        
        for i in range(10):
            bar = Rectangle(
                width=0.15,
                height=0.4,
                color=GRAY,
                fill_opacity=0.3,
                stroke_width=2
            )
            bar.move_to(bar_start + UP * (i * 0.45 - 2))
            output_bars.add(bar)
        
        output_label = Text("Output", font_size=24, color=WHITE)
        output_label.next_to(output_bars, DOWN, buff=0.3)
        
        # Output value display
        output_text = Text("Volume: ", font_size=22, color=WHITE)
        output_value = DecimalNumber(0, num_decimal_places=1, color=YELLOW).scale(0.9)
        output_value.next_to(output_text, RIGHT, buff=0.1)
        output_display = VGroup(output_text, output_value)
        output_display.next_to(output_bars, UP, buff=0.3)
        
        self.play(
            Create(knob_circle),
            Create(knob_pointer),
            Write(weight_group),
            Create(output_bars),
            Write(output_label),
            Write(output_display)
        )
        self.wait(1)
        
        # Function to light up bars based on weight
        def light_up_bars(num_bars):
            animations = []
            for i, bar in enumerate(output_bars):
                if i < num_bars:
                    animations.append(bar.animate.set_fill(GREEN, opacity=0.9).set_stroke(GREEN, width=3))
                else:
                    animations.append(bar.animate.set_fill(GRAY, opacity=0.3).set_stroke(GRAY, width=2))
            return animations
        
        # Rotate knob and show weight changing with bar visualization
        for angle, w, bars in [(PI/3, 0.5, 2), (2*PI/3, 1.0, 5), (PI, 1.5, 7), (4*PI/3, 2.0, 10)]:
            self.play(
                Rotate(knob_pointer, angle - knob_pointer.get_angle(), about_point=knob_circle.get_center()),
                weight_value.animate.set_value(w),
                output_value.animate.set_value(w * 5),
                *light_up_bars(bars),
                run_time=0.8
            )
            self.wait(0.3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # ICE CREAM SALES EXAMPLE
        # Title for ice cream example
        ice_cream_title = Text("Predicting Ice Cream Sales", font_size=34, color=BLUE)
        ice_cream_title.to_edge(UP)
        self.play(Write(ice_cream_title))
        self.wait(0.5)
        
        # Create axes for temperature vs sales
        axes = Axes(
            x_range=[0, 40, 10],
            y_range=[0, 100, 25],
            x_length=7,
            y_length=4.5,
            axis_config={"color": GRAY},
            tips=True
        )
        axes.shift(DOWN * 0.5)
        
        x_label = Text("Temperature (°C)", font_size=22).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Sales", font_size=22).next_to(axes.y_axis, LEFT, buff=0.3).rotate(PI/2)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        
        # Scatter plot data points (positive correlation)
        ice_cream_data = [
            (5, 15), (10, 25), (15, 35), (20, 50), (25, 65), (30, 75), (35, 90)
        ]
        
        dots = VGroup(*[
            Dot(axes.c2p(temp, sales), color=PINK, radius=0.1)
            for temp, sales in ice_cream_data
        ])
        
        self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.15))
        self.wait(0.5)
        
        # Show neural network learning positive weight
        neuron_diagram = VGroup()
        
        temp_input = Circle(radius=0.2, color=ORANGE, fill_opacity=0.8)
        temp_label = Text("Temp", font_size=10, color=BLACK).move_to(temp_input)
        temp_group = VGroup(temp_input, temp_label).shift(LEFT * 3 + UP * 2)
        
        neuron = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8)
        neuron_label = Text("Sales", font_size=12, color=BLACK).move_to(neuron)
        neuron_group = VGroup(neuron, neuron_label).shift(RIGHT * 0.5 + UP * 2)
        
        weight_arrow = Arrow(temp_input.get_right(), neuron.get_left(), buff=0.1, 
                            color=GREEN, stroke_width=6)
        weight_text = MathTex("w > 0", color=GREEN, font_size=36)
        weight_text.next_to(weight_arrow, UP, buff=0.2)
        
        neuron_diagram.add(temp_group, neuron_group, weight_arrow, weight_text)
        
        self.play(FadeIn(neuron_diagram))
        self.wait(0.5)
        
        # Fit line showing positive relationship
        trend_line = axes.plot(lambda x: 2.5*x + 5, color=GREEN, x_range=[5, 35], stroke_width=4)
        self.play(Create(trend_line))
        self.wait(8)
        
        # Clear for hot chocolate example
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)
        
        # HOT CHOCOLATE EXAMPLE
        hot_choc_title = Text("Predicting Hot Chocolate Demand", font_size=34, color=RED)
        hot_choc_title.to_edge(UP)
        self.play(Write(hot_choc_title))
        self.wait(0.5)
        
        # Create axes
        axes2 = Axes(
            x_range=[0, 40, 10],
            y_range=[0, 100, 25],
            x_length=7,
            y_length=4.5,
            axis_config={"color": GRAY},
            tips=True
        )
        axes2.shift(DOWN * 0.5)
        
        x_label2 = Text("Temperature (°C)", font_size=22).next_to(axes2.x_axis, DOWN, buff=0.3)
        y_label2 = Text("Demand", font_size=22).next_to(axes2.y_axis, LEFT, buff=0.3).rotate(PI/2)
        
        self.play(Create(axes2), Write(x_label2), Write(y_label2))
        self.wait(0.5)
        
        # Scatter plot data (negative correlation)
        hot_choc_data = [
            (5, 90), (10, 75), (15, 65), (20, 50), (25, 35), (30, 25), (35, 15)
        ]
        
        dots2 = VGroup(*[
            Dot(axes2.c2p(temp, demand), color=MAROON, radius=0.1)
            for temp, demand in hot_choc_data
        ])
        
        self.play(LaggedStartMap(FadeIn, dots2, lag_ratio=0.15))
        self.wait(0.5)
        
        # Show neural network with negative weight
        neuron_diagram2 = VGroup()
        
        temp_input2 = Circle(radius=0.2, color=ORANGE, fill_opacity=0.8)
        temp_label2 = Text("Temp", font_size=10, color=BLACK).move_to(temp_input2)
        temp_group2 = VGroup(temp_input2, temp_label2).shift(LEFT * 3 + UP * 2)
        
        neuron2 = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8)
        neuron_label2 = Text("Demand", font_size=12, color=BLACK).move_to(neuron2)
        neuron_group2 = VGroup(neuron2, neuron_label2).shift(RIGHT * 0.5 + UP * 2)
        
        weight_arrow2 = Arrow(temp_input2.get_right(), neuron2.get_left(), buff=0.1, 
                             color=RED, stroke_width=6)
        weight_text2 = MathTex("w < 0", color=RED, font_size=36)
        weight_text2.next_to(weight_arrow2, UP, buff=0.2)
        
        neuron_diagram2.add(temp_group2, neuron_group2, weight_arrow2, weight_text2)
        
        self.play(FadeIn(neuron_diagram2))
        self.wait(0.5)
        
        # Fit line showing negative relationship
        trend_line2 = axes2.plot(lambda x: -2.5*x + 95, color=RED, x_range=[5, 35], stroke_width=4)
        self.play(Create(trend_line2))
        
        # Clear for training section
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Create a simple weight adjustment visualization
        weight_line = NumberLine(
            x_range=[-2, 2, 0.5],
            length=10,
            color=BLUE,
            include_numbers=True,
            label_direction=DOWN,
            font_size=28
        )
        weight_line.shift(DOWN * 0.3)
        
        weight_pointer = Triangle(color=YELLOW, fill_opacity=1).scale(0.3)
        weight_pointer.next_to(weight_line.n2p(0), UP, buff=0.2)
        
        current_weight = MathTex("w = ", color=WHITE).scale(1.1)
        weight_val = DecimalNumber(0, num_decimal_places=2, color=YELLOW).scale(1.1)
        weight_val.next_to(current_weight, RIGHT, buff=0.15)
        weight_display = VGroup(current_weight, weight_val)
        weight_display.next_to(weight_line, UP, buff=1)
        
        self.play(
            Create(weight_line),
            FadeIn(weight_pointer),
            Write(weight_display)
        )
        self.wait(0.5)
        
        # Simulate weight updates during training
        example_text = Text("Example #", font_size=28, color=BLUE)
        example_num = Integer(0, color=YELLOW).scale(1.2)
        example_num.next_to(example_text, RIGHT, buff=0.2)
        example_group = VGroup(example_text, example_num)
        example_group.next_to(weight_display, UP, buff=0.5)
        
        self.play(FadeIn(example_group))
        
        # Weight progression during training
        weight_progression = [0, 0.3, 0.5, 0.8, 1.0, 1.15, 1.25, 1.32, 1.37, 1.40]
        
        for i, w in enumerate(weight_progression[1:], 1):
            self.play(
                example_num.animate.set_value(i),
                weight_pointer.animate.next_to(weight_line.n2p(w), UP, buff=0.2),
                weight_val.animate.set_value(w),
                run_time=0.5
            )
            self.wait(0.2)
        
        self.wait(0.5)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

class BiasVisualization(Scene):
    def construct(self):
        # Title
        title = Text("Each Neuron has a bias", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Show the equation with bias highlighted
        equation = MathTex("z", "=", "w_1x_1", "+", "w_2x_2", "+", "b")
        equation.scale(1.3)
        equation.next_to(title, DOWN, buff=1)
        
        # Highlight bias term
        bias_box = SurroundingRectangle(equation[-1], color=PURPLE, buff=0.15)
        
        self.play(Write(equation))
        self.wait(0.5)
        self.play(Create(bias_box))
        
        bias_label = Text("Bias: The offset/baseline", font_size=24, color=PURPLE)
        bias_label.next_to(bias_box, DOWN, buff=0.3)
        self.play(Write(bias_label))
        self.wait(4)
        
        # Clear for next section
        self.play(*[FadeOut(mob) for mob in [equation, bias_box, bias_label, title]])
        
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GRAY, "include_tip": True},
            tips=True
        )
        axes.shift(DOWN * 0.4)
        
        axes_labels = axes.get_axis_labels(x_label="x_1", y_label="x_2")
        
        self.play(Create(axes), Write(axes_labels))
        self.wait(0.5)
        
        # Highlight the origin
        origin_dot = Dot(axes.c2p(0, 0), color=YELLOW, radius=0.12)
        origin_label = Text("(0, 0)", font_size=20, color=YELLOW)
        origin_label.next_to(origin_dot, DOWN + RIGHT, buff=0.1)
        
        self.play(FadeIn(origin_dot), Write(origin_label))
        self.wait(0.5)
        
        # Show multiple lines pivoting through origin
        line_no_bias = axes.plot(lambda x: 0.5*x, color=RED, x_range=[-4, 4], stroke_width=4)
        bias_text = MathTex("b = 0", color=RED, font_size=32)
        bias_text.to_corner(UR, buff=2)
        
        self.play(Create(line_no_bias), Write(bias_text))
        self.wait(0.5)
        
        # Pivot the line through origin (show limitation)
        slopes = [0.5, 1.5, -0.5, -1.5, 0.5]
        for slope in slopes[1:]:
            new_line = axes.plot(lambda x: slope*x, color=RED, x_range=[-4, 4], stroke_width=4)
            self.play(Transform(line_no_bias, new_line), run_time=0.7)
            self.wait(0.2)
        
        stuck_text = Text("Stuck at the origin!", font_size=26, color=RED)
        stuck_text.next_to(axes, DOWN, buff=0.3)
        self.play(Write(stuck_text))
        self.wait(2)
        
        # Clear for data visualization
        self.play(
            FadeOut(line_no_bias),
            FadeOut(stuck_text),
            FadeOut(bias_text)
        )
        self.wait(0.5)
        
        # Create two clusters of data points (not centered at origin)
        np.random.seed(42)
        
        # Blue cluster (upper right)
        blue_points = []
        for _ in range(15):
            x = np.random.uniform(0.5, 3)
            y = np.random.uniform(2, 3.5)
            blue_points.append(Dot(axes.c2p(x, y), color=BLUE, radius=0.08))
        
        # Red cluster (lower left)
        red_points = []
        for _ in range(15):
            x = np.random.uniform(-3, 0)
            y = np.random.uniform(-3.5, 1)
            red_points.append(Dot(axes.c2p(x, y), color=RED, radius=0.08))
        
        all_points = VGroup(*blue_points, *red_points)
        
        self.play(LaggedStartMap(FadeIn, all_points, lag_ratio=0.05))
        self.wait(1)

        # Try to separate with line through origin (fails)
        bad_line = axes.plot(lambda x: -0.7*x, color=YELLOW, x_range=[-4, 4], 
                           stroke_width=4, stroke_opacity=0.6)
        
        self.play(Create(bad_line))
        
        self.play(FadeOut(bad_line))
        self.wait(0.5)
        
        # PART 3: Bias as a vertical slider
        
        # Show slider control
        slider_line = Line(UP * 2, DOWN * 2, color=PURPLE, stroke_width=6)
        slider_line.to_edge(RIGHT, buff=2)
        
        slider_knob = Circle(radius=0.2, color=PURPLE, fill_opacity=1)
        slider_knob.move_to(slider_line.get_center())
        
        slider_label = Text("Bias\nSlider", font_size=20, color=PURPLE)
        slider_label.next_to(slider_line, RIGHT, buff=0.3)
        
        bias_value = MathTex("b = ", color=PURPLE, font_size=28)
        bias_num = DecimalNumber(0, num_decimal_places=1, color=PURPLE).scale(0.9)
        bias_num.next_to(bias_value, RIGHT, buff=0.1)
        bias_display = VGroup(bias_value, bias_num)
        bias_display.next_to(slider_line, DOWN, buff=0.5)
        
        self.play(
            Create(slider_line),
            FadeIn(slider_knob),
            Write(slider_label),
            Write(bias_display)
        )
        self.wait(0.5)
        
        # Start with line through origin
        separation_line = axes.plot(lambda x: -0.7*x, color=GREEN, x_range=[-4, 4], stroke_width=4)
        self.play(Create(separation_line))
        self.wait(0.5)
        
        # Move slider and shift line up
        bias_values = [0, 0.5, 1.0, 1.5, 2.0, 1.5, 1.0]
        
        for b in bias_values[1:]:
            new_line = axes.plot(lambda x: -0.7*x + b, color=GREEN, x_range=[-4, 4], stroke_width=4)
            slider_pos = slider_line.get_center() + UP * (b * 0.7)
            
            self.play(
                Transform(separation_line, new_line),
                slider_knob.animate.move_to(slider_pos),
                bias_num.animate.set_value(b),
                run_time=0.7
            )
            self.wait(0.3)
        
        self.wait(0.5)
        
        # Highlight perfect separation
        perfect_text = Text("Perfect separation!", font_size=28, color=GREEN)
        perfect_text.next_to(axes, DOWN, buff=0.3)
        self.play(Write(perfect_text))
        self.wait(3)
        
        # Clear for final comparison
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Left side: Weight controls
        left_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.5,
            y_length=4.5,
            axis_config={"color": GRAY, "include_tip": False},
        )
        left_axes.shift(LEFT * 3.5 + DOWN * 0.8)
        
        weight_label = Text("Weight (slope)", font_size=24, color=GREEN)
        weight_label.next_to(left_axes, UP, buff=0.3)
        
        self.play(Create(left_axes), Write(weight_label))
        
        # Show lines with different slopes, same bias
        slopes_demo = [0.3, 0.7, 1.2]
        lines_left = VGroup()
        
        for slope in slopes_demo:
            line = left_axes.plot(lambda x: slope*x + 0.5, color=GREEN, 
                                 x_range=[-3, 3], stroke_width=3, stroke_opacity=0.6)
            lines_left.add(line)
        
        self.play(LaggedStartMap(Create, lines_left, lag_ratio=0.3))
        
        # Right side: Bias controls
        right_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.5,
            y_length=4.5,
            axis_config={"color": GRAY, "include_tip": False},
        )
        right_axes.shift(RIGHT * 3.5 + DOWN * 0.8)
        
        bias_label_final = Text("Bias (offset)", font_size=24, color=PURPLE)
        bias_label_final.next_to(right_axes, UP, buff=0.3)
        
        self.play(Create(right_axes), Write(bias_label_final))
        
        # Show lines with same slope, different bias
        biases_demo = [-1, 0, 1]
        lines_right = VGroup()
        
        for b in biases_demo:
            line = right_axes.plot(lambda x: 0.7*x + b, color=PURPLE, 
                                  x_range=[-3, 3], stroke_width=3, stroke_opacity=0.6)
            lines_right.add(line)
        
        self.play(LaggedStartMap(Create, lines_right, lag_ratio=0.3))
        
        # Final message
        final_message = Text("Together: Positions the boundary anywhere!", 
                           font_size=28, color=GOLD)
        final_message.to_edge(DOWN, buff=0.3)
        self.play(Write(final_message))
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

class ActivationFunctions(Scene):
    def construct(self):
        # Title
        title = Text("How Activation Functions Change the Output", font_size=38)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Show the neuron computation flow
        subtitle = Text("From weighted sum to final output", font_size=26, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(1)
        
        # Show neuron diagram with inputs
        neuron_viz = VGroup()
        
        # Inputs
        x1_node = Circle(radius=0.3, color=BLUE, fill_opacity=0.8)
        x1_label = MathTex("x_1", color=WHITE).scale(0.7).move_to(x1_node)
        x1_group = VGroup(x1_node, x1_label).shift(LEFT * 5 + UP * 1)
        
        x2_node = Circle(radius=0.3, color=BLUE, fill_opacity=0.8)
        x2_label = MathTex("x_2", color=WHITE).scale(0.7).move_to(x2_node)
        x2_group = VGroup(x2_node, x2_label).shift(LEFT * 5 + DOWN * 1)
        
        # Neuron computing z
        z_node = Circle(radius=0.5, color=PURPLE, fill_opacity=0.8)
        z_label = MathTex("z", color=WHITE).scale(0.9).move_to(z_node)
        z_group = VGroup(z_node, z_label).shift(LEFT * 2)
        
        # Weights
        w1_arrow = Arrow(x1_node.get_right(), z_node.get_left() + UP*0.3, buff=0.1, color=GREEN, stroke_width=4)
        w1_label = MathTex("w_1", color=GREEN).scale(0.6).next_to(w1_arrow, UP, buff=0.1)
        
        w2_arrow = Arrow(x2_node.get_right(), z_node.get_left() + DOWN*0.3, buff=0.1, color=GREEN, stroke_width=4)
        w2_label = MathTex("w_2", color=GREEN).scale(0.6).next_to(w2_arrow, DOWN, buff=0.1)
        
        # Bias
        bias_arrow = Arrow(z_node.get_top() + UP*0.5, z_node.get_top(), buff=0.1, color=ORANGE, stroke_width=4)
        bias_label = MathTex("b", color=ORANGE).scale(0.6).next_to(bias_arrow, UP, buff=0.1)
        
        # Equation
        equation = MathTex("z = w_1x_1 + w_2x_2 + b").scale(0.8)
        equation.next_to(z_group, DOWN, buff=0.5)
        
        neuron_viz.add(x1_group, x2_group, z_group, w1_arrow, w1_label, w2_arrow, w2_label, bias_arrow, bias_label, equation)
        
        self.play(LaggedStart(
            FadeIn(x1_group),
            FadeIn(x2_group),
            FadeIn(z_group),
            GrowArrow(w1_arrow), Write(w1_label),
            GrowArrow(w2_arrow), Write(w2_label),
            GrowArrow(bias_arrow), Write(bias_label),
            Write(equation),
            lag_ratio=0.15
        ))
        self.wait(1)
        
        self.play(FadeOut(subtitle))
        self.wait(0.5)
        
        # SIGMOID SECTION
        sigmoid_title = Text("Sigmoid: Smooth 'Off' to 'On' Transition", font_size=28, color=BLUE)
        sigmoid_title.next_to(title, DOWN, buff=0.3)
        self.play(Write(sigmoid_title))
        self.wait(0.5)
        
        # Add activation function to neuron diagram
        activation_node = Circle(radius=0.5, color=YELLOW, fill_opacity=0.8)
        activation_label = MathTex("\\sigma(z)", color=BLACK).scale(0.8).move_to(activation_node)
        activation_group = VGroup(activation_node, activation_label).shift(RIGHT * 1.5)
        
        z_to_activation = Arrow(z_node.get_right(), activation_node.get_left(), buff=0.1, color=BLUE, stroke_width=4)
        
        self.play(
            FadeIn(activation_group),
            GrowArrow(z_to_activation)
        )
        self.wait(0.5)
        
        # Create small sigmoid graph next to activation node
        small_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1, 0.5],
            x_length=2.5,
            y_length=1.5,
            axis_config={"color": GRAY, "stroke_width": 2, "include_tip": False},
        )
        small_axes.next_to(activation_group, RIGHT, buff=0.5)
        
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))
        
        sigmoid_curve = small_axes.plot(sigmoid, color=BLUE, x_range=[-3, 3], stroke_width=3)
        
        self.play(Create(small_axes), Create(sigmoid_curve))
        self.wait(0.5)
        
        # Input value trackers
        x1_val = ValueTracker(0.5)
        x2_val = ValueTracker(0.5)
        w1_val = ValueTracker(1.0)
        w2_val = ValueTracker(1.0)
        b_val = ValueTracker(-2.0)
        
        # Display values
        x1_display = always_redraw(lambda: DecimalNumber(x1_val.get_value(), num_decimal_places=1, color=BLUE)
                                   .scale(0.5).next_to(x1_group, LEFT, buff=0.2))
        x2_display = always_redraw(lambda: DecimalNumber(x2_val.get_value(), num_decimal_places=1, color=BLUE)
                                   .scale(0.5).next_to(x2_group, LEFT, buff=0.2))
        
        # Helper functions to compute z and output
        def get_z():
            return w1_val.get_value() * x1_val.get_value() + w2_val.get_value() * x2_val.get_value() + b_val.get_value()
        
        z_display = always_redraw(lambda: DecimalNumber(get_z(), num_decimal_places=2, color=PURPLE)
                                  .scale(0.6).next_to(z_group, RIGHT, buff=0.3)).shift(UP * 0.1)
        
        output_display = always_redraw(lambda: DecimalNumber(sigmoid(get_z()), num_decimal_places=2, color=YELLOW)
                                       .scale(0.6).next_to(activation_group, RIGHT, buff=0.3))
        
        # Dot on sigmoid curve
        sigmoid_dot = always_redraw(lambda: Dot(
            small_axes.c2p(get_z(), sigmoid(get_z())),
            color=RED, radius=0.08
        ))
        
        self.play(
            Write(x1_display), Write(x2_display),
            Write(z_display), Write(output_display),
            FadeIn(sigmoid_dot)
        )
        self.wait(1)
        
        # Scenario 1: Negative z (OFF)
        scenario1 = Text("Low inputs → Negative z → Output near 0 (OFF)", 
                        font_size=20, color=RED)
        scenario1.to_edge(DOWN, buff=0.5)
        self.play(Write(scenario1))
        self.wait(1)
        
        # Scenario 2: Increase inputs gradually
        scenario2 = Text("Increasing inputs → z rises → Output smoothly transitions", 
                        font_size=20, color=YELLOW)
        scenario2.to_edge(DOWN, buff=0.5)
        
        self.play(FadeOut(scenario1), FadeIn(scenario2))
        
        self.play(
            x1_val.animate.set_value(1.5),
            x2_val.animate.set_value(1.5),
            run_time=2
        )
        self.wait(1)
        
        # Scenario 3: High z (ON)
        self.play(
            x1_val.animate.set_value(2.5),
            x2_val.animate.set_value(2.5),
            run_time=2
        )
        
        scenario3 = Text("High inputs → Positive z → Output near 1 (ON)", 
                        font_size=20, color=GREEN)
        scenario3.to_edge(DOWN, buff=0.5)
        self.play(FadeOut(scenario2), FadeIn(scenario3))
        self.wait(2)
        
        # Show effect of bias
        self.play(FadeOut(scenario3))
        bias_scenario = Text("Changing bias shifts the threshold", 
                           font_size=20, color=ORANGE)
        bias_scenario.to_edge(DOWN, buff=0.5)
        self.play(Write(bias_scenario))
        
        # Reset inputs, change bias
        self.play(
            x1_val.animate.set_value(1.0),
            x2_val.animate.set_value(1.0),
            run_time=1
        )
        self.wait(0.5)
        
        # Increase bias to push neuron ON
        self.play(b_val.animate.set_value(0), run_time=2)
        self.wait(1.5)
        
        # Clear for ReLU
        self.play(*[FadeOut(mob) for mob in [
            neuron_viz, activation_group, z_to_activation, small_axes, sigmoid_curve,
            x1_display, x2_display, z_display, output_display, sigmoid_dot,
            bias_scenario, sigmoid_title
        ]])
        self.wait(0.5)
        
        # ReLU SECTION
        relu_title = Text("ReLU: Activates Only When z > 0", font_size=28, color=GREEN)
        relu_title.next_to(title, DOWN, buff=0.3)
        self.play(Write(relu_title))
        self.wait(0.5)
        
        # Rebuild neuron diagram for ReLU
        neuron_viz2 = VGroup()
        
        x1_node2 = Circle(radius=0.3, color=BLUE, fill_opacity=0.8)
        x1_label2 = MathTex("x_1", color=WHITE).scale(0.7).move_to(x1_node2)
        x1_group2 = VGroup(x1_node2, x1_label2).shift(LEFT * 5 + UP * 1)
        
        x2_node2 = Circle(radius=0.3, color=BLUE, fill_opacity=0.8)
        x2_label2 = MathTex("x_2", color=WHITE).scale(0.7).move_to(x2_node2)
        x2_group2 = VGroup(x2_node2, x2_label2).shift(LEFT * 5 + DOWN * 1)
        
        z_node2 = Circle(radius=0.5, color=PURPLE, fill_opacity=0.8)
        z_label2 = MathTex("z", color=WHITE).scale(0.9).move_to(z_node2)
        z_group2 = VGroup(z_node2, z_label2).shift(LEFT * 2)
        
        w1_arrow2 = Arrow(x1_node2.get_right(), z_node2.get_left() + UP*0.3, buff=0.1, color=GREEN, stroke_width=4)
        w1_label2 = MathTex("w_1", color=GREEN).scale(0.6).next_to(w1_arrow2, UP, buff=0.1)
        
        w2_arrow2 = Arrow(x2_node2.get_right(), z_node2.get_left() + DOWN*0.3, buff=0.1, color=GREEN, stroke_width=4)
        w2_label2 = MathTex("w_2", color=GREEN).scale(0.6).next_to(w2_arrow2, DOWN, buff=0.1)
        
        bias_arrow2 = Arrow(z_node2.get_top() + UP*0.5, z_node2.get_top(), buff=0.1, color=ORANGE, stroke_width=4)
        bias_label2 = MathTex("b", color=ORANGE).scale(0.6).next_to(bias_arrow2, UP, buff=0.1)
        
        equation2 = MathTex("z = w_1x_1 + w_2x_2 + b").scale(0.8)
        equation2.next_to(z_group2, DOWN, buff=0.5)
        
        neuron_viz2.add(x1_group2, x2_group2, z_group2, w1_arrow2, w1_label2, w2_arrow2, w2_label2, bias_arrow2, bias_label2, equation2)
        
        activation_node2 = Circle(radius=0.5, color=YELLOW, fill_opacity=0.8)
        activation_label2 = MathTex("ReLU(z)", color=BLACK).scale(0.7).move_to(activation_node2)
        activation_group2 = VGroup(activation_node2, activation_label2).shift(RIGHT * 1.5)
        
        z_to_activation2 = Arrow(z_node2.get_right(), activation_node2.get_left(), buff=0.1, color=GREEN, stroke_width=4)
        
        self.play(
            FadeIn(neuron_viz2),
            FadeIn(activation_group2),
            GrowArrow(z_to_activation2)
        )
        self.wait(0.5)
        
        # Small ReLU graph
        small_axes2 = Axes(
            x_range=[-2, 2, 1],
            y_range=[0, 2, 1],
            x_length=2.5,
            y_length=1.5,
            axis_config={"color": GRAY, "stroke_width": 2, "include_tip": False},
        )
        small_axes2.next_to(activation_group2, RIGHT, buff=0.5)
        
        def relu(x):
            return max(0, x)
        
        relu_neg = small_axes2.plot(lambda x: 0, color=RED, x_range=[-2, 0], stroke_width=3)
        relu_pos = small_axes2.plot(lambda x: x, color=GREEN, x_range=[0, 2], stroke_width=3)
        
        self.play(Create(small_axes2), Create(relu_neg), Create(relu_pos))
        self.wait(0.5)
        
        # Reset trackers for ReLU
        x1_val.set_value(0.5)
        x2_val.set_value(0.5)
        w1_val.set_value(1.0)
        w2_val.set_value(1.0)
        b_val.set_value(-1.5)
        
        # Displays for ReLU
        x1_display2 = always_redraw(lambda: DecimalNumber(x1_val.get_value(), num_decimal_places=1, color=BLUE)
                                    .scale(0.5).next_to(x1_group2, LEFT, buff=0.2))
        x2_display2 = always_redraw(lambda: DecimalNumber(x2_val.get_value(), num_decimal_places=1, color=BLUE)
                                    .scale(0.5).next_to(x2_group2, LEFT, buff=0.2))
        
        z_display2 = always_redraw(lambda: DecimalNumber(get_z(), num_decimal_places=2, color=PURPLE)
                                   .scale(0.6).next_to(z_group2, RIGHT, buff=0.3)).shift(UP * 0.1)
        
        output_display2 = always_redraw(lambda: DecimalNumber(relu(get_z()), num_decimal_places=2, color=YELLOW)
                                        .scale(0.6).next_to(activation_group2, RIGHT, buff=0.3))
        
        relu_dot = always_redraw(lambda: Dot(
            small_axes2.c2p(min(2, max(-2, get_z())), relu(get_z())),
            color=RED, radius=0.08
        ))
        
        self.play(
            Write(x1_display2), Write(x2_display2),
            Write(z_display2), Write(output_display2),
            FadeIn(relu_dot)
        )
        self.wait(1)
        
        # Scenario 1: Negative z (Neuron OFF)
        relu_scenario1 = Text("z < 0 → Neuron stays OFF (output = 0)", 
                             font_size=20, color=RED)
        relu_scenario1.to_edge(DOWN, buff=0.5)
        self.play(Write(relu_scenario1))
        self.wait(1.5)
        
        # Scenario 2: Cross threshold
        relu_scenario2 = Text("Increasing z... crossing threshold at z = 0", 
                             font_size=20, color=YELLOW)
        relu_scenario2.to_edge(DOWN, buff=0.5)
        
        self.play(FadeOut(relu_scenario1), FadeIn(relu_scenario2))
        
        self.play(
            x1_val.animate.set_value(1.5),
            x2_val.animate.set_value(1.5),
            run_time=2.5
        )
        self.wait(1)
        
        # Scenario 3: z > 0 (Neuron ON and growing)
        relu_scenario3 = Text("z > 0 → Neuron ON! Output grows linearly", 
                             font_size=20, color=GREEN)
        relu_scenario3.to_edge(DOWN, buff=0.5)
        
        self.play(FadeOut(relu_scenario2), FadeIn(relu_scenario3))
        
        self.play(
            x1_val.animate.set_value(2.5),
            x2_val.animate.set_value(2.0),
            run_time=2
        )
        self.wait(2)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

class NeuronDecisionMaker(Scene):
    def construct(self):
        # Title
        title = Text("A Neuron: A Tiny Decision-Maker", font_size=40, color=GOLD)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # PART 1: Show different types of inputs
        input_section = Text("Inputs can be anything:", font_size=30, color=BLUE)
        input_section.next_to(title, DOWN, buff=0.5)
        self.play(Write(input_section))
        self.wait(0.5)
        
        # Show examples of inputs
        # Pixels from image
        pixel_grid = VGroup()
        for i in range(4):
            for j in range(4):
                brightness = np.random.uniform(0.3, 1.0)
                square = Square(side_length=0.3, color=BLUE, fill_opacity=brightness, stroke_width=1)
                square.shift(LEFT * 4 + UP * 0.5 + RIGHT * j * 0.3 + DOWN * i * 0.3)
                pixel_grid.add(square)
        
        pixel_label = Text("Pixels", font_size=20, color=BLUE)
        pixel_label.next_to(pixel_grid, DOWN, buff=0.3)
        
        # Sensor readings
        sensor_group = VGroup()
        thermometer = Line(UP * 0.5, DOWN * 0.5, color=RED, stroke_width=6)
        thermometer_bulb = Circle(radius=0.15, color=RED, fill_opacity=1).next_to(thermometer, DOWN, buff=0)
        sensor_reading = MathTex("23.5°C", color=RED, font_size=24).next_to(thermometer, UP, buff=0.2)
        sensor_group.add(thermometer, thermometer_bulb, sensor_reading)
        # sensor_group.shift(UP * 0.5)
        
        sensor_label = Text("Sensor Data", font_size=20, color=RED)
        sensor_label.next_to(sensor_group, DOWN, buff=0.3)
        
        # Health data
        health_group = VGroup()
        health_item1 = MathTex("\\text{Age: } 45").scale(0.6)
        health_item2 = MathTex("\\text{BP: } 120/80").scale(0.6)
        health_item3 = MathTex("\\text{HR: } 72").scale(0.6)
        health_data = VGroup(health_item1, health_item2, health_item3).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        health_group.add(health_data)
        health_group.shift(RIGHT * 4)
        
        health_label = Text("Health Data", font_size=20, color=GREEN)
        health_label.next_to(health_group, DOWN, buff=0.3)
        
        self.play(
            LaggedStart(
                FadeIn(pixel_grid), Write(pixel_label),
                FadeIn(sensor_group), Write(sensor_label),
                FadeIn(health_group), Write(health_label),
                lag_ratio=0.4
            )
        )
        self.wait(2)
        
        # Clear examples
        self.play(*[FadeOut(mob) for mob in [
            pixel_grid, pixel_label, sensor_group, sensor_label,
            health_group, health_label, input_section
        ]])      
        
        # Create neuron with multiple inputs
        neuron = Circle(radius=0.6, color=YELLOW, fill_opacity=0.8)
        neuron_label = Text("Neuron", font_size=20, color=BLACK).move_to(neuron)
        neuron_group = VGroup(neuron, neuron_label)
        
        # Create inputs
        num_inputs = 4
        inputs = VGroup()
        arrows = VGroup()
        weight_labels = VGroup()
        
        for i in range(num_inputs):
            # Input node
            input_circle = Circle(radius=0.25, color=BLUE, fill_opacity=0.7)
            input_label = MathTex(f"x_{{{i+1}}}", color=WHITE, font_size=24).move_to(input_circle)
            input_node = VGroup(input_circle, input_label)
            
            # Position inputs vertically on the left
            y_pos = 2 - i * 1.3
            input_node.shift(LEFT * 4 + UP * y_pos)
            inputs.add(input_node)
            
            # Arrow from input to neuron
            arrow = Arrow(
                input_circle.get_right(),
                neuron.get_left() + UP * (y_pos * 0.3),
                buff=0.1,
                color=GREEN,
                stroke_width=3 + i  # Varying thickness to show different importance
            )
            arrows.add(arrow)
            
            # Weight label
            weight = MathTex(f"w_{{{i+1}}}", color=GREEN).scale(0.7)
            weight.next_to(arrow, DOWN, buff=0.1)
            weight_labels.add(weight)
        
        self.play(FadeIn(neuron_group))
        
        self.play(
            LaggedStart(*[FadeIn(inp) for inp in inputs], lag_ratio=0.2)
        )
        
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.15),
            LaggedStart(*[Write(label) for label in weight_labels], lag_ratio=0.15)
        )
        
        # PART 3: Show the multiplication and addition process
        
        # Show example values
        input_values = [2.0, 1.5, 3.0, 0.5]
        weight_values = [1.2, 0.8, 1.5, 0.3]
        
        # Display values next to inputs
        input_displays = VGroup()
        for i, (inp, val) in enumerate(zip(inputs, input_values)):
            val_display = MathTex(f"= {val}", color=BLUE).scale(0.7)
            val_display.next_to(inp, LEFT, buff=0.2)
            input_displays.add(val_display)
        
        weight_displays = VGroup()
        for i, (label, val) in enumerate(zip(weight_labels, weight_values)):
            val_display = MathTex(f"= {val}", color=GREEN).scale(0.6)
            val_display.next_to(label, RIGHT, buff=0.15)
            weight_displays.add(val_display)
        
        self.play(
            LaggedStart(*[Write(disp) for disp in input_displays], lag_ratio=0.2),
            LaggedStart(*[Write(disp) for disp in weight_displays], lag_ratio=0.2)
        )
        self.wait(1)
        
        # Show multiplication results flowing into neuron
        products = []
        product_animations = []
        
        for i in range(num_inputs):
            product_val = input_values[i] * weight_values[i]
            products.append(product_val)
            
            # Create product text
            product_text = MathTex(f"{product_val:.2f}", color=ORANGE).scale(0.7)
            product_text.shift(arrows[i].get_center() + RIGHT * 0.5)
            
            # Animate product appearing
            product_animations.append(FadeIn(product_text, shift=RIGHT * 0.5))
        
        self.play(LaggedStart(*product_animations, lag_ratio=0.3))
        self.wait(3)
        
        # Clear for next part
        self.play(*[FadeOut(mob) for mob in [
            neuron_group, inputs, arrows, weight_labels, input_displays, weight_displays,
            *self.mobjects[-num_inputs:],  # Remove product texts
        ]])
        self.wait(0.3)
        
        # PART 4: Show the weighted sum equation
        equation_title = Text("The Weighted Sum Formula", font_size=30, color=PURPLE)
        equation_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(equation_title))
        self.wait(0.5)
        
        # Show full equation
        equation = MathTex(
            "z", "=", "w_1", "x_1", "+", "w_2", "x_2", "+", "\\cdots", "+", "w_n", "x_n", "+", "b"
        )
        equation.scale(1.3)
        equation.shift(DOWN * 0.5)
        
        self.play(Write(equation))
        self.wait(8)
        
        # Label components
        inputs_brace = Brace(equation[2:12], DOWN, color=BLUE)
        inputs_label = Text("Weighted inputs", font_size=24, color=BLUE)
        inputs_label.next_to(inputs_brace, DOWN, buff=0.2)
        
        bias_brace = Brace(equation[-1], DOWN, color=ORANGE)
        bias_label = Text("Bias", font_size=24, color=ORANGE)
        bias_label.next_to(bias_brace, DOWN, buff=0.2)
        
        self.play(
            GrowFromCenter(inputs_brace),
            Write(inputs_label)
        )
        self.wait(1)
        
        self.play(
            GrowFromCenter(bias_brace),
            Write(bias_label)
        )
        self.wait(4)
        
        # Highlight z
        z_box = SurroundingRectangle(equation[0], color=YELLOW, buff=0.15)
        z_explanation = Text("The weighted sum", font_size=24, color=YELLOW)
        z_explanation.next_to(z_box, UP, buff=0.3)
        
        self.play(
            Create(z_box),
            Write(z_explanation)
        )
        self.wait(8)
        
        # Clear braces and labels
        self.play(*[FadeOut(mob) for mob in [
            inputs_brace, inputs_label, bias_brace, bias_label,
            z_box, z_explanation, equation_title
        ]])
        
        # Final message
        final_message = Text("A single number capturing all the information!", 
                           font_size=26, color=GOLD)
        final_message.to_edge(DOWN, buff=0.5)
        self.play(Write(final_message))
        self.wait(1)

class NeuronStacking(Scene):
    def construct(self):
        # Title
        title = Text("From Weighted Sum to Final Decision", font_size=38)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # PART 1: Show the transformation equation
        subtitle = Text("Adding the activation function", font_size=26, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(1)
        
        # Show z equation first
        z_eq = MathTex("z", "=", "w_1x_1", "+", "w_2x_2", "+", "b")
        z_eq.scale(1.2)
        z_eq.shift(UP * 1.5)
        
        self.play(Write(z_eq))
        self.wait(1)
        
        # Arrow down
        transform_arrow = Arrow(z_eq.get_bottom(), z_eq.get_bottom() + DOWN * 1, 
                               color=YELLOW, stroke_width=4)
        transform_label = Text("Apply activation", font_size=22, color=YELLOW)
        transform_label.next_to(transform_arrow, RIGHT, buff=0.2)
        
        self.play(GrowArrow(transform_arrow), Write(transform_label))
        self.wait(0.5)
        
        # Show output equation
        y_eq = MathTex("y", "=", "A", "(", "z", ")")
        y_eq.scale(1.2)
        y_eq.shift(DOWN * 0.5)
        
        self.play(Write(y_eq))
        self.wait(0.5)
        
        # Highlight A
        a_box = SurroundingRectangle(y_eq[2], color=GREEN, buff=0.1)
        a_label = Text("Activation function", font_size=20, color=GREEN)
        a_label.next_to(a_box, DOWN, buff=0.3)
        
        self.play(Create(a_box), Write(a_label))
        self.wait(1)
        
        # Final decision emphasis
        final_box = SurroundingRectangle(y_eq, color=GOLD, buff=0.15)
        final_label = Text("Neuron's final decision", font_size=24, color=GOLD)
        final_label.next_to(final_box, DOWN, buff=0.5)
        
        self.play(
            Create(final_box),
            Write(final_label),
            FadeOut(a_box),
            FadeOut(a_label)
        )
        self.wait(2)
        
        # Clear for next section
        self.play(*[FadeOut(mob) for mob in [
            z_eq, transform_arrow, transform_label, y_eq, 
            final_box, final_label, subtitle
        ]])
        self.wait(0.5)
        
        # PART 2: Single neuron = Linear regression with one line
        linear_title = Text("One Neuron = One Linear Decision Boundary", font_size=30, color=BLUE)
        linear_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(linear_title))
        self.wait(0.5)
        
        # Create axes with data points
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": GRAY},
        )
        axes.shift(LEFT * 3)
        
        axes_labels = axes.get_axis_labels(x_label="x_1", y_label="x_2")
        
        self.play(Create(axes), Write(axes_labels))
        self.wait(0.3)
        
        # Add data points (two classes)
        np.random.seed(42)
        blue_points = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE, radius=0.08)
            for x, y in [(np.random.uniform(-2.5, -0.5), np.random.uniform(-2.5, -0.5)) 
                        for _ in range(12)]
        ])
        
        red_points = VGroup(*[
            Dot(axes.c2p(x, y), color=RED, radius=0.08)
            for x, y in [(np.random.uniform(0.5, 2.5), np.random.uniform(0.5, 2.5)) 
                        for _ in range(12)]
        ])
        
        self.play(FadeIn(blue_points), FadeIn(red_points))
        self.wait(0.5)
        
        # Single neuron can only draw one line
        decision_line = axes.plot(lambda x: x, color=GREEN, x_range=[-3, 3], stroke_width=4)
        
        self.play(Create(decision_line))
        self.wait(0.5)
        
        # Show neuron diagram
        single_neuron = Circle(radius=0.4, color=YELLOW, fill_opacity=0.8)
        single_neuron_label = MathTex("y = A(z)", color=BLACK, font_size=20).move_to(single_neuron)
        single_neuron_group = VGroup(single_neuron, single_neuron_label)
        single_neuron_group.shift(RIGHT * 3.5 + UP * 1)
        
        limitation_text = Text("Only ONE line!\nLimited decisions", 
                             font_size=22, color=ORANGE, line_spacing=1.2)
        limitation_text.next_to(single_neuron_group, DOWN, buff=0.5)
        
        self.play(FadeIn(single_neuron_group))
        self.play(Write(limitation_text))
        self.wait(2)
        
        # Clear for multiple neurons
        self.play(*[FadeOut(mob) for mob in [
            axes, axes_labels, blue_points, red_points, decision_line,
            single_neuron_group, limitation_text, linear_title
        ]])
        self.wait(0.5)
        
        # PART 3: Multiple neurons = Multiple lines (parallel processing)
        multi_title = Text("Multiple Neurons = Multiple Decision Boundaries", 
                          font_size=30, color=PURPLE)
        multi_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(multi_title))
        self.wait(0.5)
        
        # Create new axes with more complex data
        axes2 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": GRAY},
        )
        axes2.shift(LEFT * 3)
        
        axes_labels2 = axes2.get_axis_labels(x_label="x_1", y_label="x_2")
        
        self.play(Create(axes2), Write(axes_labels2))
        self.wait(0.3)
        
        # More complex data pattern (non-linearly separable)
        blue_points2 = VGroup(*[
            Dot(axes2.c2p(x, y), color=BLUE, radius=0.08)
            for x, y in [(np.random.uniform(-2.5, -0.5), np.random.uniform(-2, 2)),
                        (np.random.uniform(0.5, 2.5), np.random.uniform(-2, 2))]
            for _ in range(6)
        ])
        
        red_points2 = VGroup(*[
            Dot(axes2.c2p(x, y), color=RED, radius=0.08)
            for x, y in [(np.random.uniform(-1, 1), np.random.uniform(-2.5, -0.5)),
                        (np.random.uniform(-1, 1), np.random.uniform(0.5, 2.5))]
            for _ in range(6)
        ])
        
        self.play(FadeIn(blue_points2), FadeIn(red_points2))
        self.wait(0.5)
        
        # Show multiple neurons creating multiple lines
        layer_group = VGroup()
        
        neuron1 = Circle(radius=0.35, color=YELLOW, fill_opacity=0.8)
        neuron1_label = MathTex("y_1", color=BLACK, font_size=18).move_to(neuron1)
        neuron1_group = VGroup(neuron1, neuron1_label)
        neuron1_group.shift(RIGHT * 3 + UP * 1.5)
        
        neuron2 = Circle(radius=0.35, color=YELLOW, fill_opacity=0.8)
        neuron2_label = MathTex("y_2", color=BLACK, font_size=18).move_to(neuron2)
        neuron2_group = VGroup(neuron2, neuron2_label)
        neuron2_group.shift(RIGHT * 3 + UP * 0.3)
        
        neuron3 = Circle(radius=0.35, color=YELLOW, fill_opacity=0.8)
        neuron3_label = MathTex("y_3", color=BLACK, font_size=18).move_to(neuron3)
        neuron3_group = VGroup(neuron3, neuron3_label)
        neuron3_group.shift(RIGHT * 3 + DOWN * 0.9)
        
        layer_group.add(neuron1_group, neuron2_group, neuron3_group)
        
        parallel_text = Text("Working in\nPARALLEL", font_size=20, color=GREEN, line_spacing=1.2)
        parallel_text.next_to(layer_group, RIGHT, buff=0.3)
        
        self.play(
            LaggedStart(
                FadeIn(neuron1_group),
                FadeIn(neuron2_group),
                FadeIn(neuron3_group),
                lag_ratio=0.3
            )
        )
        self.play(Write(parallel_text))
        self.wait(0.5)
        
        # Draw multiple decision boundaries
        line1 = axes2.plot(lambda x: 0.5*x + 1, color=YELLOW, x_range=[-3, 3], 
                          stroke_width=3, stroke_opacity=0.8)
        line1_label = MathTex("y_1", color=YELLOW, font_size=18, background_stroke_width=2)
        line1_label.next_to(axes2.c2p(2, 2), UR, buff=0.1)
        
        line2 = axes2.plot(lambda x: -0.8*x, color=ORANGE, x_range=[-3, 3], 
                          stroke_width=3, stroke_opacity=0.8)
        line2_label = MathTex("y_2", color=ORANGE, font_size=18, background_stroke_width=2)
        line2_label.next_to(axes2.c2p(-2, 1.6), UL, buff=0.1)
        
        line3 = axes2.plot(lambda x: 0.5*x - 1, color=GREEN, x_range=[-3, 3], 
                          stroke_width=3, stroke_opacity=0.8)
        line3_label = MathTex("y_3", color=GREEN, font_size=18, background_stroke_width=2)
        line3_label.next_to(axes2.c2p(2, 0), DR, buff=0.1)
        
        self.play(
            Create(line1), Write(line1_label),
            neuron1.animate.set_fill(YELLOW, opacity=1)
        )
        self.wait(0.3)
        
        self.play(
            Create(line2), Write(line2_label),
            neuron2.animate.set_fill(ORANGE, opacity=1)
        )
        self.wait(0.3)
        
        self.play(
            Create(line3), Write(line3_label),
            neuron3.animate.set_fill(GREEN, opacity=1)
        )
        self.wait(1)
        
        multiple_text = Text("Each neuron:\nOne linear boundary", 
                           font_size=22, color=GOLD, line_spacing=1.2)
        multiple_text.to_edge(DOWN, buff=0.5)
        self.play(Write(multiple_text))
        self.wait(2)
        
        # Clear for non-linearity section
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != title])
        self.wait(0.5)
        
        # PART 4: Combining creates non-linearity
        nonlinear_title = Text("Activation Creates Non-Linearity", font_size=32, color=RED)
        nonlinear_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(nonlinear_title))
        self.wait(0.5)
        
        # Show transformation from linear z to non-linear y
        comparison = VGroup()
        
        # Left: Linear z
        axes_left = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4,
            y_length=3.5,
            axis_config={"color": GRAY},
        )
        axes_left.shift(LEFT * 3.5 + DOWN * 0.5)
        
        linear_line = axes_left.plot(lambda x: 0.8*x + 0.5, color=BLUE, 
                                     x_range=[-3, 3], stroke_width=4)
        linear_label = Text("z = wx + b", font_size=22, color=BLUE)
        linear_label.next_to(axes_left, UP, buff=0.3)
        linear_desc = Text("Linear", font_size=20, color=BLUE)
        linear_desc.next_to(axes_left, DOWN, buff=0.3)
        
        comparison.add(axes_left, linear_line, linear_label, linear_desc)
        
        # Right: Non-linear y
        axes_right = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1, 0.5],
            x_length=4,
            y_length=3.5,
            axis_config={"color": GRAY},
        )
        axes_right.shift(RIGHT * 3.5 + DOWN * 0.5)
        
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))
        
        nonlinear_curve = axes_right.plot(
            lambda x: sigmoid(0.8*x + 0.5), 
            color=RED, x_range=[-3, 3], stroke_width=4
        )
        nonlinear_label = Text("y = σ(z)", font_size=22, color=RED)
        nonlinear_label.next_to(axes_right, UP, buff=0.3)
        nonlinear_desc = Text("Non-Linear", font_size=20, color=RED)
        nonlinear_desc.next_to(axes_right, DOWN, buff=0.3)
        
        comparison.add(axes_right, nonlinear_curve, nonlinear_label, nonlinear_desc)
        
        self.play(
            Create(axes_left), Create(linear_line),
            Write(linear_label), Write(linear_desc)
        )
        self.wait(1)
        
        # Arrow between them
        transform_arrow2 = Arrow(axes_left.get_right(), axes_right.get_left(), 
                                color=YELLOW, stroke_width=4, buff=0.3)
        transform_text = Text("A(z)", font_size=20, color=YELLOW)
        transform_text.next_to(transform_arrow2, UP, buff=0.1)
        
        self.play(GrowArrow(transform_arrow2), Write(transform_text))
        self.wait(0.5)
        
        self.play(
            Create(axes_right), Create(nonlinear_curve),
            Write(nonlinear_label), Write(nonlinear_desc)
        )
        self.wait(2)
        
        # Final explanation
        explanation = Text(
            "Linear boundaries + Non-linear activation\n= Complex pattern recognition",
            font_size=24,
            color=GOLD,
            line_spacing=1.3
        )
        explanation.to_edge(DOWN, buff=0.5)
        self.play(Write(explanation))
        self.wait(2)
        
        # Clear for final visualization
        self.play(*[FadeOut(mob) for mob in self.mobjects if mob != title])
        self.wait(0.5)
        
        # PART 5: Final network visualization
        final_title = Text("Many Neurons = Sophisticated Mapping", font_size=32, color=GOLD)
        final_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(final_title))
        self.wait(0.5)
        
        # Create a small network
        network = VGroup()
        
        # Input layer
        inputs_layer = VGroup(*[
            Circle(radius=0.25, color=BLUE, fill_opacity=0.7)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.5)
        inputs_layer.shift(LEFT * 4)
        
        # Hidden layer (multiple neurons)
        hidden_layer = VGroup(*[
            Circle(radius=0.25, color=YELLOW, fill_opacity=0.8)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.4)
        hidden_layer.shift(LEFT * 1.5)
        
        # Output layer
        output_layer = VGroup(*[
            Circle(radius=0.25, color=GREEN, fill_opacity=0.8)
            for _ in range(2)
        ]).arrange(DOWN, buff=0.6)
        output_layer.shift(RIGHT * 1.5)
        
        # Connections
        connections = VGroup()
        for inp in inputs_layer:
            for hidden in hidden_layer:
                line = Line(inp.get_center(), hidden.get_center(), 
                          stroke_width=1, color=GRAY, stroke_opacity=0.3)
                connections.add(line)
        
        for hidden in hidden_layer:
            for out in output_layer:
                line = Line(hidden.get_center(), out.get_center(),
                          stroke_width=1, color=GRAY, stroke_opacity=0.3)
                connections.add(line)
        
        network.add(connections, inputs_layer, hidden_layer, output_layer)
        
        # Labels
        input_label = Text("Inputs", font_size=18, color=BLUE)
        input_label.next_to(inputs_layer, LEFT, buff=0.3)
        
        hidden_label = Text("Parallel\nProcessing", font_size=18, color=YELLOW, line_spacing=1.2)
        hidden_label.next_to(hidden_layer, DOWN, buff=0.4)
        
        output_label = Text("Complex\nDecisions", font_size=18, color=GREEN, line_spacing=1.2)
        output_label.next_to(output_layer, RIGHT, buff=0.3)
        
        self.play(
            Create(connections),
            LaggedStart(*[FadeIn(node) for node in inputs_layer], lag_ratio=0.2),
            Write(input_label)
        )
        self.wait(0.5)
        
        self.play(
            LaggedStart(*[FadeIn(node) for node in hidden_layer], lag_ratio=0.15),
            Write(hidden_label)
        )
        self.wait(0.5)
        
        self.play(
            LaggedStart(*[FadeIn(node) for node in output_layer], lag_ratio=0.3),
            Write(output_label)
        )
        self.wait(1)
        
        # Final message
        final_message = Text(
            "Each neuron: Simple linear decision\nTogether: Complex pattern learning",
            font_size=26,
            color=GOLD,
            line_spacing=1.3
        )
        final_message.to_edge(DOWN, buff=0.5)
        self.play(Write(final_message))
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

class SmartThermostatExample(Scene):
    def construct(self):
        # Title
        title = Text("Real World Example: Smart Thermostat", font_size=40, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Subtitle
        subtitle = Text("Deciding when to turn on air conditioning", font_size=26, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(1.5)
        
        self.play(FadeOut(subtitle))
        self.wait(0.3)
        
        # PART 1: Show the thermostat and its inputs
        scenario = Text("The Problem: Should we turn on the AC?", font_size=28, color=ORANGE)
        scenario.next_to(title, DOWN, buff=0.4)
        self.play(Write(scenario))
        self.wait(1)
        
        # Create visual representations of inputs
        # Temperature thermometer
        temp_group = VGroup()
        thermometer = Rectangle(width=0.3, height=2, color=RED, fill_opacity=0.8)
        temp_bulb = Circle(radius=0.25, color=RED, fill_opacity=1)
        temp_bulb.next_to(thermometer, DOWN, buff=0)
        temp_reading = MathTex("32°C", color=RED, font_size=32)
        temp_reading.next_to(thermometer, UP, buff=0.2)
        temp_label = Text("Room Temp", font_size=20, color=WHITE)
        temp_label.next_to(temp_bulb, DOWN, buff=0.3)
        temp_group.add(thermometer, temp_bulb, temp_reading, temp_label)
        temp_group.shift(LEFT * 4.5 + UP * 0.5)
        
        # Sunlight (sun icon)
        sun_group = VGroup()
        sun_circle = Circle(radius=0.4, color=YELLOW, fill_opacity=0.9)
        sun_rays = VGroup(*[
            Line(ORIGIN, OUT * 0.3, color=YELLOW, stroke_width=4).rotate(i * PI/4).shift(OUT * 0.5)
            for i in range(8)
        ])
        for ray in sun_rays:
            ray.move_to(sun_circle.get_center())
            ray.shift(ray.get_center() - ORIGIN + 
                     0.5 * (ray.get_end() - ray.get_start()))
        sun_reading = Text("High", color=YELLOW, font_size=28)
        sun_reading.next_to(sun_circle, UP, buff=0.4)
        sun_label = Text("Sunlight", font_size=20, color=WHITE)
        sun_label.next_to(sun_circle, DOWN, buff=0.5)
        sun_group.add(sun_circle, sun_rays, sun_reading, sun_label)
        sun_group.shift(LEFT * 1.5 + UP * 0.5)
        
        # Time of day (clock)
        clock_group = VGroup()
        clock_circle = Circle(radius=0.5, color=BLUE_D, fill_opacity=0.8, stroke_color=WHITE, stroke_width=3)
        hour_hand = Line(ORIGIN, UP * 0.25, color=WHITE, stroke_width=4)
        minute_hand = Line(ORIGIN, UP * 0.35, color=WHITE, stroke_width=3).rotate(-PI/3)
        hour_hand.move_to(clock_circle.get_center())
        minute_hand.move_to(clock_circle.get_center())
        time_reading = Text("2 PM", color=BLUE_D, font_size=28)
        time_reading.next_to(clock_circle, UP, buff=0.4)
        time_label = Text("Time of Day", font_size=20, color=WHITE)
        time_label.next_to(clock_circle, DOWN, buff=0.5)
        clock_group.add(clock_circle, hour_hand, minute_hand, time_reading, time_label)
        clock_group.shift(RIGHT * 1.8 + UP * 0.5)
        
        # AC unit (output)
        ac_group = VGroup()
        ac_box = Rectangle(width=1.2, height=0.8, color=BLUE, fill_opacity=0.7, stroke_width=3)
        ac_label = Text("AC", color=WHITE, font_size=32, weight=BOLD).move_to(ac_box)
        ac_status = Text("???", color=YELLOW, font_size=24)
        ac_status.next_to(ac_box, DOWN, buff=0.3)
        ac_group.add(ac_box, ac_label, ac_status)
        ac_group.shift(RIGHT * 4.5 + UP * 0.5)
        
        self.play(
            LaggedStart(
                FadeIn(temp_group),
                FadeIn(sun_group),
                FadeIn(clock_group),
                FadeIn(ac_group),
                lag_ratio=0.4
            )
        )
        self.wait(2)
        
        self.play(FadeOut(scenario))
        self.wait(0.3)
        
        # PART 2: Show the neuron with weights
        neuron_title = Text("The Neuron Analyzes Each Input", font_size=28, color=GREEN)
        neuron_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(neuron_title))
        self.wait(0.5)
        
        # Create neuron in center
        neuron = Circle(radius=0.6, color=YELLOW, fill_opacity=0.9)
        neuron_label = Text("Decision\nNeuron", font_size=18, color=BLACK, line_spacing=1)
        neuron_label.move_to(neuron)
        neuron_group = VGroup(neuron, neuron_label)
        neuron_group.shift(DOWN * 1.5)
        
        self.play(FadeIn(neuron_group))
        self.wait(0.5)
        
        # Connect inputs to neuron with arrows and weights
        # Temperature connection (strong positive)
        temp_arrow = Arrow(temp_group.get_bottom(), neuron.get_left() + UP * 0.4, 
                          buff=0.1, color=RED, stroke_width=8)
        temp_weight = MathTex("w_1 = +2.5", color=RED, font_size=24)
        temp_weight.next_to(temp_arrow, LEFT, buff=0.1)
        temp_importance = Text("STRONG\npositive", font_size=16, color=RED, line_spacing=1)
        temp_importance.next_to(temp_weight, DOWN, buff=0.2)
        
        self.play(
            GrowArrow(temp_arrow),
            Write(temp_weight)
        )
        self.play(Write(temp_importance))
        self.wait(1)
        
        # Sunlight connection (smaller positive)
        sun_arrow = Arrow(sun_group.get_bottom(), neuron.get_top() + LEFT * 0.2, 
                         buff=0.1, color=YELLOW, stroke_width=5)
        sun_weight = MathTex("w_2 = +0.8", color=YELLOW, font_size=24)
        sun_weight.next_to(sun_arrow, UP, buff=0.1)
        sun_importance = Text("smaller\npositive", font_size=16, color=YELLOW, line_spacing=1)
        sun_importance.next_to(sun_weight, LEFT, buff=0.2)
        
        self.play(
            GrowArrow(sun_arrow),
            Write(sun_weight)
        )
        self.play(Write(sun_importance))
        self.wait(1)
        
        # Time connection (negative at night)
        time_arrow = Arrow(clock_group.get_bottom(), neuron.get_right() + UP * 0.3, 
                          buff=0.1, color=BLUE, stroke_width=4)
        time_weight = MathTex("w_3 = +0.5", color=BLUE, font_size=24)
        time_weight.next_to(time_arrow, RIGHT, buff=0.1)
        time_importance = Text("positive\n(daytime)", font_size=16, color=BLUE, line_spacing=1)
        time_importance.next_to(time_weight, DOWN, buff=0.2)
        
        self.play(
            GrowArrow(time_arrow),
            Write(time_weight)
        )
        self.play(Write(time_importance))
        self.wait(1)
        
        # Bias (comfort level)
        bias_arrow = Arrow(neuron.get_bottom() + DOWN * 0.5, neuron.get_bottom(), 
                          buff=0.1, color=PURPLE, stroke_width=5)
        bias_label = MathTex("b = -15", color=PURPLE, font_size=24)
        bias_label.next_to(bias_arrow, DOWN, buff=0.1)
        bias_desc = Text("Base comfort\nlevel (24°C)", font_size=16, color=PURPLE, line_spacing=1)
        bias_desc.next_to(bias_label, DOWN, buff=0.2)
        
        self.play(
            GrowArrow(bias_arrow),
            Write(bias_label)
        )
        self.play(Write(bias_desc))
        self.wait(2)
        
        # Clear annotations but keep structure
        self.play(*[FadeOut(mob) for mob in [
            temp_importance, sun_importance, time_importance, bias_desc, neuron_title
        ]])
        self.wait(0.3)
        
        # PART 3: Show the calculation
        calc_title = Text("Computing the Weighted Sum", font_size=28, color=ORANGE)
        calc_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(calc_title))
        self.wait(0.5)
        
        # Show equation building up
        equation = MathTex(
            "z", "=", "w_1", "x_1", "+", "w_2", "x_2", "+", "w_3", "x_3", "+", "b"
        )
        equation.scale(1.1)
        equation.to_edge(LEFT, buff=0.5).shift(DOWN * 3.2)
        
        self.play(Write(equation))
        self.wait(0.5)
        
        # Substitute values
        values = MathTex(
            "z", "=", "(2.5)(32)", "+", "(0.8)(0.7)", "+", "(0.5)(0.8)", "+", "(-15)"
        )
        values.scale(1.0)
        values.next_to(equation, DOWN, buff=0.4)
        
        self.play(Write(values))
        self.wait(1)
        
        # Calculate
        step1 = MathTex("z", "=", "80", "+", "0.56", "+", "0.4", "+", "(-15)")
        step1.scale(1.0)
        step1.next_to(values, DOWN, buff=0.3)
        
        self.play(Write(step1))
        self.wait(0.8)
        
        result = MathTex("z", "=", "65.96")
        result.scale(1.2)
        result.next_to(step1, DOWN, buff=0.3)
        result_box = SurroundingRectangle(result, color=ORANGE, buff=0.15)
        
        self.play(Write(result), Create(result_box))
        self.wait(1)
        
        # Show z value on neuron
        z_display = MathTex("z = 65.96", color=BLACK, font_size=20)
        z_display.move_to(neuron)
        
        self.play(
            FadeOut(neuron_label),
            FadeIn(z_display),
            neuron.animate.set_fill(ORANGE, opacity=0.9)
        )
        self.wait(1)
        
        self.play(FadeOut(calc_title))
        self.wait(0.3)
        
        # PART 4: Apply activation function
        activation_title = Text("Apply Activation: Make the Decision", font_size=28, color=GREEN)
        activation_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(activation_title))
        self.wait(0.5)
        
        # Show activation function
        activation_arrow = Arrow(neuron.get_right(), neuron.get_right() + RIGHT * 1.5,
                                color=GREEN, stroke_width=5, buff=0.1)
        activation_label = MathTex("\\sigma(z)", color=GREEN, font_size=28)
        activation_label.next_to(activation_arrow, UP, buff=0.1)
        
        self.play(GrowArrow(activation_arrow), Write(activation_label))
        self.wait(0.5)
        
        # Output node
        output_circle = Circle(radius=0.5, color=GREEN, fill_opacity=0.9)
        output_value = MathTex("y \\approx 1.0", color=BLACK, font_size=24)
        output_value.move_to(output_circle)
        output_node = VGroup(output_circle, output_value)
        output_node.next_to(activation_arrow, RIGHT, buff=0.1)
        
        self.play(FadeIn(output_node))
        self.wait(0.5)
        
        # Decision interpretation
        decision_arrow = Arrow(output_node.get_right(), ac_group.get_left(),
                              color=GREEN, stroke_width=5, buff=0.2)
        
        self.play(GrowArrow(decision_arrow))
        
        # Update AC status
        new_ac_status = Text("ON", color=GREEN, font_size=32, weight=BOLD)
        new_ac_status.next_to(ac_box, DOWN, buff=0.3)
        
        self.play(
            FadeOut(ac_status),
            FadeIn(new_ac_status),
            ac_box.animate.set_fill(GREEN, opacity=0.8)
        )
        self.wait(1)
        
        decision_text = Text("Output ≈ 1 → AC turns ON!", font_size=26, color=GREEN)
        decision_text.next_to(output_node, DOWN, buff=0.5)
        self.play(Write(decision_text))
        self.wait(2)
        
        # Clear for scenario change
        self.play(*[FadeOut(mob) for mob in [
            equation, values, step1, result, result_box,
            activation_arrow, activation_label, output_node, decision_arrow,
            decision_text, activation_title
        ]])
        self.wait(0.5)
        
        # PART 5: Different scenario - nighttime
        scenario2_title = Text("Different Scenario: Late at Night", font_size=28, color=BLUE_D)
        scenario2_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(scenario2_title))
        self.wait(0.5)
        
        # Update inputs
        new_temp = MathTex("25°C", color=RED, font_size=32)
        new_temp.move_to(temp_reading)
        
        new_sun = Text("None", color=GRAY, font_size=28)
        new_sun.move_to(sun_reading)
        
        new_time = Text("11 PM", color=BLUE_D, font_size=28)
        new_time.move_to(time_reading)
        
        # Update clock hands to show night
        new_hour_hand = Line(ORIGIN, DOWN * 0.2, color=WHITE, stroke_width=4)
        new_hour_hand.move_to(clock_circle.get_center())
        new_minute_hand = Line(ORIGIN, LEFT * 0.35, color=WHITE, stroke_width=3)
        new_minute_hand.move_to(clock_circle.get_center())
        
        # Update weight for nighttime (negative)
        new_time_weight = MathTex("w_3 = -1.2", color=BLUE, font_size=24)
        new_time_weight.move_to(time_weight)
        
        self.play(
            Transform(temp_reading, new_temp),
            Transform(sun_reading, new_sun),
            sun_group.animate.set_opacity(0.3),
            Transform(time_reading, new_time),
            Transform(hour_hand, new_hour_hand),
            Transform(minute_hand, new_minute_hand),
            Transform(time_weight, new_time_weight),
            time_arrow.animate.set_color(ORANGE)
        )
        self.wait(1)
        
        # New calculation
        new_values = MathTex(
            "z", "=", "(2.5)(25)", "+", "(0.8)(0)", "+", "(-1.2)(0.9)", "+", "(-15)"
        )
        new_values.scale(0.95)
        new_values.to_edge(LEFT, buff=0.5).shift(DOWN * 3.2)
        
        self.play(Write(new_values))
        self.wait(0.8)
        
        new_result = MathTex("z", "=", "47.42")
        new_result.scale(1.2)
        new_result.next_to(new_values, DOWN, buff=0.3)
        new_result_box = SurroundingRectangle(new_result, color=BLUE, buff=0.15)
        
        self.play(Write(new_result), Create(new_result_box))
        self.wait(1)
        
        # Still high, AC still on
        new_z_display = MathTex("z = 47.42", color=BLACK, font_size=20)
        new_z_display.move_to(neuron)
        
        new_output_text = Text("y ≈ 1.0 → Still ON\n(But close to threshold!)", 
                              font_size=24, color=YELLOW, line_spacing=1.2)
        new_output_text.next_to(ac_group, DOWN, buff=0.8)
        
        self.play(
            Transform(z_display, new_z_display),
            Write(new_output_text)
        )
        self.wait(2)
        
        # Final explanation
        self.play(*[FadeOut(mob) for mob in [new_values, new_result, new_result_box, scenario2_title]])
        
        final_explanation = Text(
            "The neuron weighs all inputs,\napplies learned weights and bias,\nand makes an intelligent decision!",
            font_size=26,
            color=GOLD,
            line_spacing=1.3
        )
        final_explanation.next_to(title, DOWN, buff=0.8)
        
        self.play(Write(final_explanation))
        self.wait(3)
        
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

class IntroText(Scene):
    def construct(self):
        intro_text = Text("Neural Networks", font_size=36, color=WHITE)
        self.play(Write(intro_text))
        self.wait(3)
        self.play(FadeOut(intro_text))
        self.wait(1)

class IntroNeuronOverview(Scene):
    def construct(self):
        # Title
        title = Text("The Fundamental Building Block", font_size=32, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Simple neuron diagram
        neuron = Circle(radius=0.8, color=YELLOW, fill_opacity=0.8, stroke_width=4)
        neuron_label = Text("Neuron", font_size=28, color=BLACK, weight=BOLD)
        neuron_label.move_to(neuron)
        neuron_group = VGroup(neuron, neuron_label)
        
        self.play(GrowFromCenter(neuron_group))
        self.wait(1)
        
        # Inputs appearing from left
        input_text = Text("Inputs", font_size=20, color=BLUE)
        input_text.shift(LEFT * 4.5)
        
        input_arrows = VGroup()
        for i in range(3):
            arrow = Arrow(LEFT * 3.5 + UP * (1 - i), neuron.get_left() + UP * (0.5 - i * 0.5),
                         buff=0.1, color=BLUE, stroke_width=3)
            input_arrows.add(arrow)
        
        self.play(
            Write(input_text),
            LaggedStart(*[GrowArrow(arrow) for arrow in input_arrows], lag_ratio=0.2)
        )
        self.wait(0.8)
        
        # Show weights
        weight_labels = VGroup()
        for i, arrow in enumerate(input_arrows):
            weight = Text("w", font_size=18, color=GREEN)
            weight.next_to(arrow, UP, buff=0.1)
            weight_labels.add(weight)
        
        weights_annotation = Text("× Weights", font_size=20, color=GREEN)
        weights_annotation.next_to(input_text, DOWN, buff=0.5)
        
        self.play(
            LaggedStart(*[FadeIn(w) for w in weight_labels], lag_ratio=0.15),
            FadeIn(weights_annotation)
        )
        self.wait(0.8)
        
        # Show bias
        bias_arrow = Arrow(neuron.get_bottom() + DOWN * 0.8, neuron.get_bottom(),
                          buff=0.1, color=PURPLE, stroke_width=3)
        bias_label = Text("+ Bias", font_size=20, color=PURPLE)
        bias_label.next_to(bias_arrow, DOWN, buff=0.1)
        
        self.play(
            GrowArrow(bias_arrow),
            Write(bias_label)
        )
        self.wait(0.8)
        
        # Output
        output_arrow = Arrow(neuron.get_right(), neuron.get_right() + RIGHT * 2,
                            buff=0.1, color=ORANGE, stroke_width=4)
        output_text = Text("Output", font_size=24, color=ORANGE)
        output_text.next_to(output_arrow, RIGHT, buff=0.2)
        
        self.play(
            GrowArrow(output_arrow),
            Write(output_text)
        )
        self.wait(1)
        
        # Fade out everything
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)
        
        # Final message
        dive_in = Text("Let's dive in!", font_size=48, color=GOLD, weight=BOLD)
        self.play(Write(dive_in, run_time=1))
        self.wait(1)
        
        self.play(FadeOut(dive_in))
        self.wait(0.5)