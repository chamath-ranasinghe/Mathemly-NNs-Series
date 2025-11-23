from manim import *
import numpy as np

class ForwardPropagation(Scene):
    def construct(self):
        # Configuration
        NEURON_RADIUS = 0.35
        LAYER_SPACING = 3.5
        INPUT_COLOR = "#3498db"  # Blue
        HIDDEN_COLOR = "#9b59b6"  # Purple
        OUTPUT_COLOR = "#e74c3c"  # Red
        CONNECTION_COLOR = "#ecf0f1"  # Light gray
        ACTIVE_CONNECTION_COLOR = "#f39c12"  # Orange
        
        # Title - "Forward Propagation"
        title = Text("Forward Propagation", font_size=48, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)
        
        # Subtitle explanation with sequential highlighting
        # Subtitle explanation with sequential highlighting
        subtitle = Text(
            "Information flows from input → hidden → output",
            font_size=32,
            color=YELLOW
        )

        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)

        # Find and highlight "input"
        input_start = subtitle.text.index("input")
        input_end = input_start + len("input")
        self.play(
            subtitle[input_start:input_end].animate.scale(1.2).set_color(YELLOW_E),
            run_time=0.5
        )
        self.wait(0.8)
        self.play(
            subtitle[input_start:input_end].animate.scale(1/1.2).set_color(YELLOW),
            run_time=0.5
        )
        self.wait(0.3)

        # Find and highlight "hidden"
        hidden_start = subtitle.text.index("hidden")
        hidden_end = hidden_start + len("hidden")
        self.play(
            subtitle[hidden_start:hidden_end].animate.scale(1.2).set_color(YELLOW_E),
            run_time=0.5
        )
        self.wait(0.8)
        self.play(
            subtitle[hidden_start:hidden_end].animate.scale(1/1.2).set_color(YELLOW),
            run_time=0.5
        )
        self.wait(0.3)

        # Find and highlight "output"
        output_start = subtitle.text.index("output")
        output_end = output_start + len("output")
        self.play(
            subtitle[output_start:output_end].animate.scale(1.2).set_color(YELLOW_E),
            run_time=0.5
        )
        self.wait(0.8)
        self.play(
            subtitle[output_start:output_end].animate.scale(1/1.2).set_color(YELLOW),
            run_time=0.5
        )
        self.wait(0.3)
        
        # Fade out title and subtitle
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.3)

        # Relay race analogy - show information flowing
        relay_text = Text(
            "Like a relay race: receive → transform → pass forward",
            font_size=32,
            color=YELLOW
        )
        self.play(FadeIn(relay_text, shift=UP))
        self.wait(6)
        self.play(FadeOut(relay_text))

        # Relay race analogy - show information flowing
        prediction = Text(
            "Last Layer : Make a Prediction!",
            font_size=32,
            color=ORANGE
        )
        self.play(FadeIn(prediction, shift=UP))
        self.wait(2)
        self.play(FadeOut(prediction))

        # Relay race analogy - show information flowing
        house_price = Text(
            "House Price Example",
            font_size=32,
            color=YELLOW
        )
        self.play(FadeIn(house_price, shift=UP))
        self.wait(1)
        self.play(FadeOut(house_price))
        
        # Create the neural network structure
        # Input layer (3 neurons)
        input_positions = [UP * 1.5, ORIGIN, DOWN * 1.5]
        input_labels = ["Size\n(sq ft)", "Bedrooms", "Location\n(distance)"]
        input_neurons = VGroup()
        input_texts = VGroup()
        
        for i, (pos, label) in enumerate(zip(input_positions, input_labels)):
            neuron = Circle(
                radius=0.6,
                color=INPUT_COLOR,
                fill_opacity=0.8,
                stroke_width=3
            ).shift(LEFT * LAYER_SPACING + pos)
            
            text = Text(label, font_size=18, color=WHITE).move_to(neuron.get_center())
            
            input_neurons.add(neuron)
            input_texts.add(text)
        
        # Hidden layer 1 (4 neurons)
        hidden1_positions = [UP * 2, UP * 0.7, DOWN * 0.7, DOWN * 2]
        hidden1_neurons = VGroup()
        
        for pos in hidden1_positions:
            neuron = Circle(
                radius=NEURON_RADIUS,
                color=HIDDEN_COLOR,
                fill_opacity=0.7,
                stroke_width=3
            ).shift(LEFT * 0.5 + pos)
            hidden1_neurons.add(neuron)
        
        # Hidden layer 2 (4 neurons)
        hidden2_positions = [UP * 2, UP * 0.7, DOWN * 0.7, DOWN * 2]
        hidden2_neurons = VGroup()
        
        for pos in hidden2_positions:
            neuron = Circle(
                radius=NEURON_RADIUS,
                color=HIDDEN_COLOR,
                fill_opacity=0.7,
                stroke_width=3
            ).shift(RIGHT * 1 + pos)
            hidden2_neurons.add(neuron)
        
        # Output layer (1 neuron)
        output_neuron = Circle(
            radius=0.6,
            color=OUTPUT_COLOR,
            fill_opacity=0.9,
            stroke_width=4
        ).shift(RIGHT * LAYER_SPACING)
        
        output_text = Text("Predicted\nPrice", font_size=20, color=WHITE).move_to(output_neuron.get_center())
        
        # Create all connections
        all_connections = VGroup()
        
        # Input to Hidden1
        input_to_hidden1 = VGroup()
        for input_n in input_neurons:
            for hidden_n in hidden1_neurons:
                line = Line(
                    input_n.get_right(),
                    hidden_n.get_left(),
                    color=CONNECTION_COLOR,
                    stroke_width=1,
                    stroke_opacity=0.3
                )
                input_to_hidden1.add(line)
                all_connections.add(line)
        
        # Hidden1 to Hidden2
        hidden1_to_hidden2 = VGroup()
        for h1 in hidden1_neurons:
            for h2 in hidden2_neurons:
                line = Line(
                    h1.get_right(),
                    h2.get_left(),
                    color=CONNECTION_COLOR,
                    stroke_width=1,
                    stroke_opacity=0.3
                )
                hidden1_to_hidden2.add(line)
                all_connections.add(line)
        
        # Hidden2 to Output
        hidden2_to_output = VGroup()
        for hidden_n in hidden2_neurons:
            line = Line(
                hidden_n.get_right(),
                output_neuron.get_left(),
                color=CONNECTION_COLOR,
                stroke_width=1,
                stroke_opacity=0.3
            )
            hidden2_to_output.add(line)
            all_connections.add(line)
        
        # Draw the network
        self.play(
            Create(all_connections),
            run_time=1.0
        )
        self.play(
            LaggedStart(
                *[Create(neuron) for neuron in input_neurons],
                lag_ratio=0.2
            ),
            run_time=1
        )
        self.play(
            LaggedStart(
                *[Write(text) for text in input_texts],
                lag_ratio=0.2
            ),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(
            LaggedStart(
                *[Create(neuron) for neuron in hidden1_neurons],
                lag_ratio=0.15
            ),
            run_time=0.8
        )
        self.play(
            LaggedStart(
                *[Create(neuron) for neuron in hidden2_neurons],
                lag_ratio=0.15
            ),
            run_time=0.8
        )
        self.play(Create(output_neuron), Write(output_text))
        self.wait(1)
        
        # Animate the forward propagation flow
        # Create flowing particles/signals
        def create_flow_animation(start_neurons, end_neurons, connections):
            animations = []
            dots = VGroup()
            
            for i, start_n in enumerate(start_neurons):
                for j, end_n in enumerate(end_neurons):
                    # Create a dot that travels along the connection
                    dot = Dot(
                        point=start_n.get_center(),
                        color=ACTIVE_CONNECTION_COLOR,
                        radius=0.08
                    )
                    dots.add(dot)
                    
                    # Animate dot moving from start to end
                    animations.append(
                        dot.animate.move_to(end_n.get_center())
                    )
            
            return dots, animations
        
        # Flow from input to hidden1
        flow_label1 = Text("Input Layer", font_size=24, color=INPUT_COLOR).to_edge(UP, buff=0.4)
        self.play(FadeIn(flow_label1))
        
        # Pulse input neurons
        self.play(
            *[neuron.animate.set_fill(INPUT_COLOR, opacity=1).scale(1.15) for neuron in input_neurons],
            run_time=0.4
        )
        self.play(
            *[neuron.animate.set_fill(INPUT_COLOR, opacity=0.8).scale(1/1.15) for neuron in input_neurons],
            run_time=0.4
        )
        self.wait(0.3)
        
        # Show flow to hidden layer 1
        self.play(
            FadeOut(flow_label1),
            FadeIn(Text("Hidden Layer 1", font_size=24, color=HIDDEN_COLOR).to_edge(UP, buff=0.4))
        )
        
        dots1, flow_anims1 = create_flow_animation(input_neurons, hidden1_neurons, input_to_hidden1)
        self.add(dots1)
        self.play(*flow_anims1, run_time=1.2)
        self.play(
            *[neuron.animate.set_fill(HIDDEN_COLOR, opacity=1).scale(1.1) for neuron in hidden1_neurons],
            FadeOut(dots1),
            run_time=0.3
        )
        self.play(
            *[neuron.animate.set_fill(HIDDEN_COLOR, opacity=0.7).scale(1/1.1) for neuron in hidden1_neurons],
            run_time=0.3
        )
        self.wait(0.3)
        
        # Flow to hidden layer 2
        self.play(
            FadeOut(VGroup(*[mob for mob in self.mobjects if isinstance(mob, Text) and mob.text == "Hidden Layer 1"])),
            FadeIn(Text("Hidden Layer 2", font_size=24, color=HIDDEN_COLOR).to_edge(UP, buff=0.4))
        )
        
        dots2, flow_anims2 = create_flow_animation(hidden1_neurons, hidden2_neurons, hidden1_to_hidden2)
        self.add(dots2)
        self.play(*flow_anims2, run_time=1.2)
        self.play(
            *[neuron.animate.set_fill(HIDDEN_COLOR, opacity=1).scale(1.1) for neuron in hidden2_neurons],
            FadeOut(dots2),
            run_time=0.3
        )
        self.play(
            *[neuron.animate.set_fill(HIDDEN_COLOR, opacity=0.7).scale(1/1.1) for neuron in hidden2_neurons],
            run_time=0.3
        )
        
        # Flow to output - "crossing the finish line"
        finish_text = Text(
            "Crossing the finish line! 🏁",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN, buff=0.4)
        self.play(
            FadeOut(VGroup(*[mob for mob in self.mobjects if isinstance(mob, Text) and mob.text == "Hidden Layer 2"])),
            FadeIn(finish_text)
        )
        
        dots3, flow_anims3 = create_flow_animation(hidden2_neurons, [output_neuron], hidden2_to_output)
        self.add(dots3)
        self.play(*flow_anims3, run_time=1.2)
        self.play(
            output_neuron.animate.set_fill(OUTPUT_COLOR, opacity=1).scale(1.2),
            FadeOut(dots3),
            run_time=0.4
        )
        
        # Show the final prediction
        self.play(FadeOut(finish_text))
        
        price_box = Rectangle(
            width=1.5,
            height=0.6,
            color=OUTPUT_COLOR,
            fill_opacity=0.2,
            stroke_width=3
        ).next_to(output_neuron, RIGHT, buff=0.8)
        
        price_text = Text("$120,000", font_size=20, weight=BOLD, color=OUTPUT_COLOR).move_to(price_box.get_center())
        
        self.play(
            Create(price_box),
            Write(price_text),
            run_time=1
        )
        self.wait(0.5)
        
        # Add arrow pointing to the prediction
        arrow = Arrow(
            output_neuron.get_right(),
            price_box.get_left(),
            color=YELLOW,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15
        )
        self.play(GrowArrow(arrow))
        self.wait(2)
        
        # Final celebration effect
        self.play(
            Flash(price_box, color=YELLOW, flash_radius=1.5, line_length=0.5),
            output_neuron.animate.set_fill(OUTPUT_COLOR, opacity=1),
            run_time=0.8
        )
        self.wait(2)

class LayerDeepDive(Scene):
    def construct(self):
        # Color scheme
        INPUT_COLOR = "#3498db"  # Blue
        NEURON_COLOR = "#9b59b6"  # Purple
        OUTPUT_COLOR = "#2ecc71"  # Green
        WEIGHT_COLOR = "#e67e22"  # Orange
        BIAS_COLOR = "#e74c3c"  # Red
        ACTIVATION_COLOR = "#f39c12"  # Yellow
        
        # Title
        title = Text("Inside a Neural Network Layer", font_size=44, weight=BOLD)
        self.play(Write(title))
        self.wait(6)
        self.play(FadeOut(title))
        
        # ===== PART 1: Show the layer structure =====
        subtitle1 = Text("Each layer contains multiple neurons", font_size=32, color=GRAY)
        subtitle1.to_edge(UP, buff=0.4)
        self.play(FadeIn(subtitle1, shift=DOWN))
        self.wait(0.5)
        
        # Create 3 inputs
        input_values = [2000, 3, 5]  # size, bedrooms, distance
        input_labels = ["Size", "Bedrooms", "Distance"]
        input_circles = VGroup()
        input_texts = VGroup()
        
        for i, (val, label) in enumerate(zip(input_values, input_labels)):
            circle = Circle(radius=0.5, color=INPUT_COLOR, fill_opacity=0.8, stroke_width=3)
            circle.shift(LEFT * 5 + UP * (2 - i * 2))
            text = Text(label, font_size=16, color=WHITE).move_to(circle.get_center())
            input_circles.add(circle)
            input_texts.add(text)
        
        self.play(
            LaggedStart(*[Create(c) for c in input_circles], lag_ratio=0.2),
            run_time=1
        )
        self.play(
            LaggedStart(*[Write(t) for t in input_texts], lag_ratio=0.2),
            run_time=1
        )
        self.wait(1)
        
        # Create 3 neurons in the layer
        neuron_circles = VGroup()
        neuron_labels = ["Neuron 1", "Neuron 2", "Neuron 3"]
        
        for i, label in enumerate(neuron_labels):
            circle = Circle(radius=0.45, color=NEURON_COLOR, fill_opacity=0.7, stroke_width=3)
            circle.shift(RIGHT * 1 + UP * (2 - i * 2))
            neuron_circles.add(circle)
        
        # Draw connections from inputs to neurons
        connections = VGroup()
        for inp in input_circles:
            for neuron in neuron_circles:
                line = Line(
                    inp.get_right(), 
                    neuron.get_left(),
                    color=WHITE,
                    stroke_width=1.5,
                    stroke_opacity=0.3
                )
                connections.add(line)
        
        self.play(Create(connections), run_time=1)
        self.play(
            LaggedStart(*[Create(n) for n in neuron_circles], lag_ratio=0.2),
            run_time=1
        )
        self.wait(9)

        neuron_1_focus = Text("Size of the house", font_size=18, color=YELLOW).next_to(neuron_circles[0], RIGHT, buff=0.6)
        neuron_2_focus = Text("Number of bedrooms", font_size=18, color=YELLOW).next_to(neuron_circles[1], RIGHT, buff=0.6)
        neuron_3_focus = Text("Distance from city", font_size=18, color=YELLOW).next_to(neuron_circles[2], RIGHT, buff=0.6)

        self.play(FadeIn(neuron_1_focus, shift=LEFT))
        self.wait(1.5)
        self.play(FadeIn(neuron_2_focus, shift=LEFT))
        self.wait(1.5)
        self.play(FadeIn(neuron_3_focus, shift=LEFT))
        self.wait(0.3)
        self.play(FadeOut(VGroup(neuron_1_focus, neuron_2_focus, neuron_3_focus)))

        # ===== PART 2: Zoom into one neuron =====
        self.play(FadeOut(subtitle1))
        zoom_text = Text("Let's zoom into one neuron...", font_size=32, color=YELLOW)
        zoom_text.to_edge(UP, buff=0.4)
        self.play(FadeIn(zoom_text, shift=DOWN))
        
        # Highlight the first neuron
        highlight = Circle(radius=0.55, color=YELLOW, stroke_width=5)
        highlight.move_to(neuron_circles[0].get_center())
        self.play(Create(highlight), run_time=0.5)
        self.play(Flash(neuron_circles[0], color=YELLOW, flash_radius=0.8))
        
        # Fade out everything except the highlighted neuron and its inputs
        fade_group = VGroup(
            neuron_circles[1], neuron_circles[2],
            *[connections[i] for i in range(len(connections)) if i in [1,2,4,5,7,8]]
        )
        self.play(FadeOut(fade_group), FadeOut(zoom_text), FadeOut(highlight))
        self.wait(0.5)
        
        # ===== PART 3: Show the weighted sum calculation =====
        calc_title = Text("Step 1: Calculate Weighted Sum", font_size=32, color=WEIGHT_COLOR)
        calc_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(calc_title, shift=DOWN))
        self.wait(0.5)
        
        # Move everything to the left to make room for the formula
        main_group = VGroup(input_circles, input_texts, neuron_circles[0], 
                           *[connections[i] for i in range(0, 8, 3)])
        self.play(main_group.animate.shift(LEFT * 1), run_time=1)
        
        # Show the formula on the right
        formula_title = Text("z = ", font_size=32, color=WHITE).shift(LEFT + DOWN * 0.5)
        
        # Build the formula step by step
        weights = [0.5, 0.3, -0.4]  # example weights
        bias = 100
        
        term1 = MathTex(r"w_1 \times \text{size}", font_size=30, color=WEIGHT_COLOR)
        term1.next_to(formula_title, RIGHT, buff=0.2)
        
        self.play(Write(formula_title), Write(term1))
        
        # Highlight the connection
        self.play(
            connections[0].animate.set_color(WEIGHT_COLOR).set_stroke(width=4, opacity=1),
            run_time=0.5
        )
        self.wait(1.0)
        
        plus1 = MathTex(r"+", font_size=30).next_to(term1, RIGHT, buff=0.2)
        term2 = MathTex(r"w_2 \times \text{bedrooms}", font_size=30, color=WEIGHT_COLOR)
        term2.next_to(plus1, RIGHT, buff=0.2)
        
        self.play(Write(plus1), Write(term2))
        self.play(
            connections[3].animate.set_color(WEIGHT_COLOR).set_stroke(width=4, opacity=1),
            run_time=0.5
        )
        self.wait(1.0)
        
        plus2 = MathTex(r"+", font_size=30).next_to(term2, RIGHT, buff=0.2)
        term3 = MathTex(r"w_3 \times \text{distance}", font_size=30, color=WEIGHT_COLOR)
        term3.next_to(plus2, RIGHT, buff=0.2)
        
        self.play(Write(plus2), Write(term3))
        self.play(
            connections[6].animate.set_color(WEIGHT_COLOR).set_stroke(width=4, opacity=1),
            run_time=0.5
        )
        self.wait(0.3)
        
        plus3 = MathTex(r"+", font_size=30).next_to(term3, RIGHT, buff=0.2)
        bias_term = MathTex(r"b", font_size=30, color=BIAS_COLOR)
        bias_term.next_to(plus3, RIGHT, buff=0.2)
        
        self.play(Write(plus3), Write(bias_term))
        self.wait(0.5)
        
        # Show actual calculation with values
        formula_group = VGroup(formula_title, term1, plus1, term2, plus2, term3, plus3, bias_term)
        
        # Calculate result
        z_value = 0.5 * 2000 + 0.3 * 3 + (-0.4) * 5 + 100
        
        # Show z value entering the neuron
        self.play(
            FadeOut(formula_group),
        )

        # ===== PART 4: Weights as importance scores =====
        self.play(FadeOut(calc_title))
        
        importance_title = Text("Weights = Importance Scores", font_size=32, color=WEIGHT_COLOR)
        importance_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(importance_title, shift=DOWN))
        self.wait(0.5)
        
        # Show weight annotations
        weight_annotations = VGroup()
        
        # Large positive weight for size
        w1_label = Text("w₁ = +0.5\nLarge → Higher price", font_size=18, color=GREEN)
        w1_label.next_to(connections[0], UP, buff=0.1)
        w1_arrow = Arrow(w1_label.get_bottom(), connections[0].get_center(), 
                        color=GREEN, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        
        self.play(
            Write(w1_label),
            GrowArrow(w1_arrow),
            connections[0].animate.set_color(GREEN).set_stroke(width=5)
        )
        self.wait(6)
        
        # Negative weight for distance
        w3_label = Text("w₃ = -0.4\nNegative → Lower price", font_size=18, color=RED)
        w3_label.next_to(connections[6], DOWN, buff=0.1)
        w3_arrow = Arrow(w3_label.get_top(), connections[6].get_center(),
                        color=RED, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        
        self.play(
            Write(w3_label),
            GrowArrow(w3_arrow),
            connections[6].animate.set_color(RED).set_stroke(width=5)
        )
        self.wait(6)
        
        # Bias explanation
        bias_label = Text("Bias: flexibility\neven with small inputs", font_size=18, color=BIAS_COLOR)
        bias_label.next_to(neuron_circles[0], DOWN, buff=0.8)
        bias_arrow = Arrow(bias_label.get_top(), neuron_circles[0].get_bottom(),
                          color=BIAS_COLOR, stroke_width=3, max_tip_length_to_length_ratio=0.2)
        
        self.play(
            Write(bias_label),
            GrowArrow(bias_arrow)
        )
        self.wait(9)
        
        # Fade out annotations
        self.play(
            FadeOut(VGroup(w1_label, w1_arrow, w3_label, w3_arrow, bias_label, bias_arrow)),
            FadeOut(importance_title)
        )
        
        # ===== PART 5: Activation function =====
        activation_title = Text("Step 2: Apply Activation Function", font_size=32, color=ACTIVATION_COLOR)
        activation_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(activation_title, shift=DOWN))
        self.wait(0.5)
        
        # Create activation function visualization (ReLU graph)
        axes = Axes(
            x_range=[-2, 5, 1],
            y_range=[-1, 5, 1],
            x_length=4,
            y_length=3,
            axis_config={"include_tip": True, "color": GRAY},
        ).shift(RIGHT * 3 + DOWN * 0.5).scale(0.8)
        
        # ReLU function
        relu_graph = axes.plot(lambda x: max(0, x), color=ACTIVATION_COLOR, stroke_width=4)
        
        graph_label = Text("ReLU(z)", font_size=24, color=ACTIVATION_COLOR)
        graph_label.next_to(axes, UP, buff=0.2)
        
        filter_text = Text("Acts like a filter", font_size=22, color=GRAY)
        filter_text.next_to(axes, DOWN, buff=0.3)
        
        self.play(
            Create(axes),
            Create(relu_graph),
            Write(graph_label)
        )
        self.wait(0.5)
        self.play(Write(filter_text))
        self.wait(1)
        
        # Show z value on the graph
        z_dot = Dot(axes.c2p(z_value, max(0, z_value)), color=YELLOW, radius=0.1)
        z_line = DashedLine(
            axes.c2p(z_value, 0),
            axes.c2p(z_value, max(0, z_value)),
            color=YELLOW,
            stroke_width=3
        )
        
        output_value = max(0, z_value)
        output_label = MathTex(f"\\text{{Output}} = {output_value:.1f}", font_size=28, color=GREEN)
        output_label.next_to(z_dot, RIGHT, buff=0.3)
        
        self.play(
            Create(z_line),
            Create(z_dot),
            Write(output_label)
        )
        self.wait(25)
        
        # Show the output leaving the neuron
        self.play(
            FadeOut(VGroup(axes, relu_graph, graph_label, filter_text, z_line, z_dot, output_label)),
            FadeOut(activation_title)
        )
        
        # Create output from neuron
        output_circle = Circle(radius=0.6, color=OUTPUT_COLOR, fill_opacity=0.8, stroke_width=3)
        output_circle.shift(RIGHT * 4.5 + UP * 2)
        output_text = Text(f"Result", font_size=22, color=WHITE).move_to(output_circle.get_center())
        
        output_connection = Arrow(
            neuron_circles[0].get_right(),
            output_circle.get_left(),
            color=OUTPUT_COLOR,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        
        passes_text = Text("Signal passes through", font_size=28, color=OUTPUT_COLOR)
        passes_text.to_edge(UP, buff=0.4)
        self.play(FadeIn(passes_text, shift=DOWN))
        
        self.play(
            GrowArrow(output_connection),
            neuron_circles[0].animate.set_fill(OUTPUT_COLOR, opacity=0.5)
        )
        self.play(
            Create(output_circle),
            Write(output_text)
        )
        self.wait(1.5)
        
        # ===== PART 6: Show all neurons working together =====
        self.play(
            FadeOut(passes_text),
            FadeOut(VGroup(output_connection, output_circle, output_text))
        )
        
        team_title = Text("All neurons work together", font_size=32, color=YELLOW)
        team_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(team_title, shift=DOWN))
        self.wait(0.5)
        
        # Bring back all neurons
        self.play(
            main_group.animate.shift(RIGHT * 1),  # Move back to center
            FadeIn(neuron_circles[1]),
            FadeIn(neuron_circles[2]),
            FadeIn(VGroup(*[connections[i] for i in [1,2,4,5,7,8]]))
        )
        
        # Reset colors
        for conn in connections:
            conn.set_color(WHITE).set_stroke(width=1.5, opacity=0.3)
        
        neuron_circles[0].set_fill(NEURON_COLOR, opacity=0.7)
        self.wait(0.5)
        
        # Show all neurons processing simultaneously
        self.play(
            *[neuron.animate.set_fill(ACTIVATION_COLOR, opacity=0.8).scale(1.1) 
              for neuron in neuron_circles],
            run_time=0.6
        )
        self.play(
            *[neuron.animate.set_fill(NEURON_COLOR, opacity=0.7).scale(1/1.1) 
              for neuron in neuron_circles],
            run_time=0.6
        )
        self.wait(0.5)
        
        # Create outputs from all neurons
        output_circles = VGroup()
        output_texts = VGroup()
        output_connections = VGroup()
        
        output_values_display = ["Result 1", "Result 2", "Result 3"]  # Different outputs
        
        for i, (neuron, val) in enumerate(zip(neuron_circles, output_values_display)):
            out_circle = Circle(radius=0.6, color=OUTPUT_COLOR, fill_opacity=0.8, stroke_width=3)
            out_circle.shift(RIGHT * 4.5 + UP * (2 - i * 2))
            out_text = Text(f"{val}", font_size=20, color=WHITE).move_to(out_circle.get_center())
            out_conn = Arrow(
                neuron.get_right(),
                out_circle.get_left(),
                color=OUTPUT_COLOR,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            output_circles.add(out_circle)
            output_texts.add(out_text)
            output_connections.add(out_conn)
        
        self.play(
            LaggedStart(*[GrowArrow(conn) for conn in output_connections], lag_ratio=0.2),
            run_time=1
        )
        self.play(
            LaggedStart(*[Create(c) for c in output_circles], lag_ratio=0.2),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[Write(t) for t in output_texts], lag_ratio=0.2),
            run_time=0.8
        )
        self.wait(1)
        
        # Show these outputs become inputs for next layer
        self.play(FadeOut(team_title))
        next_layer_text = Text("These become inputs for the next layer", font_size=28, color=GREEN)
        next_layer_text.to_edge(UP, buff=0.4)
        self.play(FadeIn(next_layer_text, shift=DOWN))
        
        # Create next layer preview (small neurons)
        next_layer_neurons = VGroup()
        for i in range(3):
            small_neuron = Circle(radius=0.3, color=NEURON_COLOR, fill_opacity=0.5, stroke_width=2)
            small_neuron.shift(RIGHT * 6.5 + UP * (1.5 - i * 1.5))
            next_layer_neurons.add(small_neuron)
        
        # Connections to next layer
        next_connections = VGroup()
        for out_c in output_circles:
            for next_n in next_layer_neurons:
                line = Line(
                    out_c.get_right(),
                    next_n.get_left(),
                    color=GREEN,
                    stroke_width=2,
                    stroke_opacity=0.4
                )
                next_connections.add(line)
        
        self.play(
            Create(next_connections),
            LaggedStart(*[Create(n) for n in next_layer_neurons], lag_ratio=0.15),
            run_time=1.5
        )
        self.wait(1.5)
        
        # Final emphasis on transformation
        transform_text = Text("Layer by layer, data transforms", font_size=28, color=YELLOW)
        transform_text.next_to(next_layer_text, DOWN)
        self.play(FadeIn(transform_text, shift=UP))
        self.wait(1)
        
        # Show flow animation
        flow_dots = VGroup()
        for out_c in output_circles:
            dot = Dot(out_c.get_center(), color=YELLOW, radius=0.08)
            flow_dots.add(dot)
        
        self.play(
            *[dot.animate.move_to(next_layer_neurons[i % 3].get_center()) 
              for i, dot in enumerate(flow_dots)],
            run_time=1.5
        )
        self.play(
            *[neuron.animate.set_fill(YELLOW, opacity=1).scale(1.15) 
              for neuron in next_layer_neurons],
            FadeOut(flow_dots),
            run_time=0.5
        )
        self.wait(2)
        
        # Final message
        final_text = Text(
            "Each neuron focuses on different aspects,\nworking together to extract patterns",
            font_size=26,
            color=WHITE,
            line_spacing=1.2
        )
        final_text.move_to(ORIGIN)
        
        self.play(
            FadeOut(VGroup(
                input_circles, input_texts, neuron_circles,
                connections, output_circles, output_texts, output_connections,
                next_layer_neurons, next_connections,
                next_layer_text, transform_text
            ))
        )
        self.play(Write(final_text))
        self.wait(4.5)
        self.play(FadeOut(final_text))

class DeepLearningAbstraction(Scene):
    def construct(self):
        # Color scheme
        LAYER1_COLOR = "#3498db"  # Blue - simple patterns
        LAYER2_COLOR = "#9b59b6"  # Purple - combined patterns
        LAYER3_COLOR = "#e67e22"  # Orange - abstract patterns
        OUTPUT_COLOR = "#e74c3c"  # Red - final prediction
        INSIGHT_COLOR = "#f39c12"  # Yellow - for insights
        
        # ===== INTRODUCTION =====
        title = Text("Layer by Layer", font_size=44, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)
        
        subtitle = Text("Each layer learns more abstract features", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait(1.5)
        
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)
        
        # ===== CREATE THE NETWORK STRUCTURE =====
        # Input layer (3 neurons)
        input_layer = VGroup()
        input_labels = ["Size", "Bedrooms", "Location"]
        input_positions = [UP * 1.5, ORIGIN, DOWN * 1.5]
        
        for i, (pos, label) in enumerate(zip(input_positions, input_labels)):
            circle = Circle(radius=0.6, color=WHITE, fill_opacity=0.6, stroke_width=2)
            circle.shift(LEFT * 5 + pos)
            text = Text(label, font_size=16, color=WHITE).move_to(circle.get_center())
            group = VGroup(circle, text)
            input_layer.add(group)
        
        # Layer 1 - Simple patterns (4 neurons)
        layer1 = VGroup()
        layer1_positions = [UP * 2, UP * 0.7, DOWN * 0.7, DOWN * 2]
        
        for pos in layer1_positions:
            circle = Circle(radius=0.35, color=LAYER1_COLOR, fill_opacity=0.7, stroke_width=3)
            circle.shift(LEFT * 2.5 + pos)
            layer1.add(circle)
        
        # Layer 2 - Combined patterns (4 neurons)
        layer2 = VGroup()
        layer2_positions = [UP * 2, UP * 0.7, DOWN * 0.7, DOWN * 2]
        
        for pos in layer2_positions:
            circle = Circle(radius=0.35, color=LAYER2_COLOR, fill_opacity=0.7, stroke_width=3)
            circle.shift(RIGHT * 0.5 + pos)
            layer2.add(circle)
        
        # Layer 3 - Abstract patterns (3 neurons)
        layer3 = VGroup()
        layer3_positions = [UP * 1.2, ORIGIN, DOWN * 1.2]
        
        for pos in layer3_positions:
            circle = Circle(radius=0.35, color=LAYER3_COLOR, fill_opacity=0.7, stroke_width=3)
            circle.shift(RIGHT * 3.5 + pos)
            layer3.add(circle)
        
        # Output layer (1 neuron)
        output_neuron = Circle(radius=0.4, color=OUTPUT_COLOR, fill_opacity=0.9, stroke_width=4)
        output_neuron.shift(RIGHT * 6)
        
        # Create connections
        def create_connections(layer_from, layer_to, opacity=0.15):
            connections = VGroup()
            for neuron1 in layer_from:
                circle1 = neuron1[0] if isinstance(neuron1, VGroup) else neuron1
                for neuron2 in layer_to:
                    circle2 = neuron2[0] if isinstance(neuron2, VGroup) else neuron2
                    line = Line(
                        circle1.get_right(),
                        circle2.get_left(),
                        color=WHITE,
                        stroke_width=1,
                        stroke_opacity=opacity
                    )
                    connections.add(line)
            return connections
        
        conn_input_layer1 = create_connections(input_layer, layer1)
        conn_layer1_layer2 = create_connections(layer1, layer2)
        conn_layer2_layer3 = create_connections(layer2, layer3)
        conn_layer3_output = create_connections(layer3, [output_neuron])
        
        # Draw the entire network
        all_connections = VGroup(conn_input_layer1, conn_layer1_layer2, 
                                conn_layer2_layer3, conn_layer3_output)
        
        self.play(Create(all_connections), run_time=0.5)
        self.play(
            LaggedStart(*[Create(group) for group in input_layer], lag_ratio=0.15),
            run_time=0.5
        )
        self.play(
            LaggedStart(*[Create(neuron) for neuron in layer1], lag_ratio=0.1),
            run_time=0.5
        )
        self.play(
            LaggedStart(*[Create(neuron) for neuron in layer2], lag_ratio=0.1),
            run_time=0.5
        )
        self.play(
            LaggedStart(*[Create(neuron) for neuron in layer3], lag_ratio=0.1),
            run_time=0.5
        )
        self.play(Create(output_neuron), run_time=0.5)
        self.wait(0.5)
        
        # ===== LAYER 1: SIMPLE PATTERNS =====
        layer1_title = Text("Layer 1: Simple Patterns", font_size=36, color=LAYER1_COLOR, weight=BOLD)
        layer1_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(layer1_title, shift=DOWN))
        self.wait(0.5)
        
        # Highlight Layer 1
        self.play(
            *[neuron.animate.set_fill(LAYER1_COLOR, opacity=1).scale(1.15) 
              for neuron in layer1],
            conn_input_layer1.animate.set_opacity(0.5),
            run_time=0.8
        )
        self.wait(0.5)
        
        # Show simple pattern insights
        insight1_box = RoundedRectangle(
            width=3.5,
            height=0.8,
            corner_radius=0.2,
            color=LAYER1_COLOR,
            fill_opacity=0.2,
            stroke_width=3
        ).shift(DOWN * 3.5)
        
        insight1_text = Text(
            "\"Bigger houses\nusually cost more\"",
            font_size=20,
            color=WHITE,
            line_spacing=1.3
        ).move_to(insight1_box.get_center())
        
        # Animate insight appearing
        self.play(
            Create(insight1_box),
            Write(insight1_text),
            run_time=1
        )
        self.wait(0.5)
        
        # Create visual effect showing this simple pattern
        size_input = input_layer[0][0]  # Size input circle
        pattern_arrow = CurvedArrow(
            size_input.get_right() + RIGHT * 0.2,
            layer1[0].get_left() + LEFT * 0.1,
            color=INSIGHT_COLOR,
            stroke_width=5
        )
        pattern_label = Text("Size pattern", font_size=18, color=INSIGHT_COLOR)
        pattern_label.next_to(pattern_arrow, UP, buff=0.1)
        
        self.play(
            Create(pattern_arrow),
            Write(pattern_label)
        )
        self.wait(1.5)
        
        # Clean up Layer 1 annotations
        self.play(
            FadeOut(VGroup(insight1_box, insight1_text, 
                          pattern_arrow, pattern_label)),
            *[neuron.animate.set_fill(LAYER1_COLOR, opacity=0.7).scale(1/1.15) 
              for neuron in layer1],
            FadeOut(layer1_title)
        )
        self.wait(0.5)
        
        # ===== LAYER 2: COMBINING IDEAS =====
        layer2_title = Text("Layer 2: Combining Ideas", font_size=36, color=LAYER2_COLOR, weight=BOLD)
        layer2_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(layer2_title, shift=DOWN))
        self.wait(0.5)
        
        # Show data flowing from Layer 1 to Layer 2
        flow_dots1 = VGroup()
        for neuron in layer1:
            dot = Dot(neuron.get_center(), color=INSIGHT_COLOR, radius=0.08)
            flow_dots1.add(dot)
        
        self.play(
            conn_layer1_layer2.animate.set_opacity(0.5),
            *[dot.animate.move_to(layer2[i % len(layer2)].get_center()) 
              for i, dot in enumerate(flow_dots1)],
            run_time=1.2
        )
        
        # Highlight Layer 2
        self.play(
            *[neuron.animate.set_fill(LAYER2_COLOR, opacity=1).scale(1.15) 
              for neuron in layer2],
            FadeOut(flow_dots1),
            run_time=0.6
        )
        self.wait(0.5)
        
        # Show combined pattern insight
        insight2_box = RoundedRectangle(
            width=4.5,
            height=1.2,
            corner_radius=0.2,
            color=LAYER2_COLOR,
            fill_opacity=0.2,
            stroke_width=3
        ).shift(DOWN * 3.2)
        
        insight2_text = Text(
            "\"Large houses near\nthe city are especially\nexpensive\"",
            font_size=18,
            color=WHITE,
            line_spacing=1.2,
            weight=SEMIBOLD
        ).move_to(insight2_box.get_center())
        
        self.play(
            Create(insight2_box),
            Write(insight2_text),
            run_time=0.5
        )
        
        # Visual showing combination
        combo_arrows = VGroup()
        combo_labels = VGroup()
        
        # Arrow from two Layer 1 neurons to one Layer 2 neuron
        arrow1 = CurvedArrow(
            layer1[0].get_right() + RIGHT * 0.1,
            layer2[1].get_left() + LEFT * 0.1,
            color=INSIGHT_COLOR,
            stroke_width=4,
            angle=-TAU/6
        )
        arrow2 = CurvedArrow(
            layer1[3].get_right() + RIGHT * 0.1,
            layer2[1].get_left() + LEFT * 0.1,
            color=INSIGHT_COLOR,
            stroke_width=4,
            angle=TAU/6
        )
        
        combo_label = Text("Combining\npatterns", font_size=18, color=INSIGHT_COLOR, line_spacing=1.2)
        combo_label.next_to(layer2[1], LEFT + UP * 1.8, buff=0.5)
        
        self.play(
            Create(arrow1),
            Create(arrow2),
            Write(combo_label)
        )
        self.wait(0.5)
        
        # Clean up Layer 2 annotations
        self.play(
            FadeOut(VGroup(insight2_box, insight2_text, arrow1, arrow2, 
                          combo_label)),
            *[neuron.animate.set_fill(LAYER2_COLOR, opacity=0.7).scale(1/1.15) 
              for neuron in layer2],
            FadeOut(layer2_title)
        )
        # ===== LAYER 3 & OUTPUT: WEAVING IT ALL TOGETHER =====
        final_title = Text("Final Layers: Weaving Insights Together", 
                          font_size=36, color=LAYER3_COLOR, weight=BOLD)
        final_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(final_title, shift=DOWN))
        self.wait(0.5)
        
        # Show data flowing through Layer 3 to Output
        flow_dots2 = VGroup()
        for neuron in layer2:
            dot = Dot(neuron.get_center(), color=INSIGHT_COLOR, radius=0.08)
            flow_dots2.add(dot)
        
        self.play(
            conn_layer2_layer3.animate.set_opacity(0.5),
            *[dot.animate.move_to(layer3[i % len(layer3)].get_center()) 
              for i, dot in enumerate(flow_dots2)],
            run_time=0.8
        )
        
        self.play(
            *[neuron.animate.set_fill(LAYER3_COLOR, opacity=1).scale(1.1) 
              for neuron in layer3],
            FadeOut(flow_dots2),
            run_time=0.5
        )
        
        # Flow to output
        flow_dots3 = VGroup()
        for neuron in layer3:
            dot = Dot(neuron.get_center(), color=INSIGHT_COLOR, radius=0.08)
            flow_dots3.add(dot)
        
        self.play(
            conn_layer3_output.animate.set_opacity(0.7).set_color(OUTPUT_COLOR),
            *[dot.animate.move_to(output_neuron.get_center()) 
              for dot in flow_dots3],
            run_time=0.8
        )
        
        self.play(
            output_neuron.animate.set_fill(OUTPUT_COLOR, opacity=1).scale(1.3),
            FadeOut(flow_dots3),
            run_time=0.3
        )
        
        # Show final prediction
        prediction_box = RoundedRectangle(
            width=3.5,
            height=1.0,
            corner_radius=0.2,
            color=OUTPUT_COLOR,
            fill_opacity=0.3,
            stroke_width=4
        ).shift(DOWN * 3.2)
        
        prediction_text = Text("Predicted Price:\n$120,000", 
                              font_size=24, 
                              color=WHITE,
                              weight=BOLD,
                              line_spacing=1.2)
        prediction_text.move_to(prediction_box.get_center())
        
        self.play(
            Create(prediction_box),
            Write(prediction_text),
            run_time=0.5
        )
        
        # Add sparkle effect
        self.play(
            Flash(prediction_box, color=YELLOW, flash_radius=1.5, num_lines=12),
            run_time=0.8
        )
        self.wait(1.5)
        
        # Clean up for final message
        self.play(
            FadeOut(VGroup(prediction_box, prediction_text, final_title))
        )
        
        # ===== SHOW THE POWER OF DEEP LEARNING =====
        power_title = Text("The Power of Deep Learning", 
                          font_size=40, 
                          color=YELLOW,
                          weight=BOLD)
        power_title.to_edge(UP, buff=0.5)
        self.play(Write(power_title))
        self.wait(0.5)
        
        # Animate the entire flow one more time to show the complete picture
        self.play(
            all_connections.animate.set_opacity(0.4),
            run_time=0.5
        )
        
        # Create a wave of activation through the network
        wave_dot = Dot(input_layer[0][0].get_center(), color=INSIGHT_COLOR, radius=0.12)
        self.add(wave_dot)
        
        # Animate through each layer
        for i, layer_neurons in enumerate([layer1, layer2, layer3, [output_neuron]]):
            if i < 3:
                target_pos = layer_neurons[len(layer_neurons)//2].get_center()
            else:
                target_pos = layer_neurons[0].get_center()
            
            self.play(
                wave_dot.animate.move_to(target_pos),
                *[neuron.animate.set_stroke(color=YELLOW, width=5) 
                  for neuron in layer_neurons],
                run_time=0.3
            )
            self.play(
                *[neuron.animate.set_stroke(color=neuron.get_color(), width=3) 
                  for neuron in layer_neurons],
                run_time=0.3
            )
        
        self.play(FadeOut(wave_dot))
        
        # Final message boxes        
        message2 = Text(
            "No single equation could capture this!",
            font_size=28,
            color=INSIGHT_COLOR,
            weight=BOLD
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(message2))
        self.wait(0.5)

class RandomWeightsFirstGuess(Scene):
    def construct(self):
        # Color scheme
        RANDOM_COLOR = "#95a5a6"  # Gray for random/untrained
        WEIGHT_COLOR = "#e67e22"  # Orange
        WRONG_COLOR = "#e74c3c"  # Red for wrong prediction
        CORRECT_COLOR = "#2ecc71"  # Green for actual price
        QUESTION_COLOR = "#f39c12"  # Yellow
        

         # ===== INTRODUCTION =====
        interesting = Text("Something interesting", font_size=44, weight=BOLD, color=YELLOW)
        self.play(Write(interesting))
        self.wait(1.2)
        self.play(FadeOut(interesting))
        self.wait(0.5)

        # ===== INTRODUCTION =====
        title = Text("Before Training: Random Weights", font_size=44, weight=BOLD, color=RANDOM_COLOR)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(0.5)      
        self.play(FadeOut(title))

        # ===== CREATE SIMPLE NETWORK =====
        # Input layer
        input_layer = VGroup()
        input_labels = ["Size", "Beds", "Distance"]
        input_positions = [UP * 1.5, ORIGIN, DOWN * 1.5]
        
        for pos, label in zip(input_positions, input_labels):
            circle = Circle(radius=0.5, color="#3498db", fill_opacity=0.7, stroke_width=3)
            circle.shift(LEFT * 4.5 + pos)
            text = Text(label, font_size=16, color=WHITE, line_spacing=1.1).move_to(circle.get_center())
            group = VGroup(circle, text)
            input_layer.add(group)
        
        # Hidden layer
        hidden_layer = VGroup()
        hidden_positions = [UP * 1.8, UP * 0.6, DOWN * 0.6, DOWN * 1.8]
        
        for pos in hidden_positions:
            circle = Circle(radius=0.35, color=RANDOM_COLOR, fill_opacity=0.5, stroke_width=3)
            circle.shift(LEFT * 1.5 + pos)
            hidden_layer.add(circle)
        
        # Output layer
        output_neuron = Circle(radius=0.45, color=RANDOM_COLOR, fill_opacity=0.5, stroke_width=3)
        output_neuron.shift(RIGHT * 2)
        
        # Create connections with random weight labels
        connections = VGroup()
        weight_labels = VGroup()
        
        # Store weight values for animation
        weight_values = []
        
        for i, inp in enumerate(input_layer):
            for j, hidden in enumerate(hidden_layer):
                # Random weight value
                weight = np.random.uniform(-1, 1)
                weight_values.append(weight)
                
                line = Line(
                    inp[0].get_right(),
                    hidden.get_left(),
                    color=RANDOM_COLOR,
                    stroke_width=2,
                    stroke_opacity=0.4
                )
                connections.add(line)
                
                # Add weight label (show only a few for clarity)
                if j == 0 and i < 2:  # Only show weights to first hidden neuron for first two inputs
                    weight_text = DecimalNumber(
                        weight,
                        num_decimal_places=2,
                        font_size=14,
                        color=WEIGHT_COLOR
                    )
                    weight_text.next_to(line.get_center(), UP, buff=0.05)
                    weight_labels.add(weight_text)
        
        # Hidden to output connections
        for hidden in hidden_layer:
            weight = np.random.uniform(-1, 1)
            weight_values.append(weight)
            
            line = Line(
                hidden.get_right(),
                output_neuron.get_left(),
                color=RANDOM_COLOR,
                stroke_width=2,
                stroke_opacity=0.4
            )
            connections.add(line)
        
        # Draw network
        self.play(Create(connections), run_time=0.8)
        self.play(
            LaggedStart(*[Create(group) for group in input_layer], lag_ratio=0.15),
            run_time=0.5
        )
        self.play(
            LaggedStart(*[Create(neuron) for neuron in hidden_layer], lag_ratio=0.1),
            run_time=0.5
        )
        self.play(Create(output_neuron), run_time=0.5)
        
        # Add question marks on neurons to show uncertainty
        question_marks = VGroup()
        for neuron in hidden_layer:
            qmark = Text("?", font_size=24, color=QUESTION_COLOR, weight=BOLD)
            qmark.move_to(neuron.get_center())
            question_marks.add(qmark)
        
        output_qmark = Text("?", font_size=28, color=QUESTION_COLOR, weight=BOLD)
        output_qmark.move_to(output_neuron.get_center())
        
        self.play(
            LaggedStart(*[Write(qm) for qm in question_marks], lag_ratio=0.1),
            Write(output_qmark),
            run_time=0.5
        )       
        # ===== FIRST PREDICTION =====
        self.play(
            FadeOut(question_marks),
            FadeOut(output_qmark)
        )
        
        # Flow from input to hidden
        flow_dots1 = VGroup()
        for inp in input_layer:
            dot = Dot(inp[0].get_center(), color=QUESTION_COLOR, radius=0.08)
            flow_dots1.add(dot)
        
        self.play(
            *[dot.animate.move_to(hidden_layer[i % len(hidden_layer)].get_center()) 
              for i, dot in enumerate(flow_dots1)],
            connections[0:12].animate.set_opacity(0.8).set_color(QUESTION_COLOR),
            run_time=0.8
        )
        
        self.play(
            *[neuron.animate.set_fill(QUESTION_COLOR, opacity=0.6) 
              for neuron in hidden_layer],
            FadeOut(flow_dots1),
            run_time=0.4
        )
        
        # Flow from hidden to output
        flow_dots2 = VGroup()
        for neuron in hidden_layer:
            dot = Dot(neuron.get_center(), color=QUESTION_COLOR, radius=0.08)
            flow_dots2.add(dot)
        
        self.play(
            *[dot.animate.move_to(output_neuron.get_center()) 
              for dot in flow_dots2],
            connections[12:].animate.set_opacity(0.8).set_color(QUESTION_COLOR),
            run_time=0.5
        )
        
        self.play(
            output_neuron.animate.set_fill(QUESTION_COLOR, opacity=0.8).scale(1.2),
            FadeOut(flow_dots2),
            run_time=0.5
        )
        self.wait(0.5)
        
        # ===== SHOW ARBITRARY PREDICTION =====
        
        # First show a wildly wrong prediction
        wrong_prediction_box = RoundedRectangle(
            width=4,
            height=1.3,
            corner_radius=0.2,
            color=WRONG_COLOR,
            fill_opacity=0.2,
            stroke_width=4
        ).shift(RIGHT * 2 + DOWN * 2.8)
        
        wrong_prediction_text = Text("$640,000", font_size=36, color=WRONG_COLOR, weight=BOLD)
        wrong_prediction_text.move_to(wrong_prediction_box.get_center())
        
        arbitrary_label = Text("Completely arbitrary!", font_size=20, color=GRAY, slant=ITALIC)
        arbitrary_label.next_to(wrong_prediction_box, DOWN, buff=0.1)
        
        self.play(
            Create(wrong_prediction_box),
            Write(wrong_prediction_text),
            run_time=0.5
        )
        self.play(Write(arbitrary_label))
        
        # Shake the prediction to show it's wrong
        self.play(
            wrong_prediction_box.animate.shift(LEFT * 0.1),
            wrong_prediction_text.animate.shift(LEFT * 0.1),
            run_time=0.1
        )
        self.play(
            wrong_prediction_box.animate.shift(RIGHT * 0.2),
            wrong_prediction_text.animate.shift(RIGHT * 0.2),
            run_time=0.1
        )
        self.play(
            wrong_prediction_box.animate.shift(LEFT * 0.1),
            wrong_prediction_text.animate.shift(LEFT * 0.1),
            run_time=0.1
        )
        
        # Show "OR" text
        or_text = Text("OR", font_size=28, color=WHITE, weight=BOLD)
        or_text.next_to(wrong_prediction_box, LEFT, buff=1)
        self.play(Write(or_text))
        
        # Show another random prediction
        another_prediction_box = RoundedRectangle(
            width=4,
            height=1.3,
            corner_radius=0.2,
            color=WRONG_COLOR,
            fill_opacity=0.2,
            stroke_width=4
        ).shift(LEFT * 4.5 + DOWN * 2.8)
        
        another_prediction_text = Text("$120,000", font_size=36, color=WRONG_COLOR, weight=BOLD)
        another_prediction_text.move_to(another_prediction_box.get_center())
        
        self.play(
            Create(another_prediction_box),
            Write(another_prediction_text),
            run_time=0.5
        )
        
        # Show it might be close by chance, but still wrong
        lucky_text = Text("Maybe closer by luck?", font_size=18, color=GRAY, slant=ITALIC)
        lucky_text.next_to(another_prediction_box, DOWN, buff=0.1)
        self.play(Write(lucky_text))
        self.wait(0.3)

        first_guess_title = Text("The Network's First Guess", font_size=36, color=QUESTION_COLOR, weight=BOLD)
        first_guess_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(first_guess_title, shift=DOWN))
        self.wait(0.8)
        
        # ===== SHOW ACTUAL PRICE =====
        self.play(
            FadeOut(first_guess_title),
            FadeOut(VGroup(or_text, arbitrary_label, lucky_text))
        )
        
        comparison_title = Text("Comparing to Actual Price", font_size=34, color=CORRECT_COLOR, weight=BOLD)
        comparison_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(comparison_title, shift=DOWN))
        self.wait(0.5)
        
        # Show actual price
        actual_box = RoundedRectangle(
            width=3.5,
            height=1.5,
            corner_radius=0.2,
            color=CORRECT_COLOR,
            fill_opacity=0.3,
            stroke_width=4
        ).next_to(output_neuron, RIGHT, buff=0.5)
        
        actual_label = Text("Actual Price:", font_size=22, color=WHITE)
        actual_price = Text("$250,000", font_size=38, color=CORRECT_COLOR, weight=BOLD)
        actual_group = VGroup(actual_label, actual_price).arrange(DOWN, buff=0.2)
        actual_group.move_to(actual_box.get_center())
        
        self.play(
            Create(actual_box),
            Write(actual_group),
            run_time=1.2
        )
        self.wait(1)
        
        # Show error/distance arrows
        # From $640,000 prediction
        error_arrow1 = DoubleArrow(
            wrong_prediction_box.get_top(),
            actual_box.get_bottom(),
            color=WRONG_COLOR,
            stroke_width=4,
            tip_length=0.2
        )
        error_label1 = Text("Way off!", font_size=20, color=WRONG_COLOR, weight=BOLD)
        error_label1.next_to(error_arrow1, RIGHT, buff=0.2)
        
        self.play(
            GrowArrow(error_arrow1),
            Write(error_label1)
        )
        self.wait(1)
        
        # From $120,000 prediction
        error_arrow2 = DoubleArrow(
            another_prediction_box.get_right(),
            actual_box.get_bottom() + LEFT * 1.5,
            color=WRONG_COLOR,
            stroke_width=4,
            tip_length=0.2
        )
        # error_label2 = Text("Still wrong!", font_size=20, color=WRONG_COLOR, weight=BOLD)
        # error_label2.next_to(error_arrow2, LEFT * 0.1 + UP * 0.5)
        
        self.play(
            GrowArrow(error_arrow2),
            # Write(error_label2)
        )
        self.wait(1.5)

        self.play(
            FadeOut(comparison_title))

        correction = Text("The change can be used to adjust the weights", font_size=34, color=CORRECT_COLOR, weight=BOLD)
        correction.to_edge(UP, buff=0.4)
        self.play(FadeIn(correction, shift=DOWN))
        self.wait(4)
        
        # ===== CRUCIAL STARTING POINT =====
        self.play(
            FadeOut(VGroup(error_arrow1, error_label1, error_arrow2,
                          wrong_prediction_box, wrong_prediction_text,
                          another_prediction_box, another_prediction_text,
                          actual_box, actual_group)),
            FadeOut(correction)
        )
        self.wait(0.5)
        
        # ===== FINAL MESSAGE =====
        
        final_title = Text("Forward Propagation", font_size=40, color="#3498db", weight=BOLD)
        final_title.to_edge(UP, buff=0.5)
        
        final_subtitle = Text("Pushing data forward to get that first prediction", 
                             font_size=28, 
                             color=WHITE)
        final_subtitle.next_to(final_title, DOWN, buff=0.3)
        
        self.play(
            Write(final_title),
            Write(final_subtitle)
        )
        self.wait(1)
        
        # Animate one final forward pass
        self.play(
            output_neuron.animate.set_fill("#3498db", opacity=0.8),
            *[neuron.animate.set_fill("#3498db", opacity=0.5) 
              for neuron in hidden_layer],
            connections.animate.set_color("#3498db").set_opacity(0.5),
            run_time=1.5
        )
        
        # Show prediction appearing
        final_pred_box = RoundedRectangle(
            width=4,
            height=0.8,
            corner_radius=0.2,
            color="#3498db",
            fill_opacity=0.2,
            stroke_width=3
        ).shift(DOWN * 3.0)
        
        final_pred_text = Text("Prediction: Ready!", 
                              font_size=24, 
                              color="#3498db",
                              weight=BOLD)
        final_pred_text.move_to(final_pred_box.get_center())
        
        self.play(
            Create(final_pred_box),
            Write(final_pred_text)
        )
        
        # Checkmark animation
        checkmark = Text("✓", font_size=48, color="#2ecc71", weight=BOLD)
        checkmark.next_to(final_pred_box, RIGHT, buff=0.5)
        self.play(Write(checkmark), Flash(checkmark, color="#2ecc71"))
        
        self.wait(0.5)

class CakeBakingAnalogy(Scene):
    def construct(self):
        # Color scheme
        INGREDIENT_COLOR = "#f39c12"
        PROCESS_COLOR = "#3498db"
        RESULT_COLOR = "#e74c3c"
        LEARN_COLOR = "#9b59b6"
        
         # ===== TITLE =====
        title = Text("A Real-World Analogy", font_size=44, weight=BOLD, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)
        
        subtitle = Text("Learning to Bake a Cake", font_size=32, color=INGREDIENT_COLOR)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait(1.5)
        
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)
        
        # ===== QUICK INGREDIENT MIXING (4s) =====
        # Create SVG ingredients (smaller, arranged horizontally)
        flour = SVGMobject("flour.svg").scale(0.5)
        sugar = SVGMobject("sugar.svg").scale(0.5)
        eggs = SVGMobject("eggs.svg").scale(0.5)
        powder = SVGMobject("baking_powder.svg").scale(0.5)
        
        ingredients = VGroup(flour, sugar, eggs, powder).arrange(RIGHT, buff=0.5)
        ingredients.shift(UP * 1.5)
        
        
        # Show ingredients
        self.play(LaggedStart(*[FadeIn(ing, shift=UP) for ing in ingredients], lag_ratio=0.15), run_time=1)
        
        # Mixing bowl
        mixing_bowl = SVGMobject("mixing_bowl.svg").scale(0.8)
        mixing_bowl.shift(UP * 0.2)
        self.play(FadeIn(mixing_bowl), run_time=0.5)
        
        # Ingredients go into bowl
        self.play(
            *[ing.animate.move_to(mixing_bowl.get_center()).scale(0.3) for ing in ingredients],
            run_time=1
        )
        self.play(FadeOut(ingredients))
        
        # Batter appears
        batter = Ellipse(width=1.2, height=0.4, color="#FFE4B5", fill_opacity=0.9)
        batter.move_to(mixing_bowl.get_center())
        self.play(FadeIn(batter), run_time=0.5)
        
        # ===== BAKE (3s) =====
        # Oven appears, bowl moves in
        oven = SVGMobject("oven.svg").scale(1.2)
        oven.shift(RIGHT * 3)
        self.play(
            FadeIn(oven),
            VGroup(mixing_bowl, batter).animate.scale(0.4).move_to(oven.get_center()),
            run_time=1
        )
        
        # Quick baking indication
        self.wait(0.5)
        
        # Cake appears
        cake_svg = SVGMobject("cake.svg").scale(0.5)
        cake_svg.move_to(mixing_bowl.get_center())
        self.play(FadeOut(batter), FadeIn(cake_svg), run_time=0.5)
        
        # Take out
        self.play(
            VGroup(cake_svg).animate.scale(2).move_to(LEFT * 2.5 + UP * 0.5),
            FadeOut(oven),
            FadeOut(mixing_bowl),
            run_time=1
        )
        
        # ===== TASTE & FEEDBACK (5s) =====
        # Sad face
        face = SVGMobject("sad_face.svg").scale(0.8)
        face.shift(RIGHT * 3)
        self.play(FadeIn(face), run_time=0.5)
        
        feedback = Text("Too sweet!\nNot fluffy!", font_size=20, color=RESULT_COLOR, line_spacing=1.1)
        feedback.next_to(face, DOWN, buff=0.3)
        self.play(Write(feedback), run_time=0.8)
        self.wait(1.5)
        
        # Key insight
        self.play(FadeOut(face), FadeOut(feedback))
        key_insight = Text(
            "You HAD to make that first cake\nto learn what's wrong!",
            font_size=24,
            color=INGREDIENT_COLOR,
            weight=BOLD,
            line_spacing=1.2
        )
        key_insight.shift(RIGHT * 2.5)
        
        insight_box = SurroundingRectangle(key_insight, color=INGREDIENT_COLOR, stroke_width=3, buff=0.25)
        self.play(Write(key_insight), run_time=1)
        self.play(Create(insight_box), run_time=0.5)
        self.wait(1)
        
        # ===== PARALLEL COMPARISON (10s) =====
        self.play(FadeOut(VGroup(cake_svg, key_insight, insight_box)))
        
        comparison_title = Text("Forward Propagation Works the Same Way", 
                               font_size=32, 
                               color=PROCESS_COLOR,
                               weight=BOLD)
        comparison_title.to_edge(UP, buff=0.3)
        self.play(Write(comparison_title), run_time=0.8)
        
        # Side by side
        cake_side = VGroup(
            Text("Baking", font_size=24, color=INGREDIENT_COLOR, weight=BOLD),
            Text("1. Mix ingredients", font_size=18, color=WHITE),
            Text("2. Bake", font_size=18, color=WHITE),
            Text("3. Taste (first attempt)", font_size=18, color=WHITE),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        cake_side.shift(LEFT * 3)
        
        nn_side = VGroup(
            Text("Neural Network", font_size=24, color=PROCESS_COLOR, weight=BOLD),
            Text("1. Input data", font_size=18, color=WHITE),
            Text("2. Process layers", font_size=18, color=WHITE),
            Text("3. Predict (first attempt)", font_size=18, color=WHITE),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        nn_side.shift(RIGHT * 3)
        
        divider = DashedLine(UP * 2, DOWN * 2.5, color=GRAY, stroke_width=2)
        
        self.play(
            Write(cake_side[0]),
            Write(nn_side[0]),
            Create(divider),
            run_time=0.8
        )
        
        # Show steps together
        for i in range(1, 4):
            self.play(Write(cake_side[i]), Write(nn_side[i]), run_time=0.6)
            self.wait(0.3)
        
        # Highlight first attempts
        highlight_left = SurroundingRectangle(cake_side[3], color=INGREDIENT_COLOR, stroke_width=2, buff=0.05)
        highlight_right = SurroundingRectangle(nn_side[3], color=PROCESS_COLOR, stroke_width=2, buff=0.05)
        
        self.play(Create(highlight_left), Create(highlight_right), run_time=0.5)
        
        same_text = Text("Same concept!", font_size=22, color=INGREDIENT_COLOR, weight=BOLD)
        same_text.shift(DOWN * 2.8)
        self.play(Write(same_text), run_time=0.6)
        self.wait(1.5)
        
        # ===== FINAL MESSAGE (3s) =====
        self.play(FadeOut(VGroup(comparison_title, cake_side, nn_side, divider, 
                                 highlight_left, highlight_right, same_text)))
        
        final_message = Text(
            "The network's first taste\nbefore fine-tuning",
            font_size=28,
            color=WHITE,
            line_spacing=1.3,
            weight=SEMIBOLD
        )
        
        self.play(Write(final_message), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(final_message), run_time=0.5)

class ForwardPropIntroPreview(Scene):
    def construct(self):
        # Color scheme
        INPUT_COLOR = "#3498db"  # Blue
        HIDDEN_COLOR = "#9b59b6"  # Purple
        OUTPUT_COLOR = "#e74c3c"  # Red
        HIGHLIGHT_COLOR = "#f39c12"  # Orange/Yellow
        
        # ===== "TODAY" - Main concept introduction =====
        
        # Main title appears
        main_title = Text("Forward Propagation", font_size=52, weight=BOLD, color=INPUT_COLOR)
        main_title.to_edge(UP, buff=0.8)
        
        subtitle = Text("Data flowing through the network", font_size=28, color=WHITE)
        subtitle.next_to(main_title, DOWN, buff=0.3)
        
        self.play(
            Write(main_title),
            run_time=1.2
        )
        self.play(FadeIn(subtitle, shift=UP), run_time=0.8)
        self.wait(1)
        
        # ===== Quick network preview =====
        # Create simple network structure
        # Input layer (3 neurons)
        input_layer = VGroup()
        for i in range(3):
            circle = Circle(radius=0.25, color=INPUT_COLOR, fill_opacity=0.7, stroke_width=2)
            circle.shift(LEFT * 4 + UP * (1 - i))
            input_layer.add(circle)
        
        # Hidden layer (4 neurons)
        hidden_layer = VGroup()
        for i in range(4):
            circle = Circle(radius=0.25, color=HIDDEN_COLOR, fill_opacity=0.6, stroke_width=2)
            circle.shift(LEFT * 1.5 + UP * (1.5 - i))
            hidden_layer.add(circle)
        
        # Output layer (1 neuron)
        output_neuron = Circle(radius=0.3, color=OUTPUT_COLOR, fill_opacity=0.8, stroke_width=3)
        output_neuron.shift(RIGHT * 2)
        
        # Connections
        connections = VGroup()
        for inp in input_layer:
            for hidden in hidden_layer:
                line = Line(inp.get_right(), hidden.get_left(), 
                           color=WHITE, stroke_width=1, stroke_opacity=0.2)
                connections.add(line)
        
        for hidden in hidden_layer:
            line = Line(hidden.get_right(), output_neuron.get_left(),
                       color=WHITE, stroke_width=1, stroke_opacity=0.2)
            connections.add(line)
        
        network = VGroup(connections, input_layer, hidden_layer, output_neuron)
        network.shift(DOWN * 0.5)
        
        # Draw network quickly
        self.play(
            FadeOut(subtitle),
            main_title.animate.scale(0.8).to_edge(UP, buff=0.3),
            run_time=0.5
        )
        
        self.play(
            Create(connections),
            LaggedStart(
                *[Create(neuron) for neuron in input_layer],
                *[Create(neuron) for neuron in hidden_layer],
                Create(output_neuron),
                lag_ratio=0.05
            ),
            run_time=1.5
        )
        self.wait(0.5)
        
        # ===== Show the flow animation =====
        # Quick flow visualization
        flow_arrow = Arrow(
            input_layer.get_right() + RIGHT * 0.3 + UP * 2,
            output_neuron.get_left() + LEFT * 0.3 + UP * 2,
            color=HIGHLIGHT_COLOR,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.12
        )
        
        flow_label = Text("Data flows →", font_size=24, color=HIGHLIGHT_COLOR)
        flow_label.next_to(flow_arrow, UP, buff=0.2)
        
        self.play(
            GrowArrow(flow_arrow),
            Write(flow_label),
            run_time=1
        )
        self.wait(0.8)
        
        # Pulse animation showing activation
        self.play(
            *[neuron.animate.set_fill(opacity=1).scale(1.2) for neuron in input_layer],
            run_time=0.3
        )
        self.play(
            *[neuron.animate.set_fill(opacity=0.7).scale(1/1.2) for neuron in input_layer],
            *[neuron.animate.set_fill(opacity=1).scale(1.15) for neuron in hidden_layer],
            run_time=0.4
        )
        self.play(
            *[neuron.animate.set_fill(opacity=0.6).scale(1/1.15) for neuron in hidden_layer],
            output_neuron.animate.set_fill(opacity=1).scale(1.2),
            run_time=0.4
        )
        self.wait(0.5)
        
        self.play(
            FadeOut(flow_arrow),
            FadeOut(flow_label)
        )

        self.wait(7)
        
        # ===== House price example =====
        # Fade network to background
        self.play(
            network.animate.scale(0.7).shift(LEFT * 1.5),
            main_title.animate.scale(0.8),
            run_time=0.8
        )
        
        # Show example box
        example_title = Text("Example: House Price Prediction", 
                           font_size=28, 
                           color=HIGHLIGHT_COLOR,
                           weight=BOLD)
        example_title.shift(RIGHT * 2.5 + UP * 1.5)
        
        # Input features
        feature_box = RoundedRectangle(
            width=3.5,
            height=2.2,
            corner_radius=0.15,
            color=INPUT_COLOR,
            fill_opacity=0.1,
            stroke_width=2
        ).shift(RIGHT * 2.5)
        
        features = VGroup(
            Text("📐 Size", font_size=24),
            Text("🛏️ Bedrooms", font_size=24),
            Text("📍 Location", font_size=24)
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        features.move_to(feature_box.get_center())
        
        # Output prediction
        output_box = RoundedRectangle(
            width=3.5,
            height=0.9,
            corner_radius=0.15,
            color=OUTPUT_COLOR,
            fill_opacity=0.15,
            stroke_width=3
        ).shift(RIGHT * 2.5 + DOWN * 1.8)
        
        output_text = Text("💰 Predicted Price", 
                          font_size=20, 
                          color=OUTPUT_COLOR,
                          weight=BOLD)
        output_text.move_to(output_box.get_center())
        
        self.play(Write(example_title), run_time=0.8)
        self.wait(0.3)
        
        self.play(
            Create(feature_box),
            LaggedStart(*[Write(f) for f in features], lag_ratio=0.2),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Arrow from inputs to output
        prediction_arrow = Arrow(
            feature_box.get_bottom(),
            output_box.get_top(),
            color=HIGHLIGHT_COLOR,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(GrowArrow(prediction_arrow), run_time=0.6)
        
        self.play(
            Create(output_box),
            Write(output_text),
            run_time=1
        )
        self.wait(1.8)
        
        # ===== Final call to action =====
        dive_in = Text("Let's dive in!", font_size=36, color=HIGHLIGHT_COLOR, weight=BOLD)
        dive_in.to_edge(DOWN, buff=0.8)
        
        self.play(
            Write(dive_in),
            Flash(dive_in, color=HIGHLIGHT_COLOR, flash_radius=1.5, num_lines=8),
            run_time=1
        )
        self.wait(0.5)
        
        # Fade everything out
        self.play(
            FadeOut(VGroup(
                main_title, network, example_title, feature_box, features,
                prediction_arrow, output_box, output_text, dive_in
            )),
            run_time=1
        )
        self.wait(0.5)

class KeyTakeaways(Scene):
    def construct(self):
        # Color scheme
        TITLE_COLOR = "#f39c12"  # Orange
        POINT_COLOR = "#3498db"  # Blue
        HIGHLIGHT_COLOR = "#e74c3c"  # Red
        
        # ===== TITLE (2s) =====
        title = Text("Key Takeaways", font_size=48, weight=BOLD, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # ===== KEY POINTS (18s) =====
        # Create all points
        point1 = VGroup(
            Text("1.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            Text("Forward propagation = First pass", font_size=28, color=WHITE)
        ).arrange(RIGHT, buff=0.3)
        
        point2 = VGroup(
            Text("2.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            Text("Input → Hidden → Output", font_size=28, color=WHITE)
        ).arrange(RIGHT, buff=0.3)
        
        point3 = VGroup(
            Text("3.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            Text("Each neuron: compute → activate → pass", font_size=28, color=WHITE)
        ).arrange(RIGHT, buff=0.3)
        
        point4 = VGroup(
            Text("4.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            Text("Produces the 'first guess'", font_size=28, color=WHITE)
        ).arrange(RIGHT, buff=0.3)
        
        point5 = VGroup(
            Text("5.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            Text("Starting point for backpropagation", font_size=28, color=POINT_COLOR, slant=ITALIC)
        ).arrange(RIGHT, buff=0.3)
        
        # Arrange all points
        points = VGroup(point1, point2, point3, point4, point5)
        points.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        points.shift(DOWN * 0.3)
        
        # Animate each point appearing (3-4s per point)
        self.play(FadeIn(point1, shift=RIGHT), run_time=0.8)
        self.wait(3)
        
        self.play(FadeIn(point2, shift=RIGHT), run_time=0.8)
        self.wait(1)
        
        self.play(FadeIn(point3, shift=RIGHT), run_time=0.8)
        self.wait(7)
        
        self.play(FadeIn(point4, shift=RIGHT), run_time=0.8)
        self.wait(1)
        
        # Highlight "first guess"
        first_guess = point4[1]
        highlight_box = SurroundingRectangle(
            first_guess, 
            color=HIGHLIGHT_COLOR, 
            stroke_width=3, 
            buff=0.1
        )
        self.play(Create(highlight_box), run_time=0.5)
        self.wait(0.5)
        self.play(FadeOut(highlight_box), run_time=0.3)
        
        self.play(FadeIn(point5, shift=RIGHT), run_time=0.8)
        self.wait(1)
        
        # ===== COMING NEXT (2s) =====
        coming_next = Text("Coming next: Backpropagation!", 
                          font_size=26, 
                          color=POINT_COLOR,
                          weight=BOLD)
        coming_next.next_to(points, DOWN, buff=0.6)
        
        arrow = Arrow(point5.get_bottom(), coming_next.get_top(), 
                     color=POINT_COLOR, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        
        self.play(GrowArrow(arrow), run_time=0.4)
        self.play(Write(coming_next), run_time=0.6)
        self.wait(2)