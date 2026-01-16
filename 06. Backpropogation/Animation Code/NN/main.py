from manim import *
import numpy as np

class BackpropIntro(Scene):
    def construct(self):
        # Color scheme
        INPUT_COLOR = BLUE
        HIDDEN_COLOR = GREEN
        OUTPUT_COLOR = RED
        ERROR_COLOR = ORANGE
        FORWARD_COLOR = BLUE_C
        BACKWARD_COLOR = RED_C
        
        # Title
        title = Text("Backpropagation: Propagating Error Backward", font_size=36, gradient=(RED, ORANGE))
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Create a simple neural network
        # Input layer (3 neurons - house features)
        input_neurons = VGroup(*[Circle(radius=0.3, color=INPUT_COLOR, fill_opacity=0.3) for _ in range(3)])
        input_neurons.arrange(DOWN, buff=0.5)
        input_neurons.shift(LEFT * 4)
        
        # Input labels
        input_labels = VGroup(
            Text("Size", font_size=20),
            Text("Location", font_size=20),
            Text("Rooms", font_size=20)
        )
        for i, label in enumerate(input_labels):
            label.next_to(input_neurons[i], LEFT, buff=0.3)
        
        # Hidden layer (4 neurons)
        hidden_neurons = VGroup(*[Circle(radius=0.3, color=HIDDEN_COLOR, fill_opacity=0.3) for _ in range(4)])
        hidden_neurons.arrange(DOWN, buff=0.4)
        hidden_neurons.shift(LEFT * 1)
        
        # Output layer (1 neuron - price prediction)
        output_neuron = Circle(radius=0.4, color=OUTPUT_COLOR, fill_opacity=0.3)
        output_neuron.shift(RIGHT * 3)
        
        output_label = Text("Price", font_size=20)
        output_label.next_to(output_neuron, RIGHT, buff=0.3)
        
        # Create connections
        input_to_hidden = VGroup()
        for inp in input_neurons:
            for hid in hidden_neurons:
                line = Line(inp.get_right(), hid.get_left(), stroke_width=1.5, color=GRAY)
                input_to_hidden.add(line)
        
        hidden_to_output = VGroup()
        for hid in hidden_neurons:
            line = Line(hid.get_right(), output_neuron.get_left(), stroke_width=1.5, color=GRAY)
            hidden_to_output.add(line)
        
        # Draw the network
        self.play(
            Create(input_to_hidden),
            Create(hidden_to_output),
            Create(input_neurons),
            Create(hidden_neurons),
            Create(output_neuron),
            Write(input_labels),
            Write(output_label)
        )
        self.wait()
        
        # Forward propagation demonstration
        forward_text = Text("Forward Propagation", font_size=28, color=FORWARD_COLOR)
        forward_text.next_to(title, DOWN, buff=0.3)
        self.play(Write(forward_text))
        self.wait()
        
        # Animate data flowing forward
        for i, inp in enumerate(input_neurons):
            self.play(inp.animate.set_fill(INPUT_COLOR, opacity=0.8), run_time=0.3)
        
        # Flow to hidden layer
        self.play(
            *[line.animate.set_color(FORWARD_COLOR) for line in input_to_hidden],
            run_time=0.8
        )
        self.play(*[hid.animate.set_fill(HIDDEN_COLOR, opacity=0.8) for hid in hidden_neurons])
        self.wait()
        
        # Flow to output
        self.play(
            *[line.animate.set_color(FORWARD_COLOR) for line in hidden_to_output],
            run_time=0.8
        )
        self.play(output_neuron.animate.set_fill(OUTPUT_COLOR, opacity=0.8))
        self.wait(5)
        
        # Show prediction
        prediction = Text("$280,000", font_size=32, color=OUTPUT_COLOR, weight=BOLD)
        prediction.next_to(output_neuron, DOWN, buff=0.5)
        self.play(Write(prediction))
        self.wait()
        
        # Show actual value
        actual = Text("Actual: $300,000", font_size=28, color=GREEN)
        actual.next_to(prediction, DOWN, buff=0.3)
        self.play(Write(actual))
        self.wait()
        
        # Calculate error
        error_calc = MathTex(r"\text{Error} = \$20{,}000", font_size=32, color=ERROR_COLOR)
        error_calc.next_to(actual, DOWN, buff=0.3)
        self.play(Write(error_calc))
        self.wait()
        
        # Fade out forward propagation, reset colors
        self.play(
            FadeOut(forward_text),
            FadeOut(prediction),
            FadeOut(actual),
            FadeOut(title),
            *[line.animate.set_color(GRAY) for line in input_to_hidden],
            *[line.animate.set_color(GRAY) for line in hidden_to_output],
            *[inp.animate.set_fill(INPUT_COLOR, opacity=0.3) for inp in input_neurons],
            *[hid.animate.set_fill(HIDDEN_COLOR, opacity=0.3) for hid in hidden_neurons],
            output_neuron.animate.set_fill(OUTPUT_COLOR, opacity=0.3)
        )
        self.wait()
        
        # Backpropagation begins
        backprop_text = Text("Backpropagation", font_size=28, color=BACKWARD_COLOR, weight=BOLD)
        backprop_text.next_to(title, DOWN, buff=0.3)
        self.play(Write(backprop_text))
        self.wait()
        
        # Question appears
        question = Text("Where did this $20,000 error come from?", font_size=26, color=ERROR_COLOR, slant=ITALIC)
        question.move_to(error_calc.get_center())
        self.play(Transform(error_calc, question))
        self.wait(3)
        
        # Output neuron highlights - it goes first
        output_glow = Circle(radius=0.5, color=ERROR_COLOR).move_to(output_neuron.get_center())
        output_glow.set_stroke(width=4)
        self.play(
            Create(output_glow),
            output_neuron.animate.set_fill(ERROR_COLOR, opacity=0.9),
            Flash(output_neuron, color=ERROR_COLOR, flash_radius=0.7)
        )
        self.wait()
        
        # Output neuron's thought
        output_thought = Text("I'm responsible!", font_size=20, color=ERROR_COLOR)
        output_thought.next_to(output_neuron, UP, buff=0.3)
        self.play(Write(output_thought))
        self.wait()
        
        # Error flows backward to hidden layer
        self.play(FadeOut(output_thought))
        
        # Create error signals (arrows) flowing backward
        error_arrows_to_hidden = VGroup()
        for hid in hidden_neurons:
            arrow = Arrow(
                output_neuron.get_left(),
                hid.get_right(),
                color=BACKWARD_COLOR,
                stroke_width=3,
                buff=0.3,
                max_tip_length_to_length_ratio=0.15
            )
            error_arrows_to_hidden.add(arrow)
        
        self.play(
            *[GrowArrow(arrow) for arrow in error_arrows_to_hidden],
            *[line.animate.set_color(BACKWARD_COLOR) for line in hidden_to_output],
            run_time=1.2
        )
        self.wait(5)

        self.play(FadeOut(error_calc))
        
        # Hidden neurons ask the question
        hidden_question = Text("How much did MY output contribute?", font_size=22, color=BACKWARD_COLOR)
        hidden_question.next_to(hidden_neurons, DOWN, buff=0.5)
        self.play(Write(hidden_question))
        self.wait()
        
        # Highlight hidden neurons with varying intensities (showing different contributions)
        contributions = [0.9, 0.5, 0.7, 0.4]  # Different responsibility levels
        for i, (hid, contrib) in enumerate(zip(hidden_neurons, contributions)):
            self.play(
                hid.animate.set_fill(ERROR_COLOR, opacity=contrib),
                run_time=0.4
            )
        self.wait()
        
        # Labels showing strong vs minor impact
        strong_label = Text("Strong impact", font_size=18, color=RED)
        strong_label.next_to(hidden_neurons[0], LEFT, buff=0.3)
        minor_label = Text("Minor effect", font_size=18, color=YELLOW)
        minor_label.next_to(hidden_neurons[3], LEFT, buff=0.3)
        
        self.play(Write(strong_label), Write(minor_label))
        self.wait()
        
        self.play(FadeOut(hidden_question), FadeOut(strong_label), FadeOut(minor_label))
        
        # Error flows backward to input layer
        error_arrows_to_input = VGroup()
        for inp in input_neurons:
            for hid in hidden_neurons:
                arrow = Arrow(
                    hid.get_left(),
                    inp.get_right(),
                    color=BACKWARD_COLOR,
                    stroke_width=2,
                    buff=0.3,
                    max_tip_length_to_length_ratio=0.1
                )
                error_arrows_to_input.add(arrow)
        
        self.play(
            *[GrowArrow(arrow) for arrow in error_arrows_to_input],
            *[line.animate.set_color(BACKWARD_COLOR) for line in input_to_hidden],
            run_time=1.2
        )
        
        # Input neurons light up
        input_contributions = [0.6, 0.8, 0.5]
        for inp, contrib in zip(input_neurons, input_contributions):
            self.play(inp.animate.set_fill(ERROR_COLOR, opacity=contrib), run_time=0.3)
        self.wait(8)
        
        # Final message
        final_message = Text(
            "Every neuron and weight knows\nits responsibility for the error",
            font_size=26,
            color=YELLOW,
            line_spacing=1.2
        )
        final_message.to_edge(DOWN, buff=0.5)
        
        # Create a glowing box around the message
        message_box = SurroundingRectangle(final_message, color=YELLOW, buff=0.3)
        message_box.set_stroke(width=3)
        
        self.play(Write(final_message), Create(message_box))
        self.wait()
        
        # Pulse all neurons to show they're "aware"
        self.play(
            *[neuron.animate.scale(1.2).set_stroke(width=3) for neuron in input_neurons],
            *[neuron.animate.scale(1.2).set_stroke(width=3) for neuron in hidden_neurons],
            output_neuron.animate.scale(1.2).set_stroke(width=3),
            run_time=0.5
        )
        self.play(
            *[neuron.animate.scale(1/1.2) for neuron in input_neurons],
            *[neuron.animate.scale(1/1.2) for neuron in hidden_neurons],
            output_neuron.animate.scale(1/1.2),
            run_time=0.5
        )
        self.wait()
        
        # Summary: Backpropagation assigns credit and responsibility
        summary = Text(
            "Backpropagation: Assigning Credit & Responsibility",
            font_size=32,
            color=YELLOW,
            weight=BOLD
        )
        summary.move_to(ORIGIN)
        
        # Fade out everything except the network structure, then show summary
        self.play(
            FadeOut(backprop_text),
            FadeOut(final_message),
            FadeOut(message_box),
            FadeOut(error_arrows_to_hidden),
            FadeOut(error_arrows_to_input),
            FadeOut(output_glow),
            FadeOut(input_to_hidden),
            FadeOut(hidden_to_output),
            FadeOut(input_neurons),
            FadeOut(hidden_neurons),
            FadeOut(output_neuron),
            FadeOut(input_labels),
            FadeOut(output_label),
        )
        
        self.wait()
        
        self.play(Write(summary))
        self.wait()
        
        # Final wait
        self.wait(2)

class GradientDescentWeights(Scene):
    def construct(self):
        # Color scheme
        WEIGHT_COLOR = BLUE
        GRADIENT_COLOR = ORANGE
        LOSS_COLOR = RED
        IMPROVE_COLOR = GREEN
        WORSE_COLOR = RED
        
        # Title
        title = Text("Taking Action: Updating Weights", font_size=36, color=BLUE)
        self.play(Write(title))
        self.wait(7)
        
        # Recap the scenario
        scenario = VGroup(
            Text("Predicted: $280,000", font_size=28, color=RED),
            Text("Actual: $300,000", font_size=28, color=GREEN),
            Text("Error: $20,000", font_size=28, color=ORANGE, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        
        self.play(Write(scenario), FadeOut(title))
        self.wait(6)
        
        self.play(scenario.animate.scale(0.7).to_corner(UL, buff=0.5))
        self.wait()
        
        # Show a simple connection with a weight
        neuron_left = Circle(radius=0.4, color=BLUE, fill_opacity=0.5)
        neuron_left.shift(LEFT * 3)
        neuron_right = Circle(radius=0.4, color=GREEN, fill_opacity=0.5)
        neuron_right.shift(RIGHT * 3)
        
        connection = Line(neuron_left.get_right(), neuron_right.get_left(), stroke_width=4, color=GRAY)
        
        # Weight value
        weight_value = DecimalNumber(0.5, num_decimal_places=2, color=WEIGHT_COLOR, font_size=32)
        weight_value.next_to(connection, UP, buff=0.3)
        weight_label = Text("Weight", font_size=20, color=WEIGHT_COLOR)
        weight_label.next_to(weight_value, UP, buff=0.2)
        
        self.play(
            Create(neuron_left),
            Create(neuron_right),
            Create(connection),
            Write(weight_value),
            Write(weight_label)
        )
        self.wait()
        
        # Weight receives a signal during backpropagation
        signal_text = Text("Signal from backpropagation", font_size=24, color=GRADIENT_COLOR)
        signal_text.next_to(connection, DOWN, buff=0.5)
        
        # Gradient arrow pointing at weight
        gradient_arrow = Arrow(
            signal_text.get_top(),
            connection.get_center(),
            color=GRADIENT_COLOR,
            stroke_width=4,
            buff=0.1
        )
        
        self.play(Write(signal_text), GrowArrow(gradient_arrow))
        self.play(Flash(weight_value, color=GRADIENT_COLOR, flash_radius=0.5))
        self.wait(2.5)
        
        # The weight asks a question
        question = Text(
            "If I were larger, would prediction\nmove closer to $300,000?",
            font_size=22,
            color=YELLOW,
            line_spacing=1.2,
            slant=ITALIC
        )
        question_box = SurroundingRectangle(question, color=YELLOW, buff=0.2)
        question_group = VGroup(question, question_box)
        question_group.next_to(signal_text, DOWN, buff=0.7)
        
        self.play(Write(question), Create(question_box))
        self.wait(10)
        
        self.play(FadeOut(question_group), FadeOut(signal_text), FadeOut(gradient_arrow))   
        # Introduce gradient descent
        self.play(
            FadeOut(scenario),
            FadeOut(neuron_left),
            FadeOut(neuron_right),
            FadeOut(connection),
            FadeOut(weight_value),
            FadeOut(weight_label)
        )
        
        gradient_title = Text("Gradient Descent", font_size=32, color=GRADIENT_COLOR, weight=BOLD)
        gradient_title.move_to(UP * 0.5)
        self.play(Write(gradient_title))
        self.wait()
        
        # Mathematical concept visualization
        calc_text = Text("Guided by Multivariable Calculus", font_size=24, color=WHITE, slant=ITALIC)
        calc_text.next_to(gradient_title, DOWN, buff=0.4)
        self.play(Write(calc_text))
        self.wait(4)
        
        # Show what gradient descent tells us
        gd_explanation = VGroup(
            Text("Gradient Descent tells us:", font_size=24, weight=BOLD),
            Text("• Which direction increases error", font_size=20, color=RED),
            Text("• Which direction decreases error", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        gd_explanation.next_to(calc_text, DOWN, buff=0.5)
        
        self.play(Write(gd_explanation))
        self.wait(2)
        self.play(
            FadeOut(gradient_title),
            FadeOut(calc_text),
            FadeOut(gd_explanation)
        )
        
        # Create loss landscape visualization
        landscape_title = Text("Loss Landscape", font_size=28, color=LOSS_COLOR)
        landscape_title.to_edge(UP, buff=1.5)
        
        # Create axes for loss vs weight
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[0, 4, 1],
            x_length=8,
            y_length=4,
            axis_config={"color": GRAY},
            tips=False
        )
        axes.shift(DOWN * 0.5)
        
        # Labels
        x_label = Text("Weight Value", font_size=20).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Loss", font_size=20).next_to(axes.y_axis, LEFT + UP * 0.3, buff=0.3).rotate(PI/2)
        
        # Loss curve (parabola)
        loss_curve = axes.plot(
            lambda x: (x - 0.3) ** 2 + 0.5,
            color=LOSS_COLOR,
            stroke_width=4
        )
        
        self.play(Write(landscape_title))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(loss_curve))
        
        # Current weight position (too small)
        current_x = -0.5
        current_point = Dot(axes.c2p(current_x, (current_x - 0.3) ** 2 + 0.5), color=YELLOW, radius=0.1)
        current_label = Text("Current Weight", font_size=18, color=YELLOW)
        current_label.next_to(current_point, UP, buff=0.2)
        
        self.play(FadeIn(current_point), Write(current_label))
        
        # Show gradient arrow (pointing right - direction to decrease loss)
        gradient_x = current_x + 0.3
        gradient_arrow_on_curve = Arrow(
            current_point.get_center(),
            axes.c2p(gradient_x, (current_x - 0.3) ** 2 + 0.5),
            color=GRADIENT_COLOR,
            buff=0,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.2
        )
        
        gradient_label = Text("Gradient Direction", font_size=18, color=GRADIENT_COLOR)
        gradient_label.next_to(gradient_arrow_on_curve, DOWN + LEFT * 0.3, buff=0.2)
        
        self.play(GrowArrow(gradient_arrow_on_curve), Write(gradient_label))
        self.wait()
        
        # Animate weight update (small step)
        new_x = current_x + 0.2
        new_point = Dot(axes.c2p(new_x, (new_x - 0.3) ** 2 + 0.5), color=IMPROVE_COLOR, radius=0.1)
        update_arrow = Arrow(
            current_point.get_center(),
            new_point.get_center(),
            color=IMPROVE_COLOR,
            buff=0.1,
            stroke_width=4
        )
        
        self.play(
            GrowArrow(update_arrow)
        )

        self.play(FadeOut(gradient_arrow_on_curve), FadeOut(gradient_label), FadeOut(current_label))
        self.play(Transform(current_point, new_point))
        
        # Clean up for decision visualization
        self.play(
            FadeOut(landscape_title),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(loss_curve),
            FadeOut(current_point),
            FadeOut(update_arrow),
        )
        
        # Weight adjustment decision tree
        decision_title = Text("Weight Update Decision", font_size=32, color=YELLOW, weight=BOLD)
        decision_title.to_edge(UP, buff=1)
        self.play(Write(decision_title))
        
        # Central weight
        weight_box = Rectangle(height=1, width=2, color=WEIGHT_COLOR, fill_opacity=0.3)
        weight_text = Text("Weight", font_size=24, color=WEIGHT_COLOR)
        weight_text.move_to(weight_box.get_center())
        weight_group = VGroup(weight_box, weight_text)
        weight_group.move_to(ORIGIN + UP * 1.5)
        
        self.play(Create(weight_box), Write(weight_text))
        
        # Two branches
        left_arrow = Arrow(weight_group.get_bottom(), LEFT * 2 + DOWN * 1.2, color=GREEN, stroke_width=4)
        right_arrow = Arrow(weight_group.get_bottom(), RIGHT * 2 + DOWN * 1.2, color=RED, stroke_width=4)
        
        # Left side: increase helps
        increase_helps_box = Rectangle(height=1.2, width=3, color=GREEN, fill_opacity=0.2)
        increase_helps_box.move_to(LEFT * 2 + DOWN * 1.8)
        increase_helps_text = VGroup(
            Text("Increasing reduces error", font_size=18, color=GREEN),
            Text("→ Increase weight", font_size=18, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        increase_helps_text.move_to(increase_helps_box.get_center())
        
        # Right side: increase hurts
        increase_hurts_box = Rectangle(height=1.2, width=3, color=RED, fill_opacity=0.2)
        increase_hurts_box.move_to(RIGHT * 2 + DOWN * 1.8)
        increase_hurts_text = VGroup(
            Text("Increasing adds error", font_size=18, color=RED),
            Text("→ Decrease weight", font_size=18, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        increase_hurts_text.move_to(increase_hurts_box.get_center())
        
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow))
        self.play(
            Create(increase_helps_box),
            Write(increase_helps_text),
            Create(increase_hurts_box),
            Write(increase_hurts_text)
        )
        self.wait(5)
        
        # Emphasize small adjustments
        careful_note = Text(
            "Adjustments are intentionally  small",
            font_size=22,
            color=YELLOW,
            slant=ITALIC
        )
        careful_note.to_edge(DOWN, buff=0.8)
        careful_box = SurroundingRectangle(careful_note, color=YELLOW, buff=0.2)
        
        self.play(Write(careful_note), Create(careful_box))
        self.wait()
        
        # Clean up for next section
        self.play(
            FadeOut(decision_title),
            FadeOut(weight_group),
            FadeOut(left_arrow),
            FadeOut(right_arrow),
            FadeOut(increase_helps_box),
            FadeOut(increase_helps_text),
            FadeOut(increase_hurts_box),
            FadeOut(increase_hurts_text),
            FadeOut(careful_note),
            FadeOut(careful_box)
        )
        self.wait(3)
        
        # Show iterative improvement
        iteration_title = Text("Iterative Improvement", font_size=32, color=BLUE, weight=BOLD)
        iteration_title.to_edge(UP, buff=1)
        self.play(Write(iteration_title))
        self.wait()
        
        # Create a cycle diagram
        cycle_radius = 2
        cycle_center = ORIGIN + DOWN * 0.5
        
        # Three stages
        predict_circle = Circle(radius=0.6, color=BLUE, fill_opacity=0.3)
        predict_circle.move_to(cycle_center + UP * cycle_radius)
        predict_text = Text("Predict", font_size=20, color=BLUE)
        predict_text.move_to(predict_circle.get_center())
        
        error_circle = Circle(radius=0.6, color=ORANGE, fill_opacity=0.3)
        error_circle.move_to(cycle_center + DOWN * cycle_radius * 0.5 + LEFT * cycle_radius * 0.866)
        error_text = Text("Measure\nError", font_size=18, color=ORANGE, line_spacing=0.8)
        error_text.move_to(error_circle.get_center())
        
        adjust_circle = Circle(radius=0.6, color=GREEN, fill_opacity=0.3)
        adjust_circle.move_to(cycle_center + DOWN * cycle_radius * 0.5 + RIGHT * cycle_radius * 0.866)
        adjust_text = Text("Adjust\nWeights", font_size=18, color=GREEN, line_spacing=0.8)
        adjust_text.move_to(adjust_circle.get_center())
        
        # Arrows connecting them
        arrow1 = CurvedArrow(
            predict_circle.get_left() + DOWN * 0.3,
            error_circle.get_top() + RIGHT * 0.3,
            color=WHITE,
            stroke_width=3
        )
        arrow2 = CurvedArrow(
            error_circle.get_right() + UP * 0.3,
            adjust_circle.get_left() + UP * 0.3,
            color=WHITE,
            stroke_width=3
        )
        arrow3 = CurvedArrow(
            adjust_circle.get_top() + LEFT * 0.3,
            predict_circle.get_right() + DOWN * 0.3,
            color=WHITE,
            stroke_width=3
        )
        
        self.play(
            Create(predict_circle), Write(predict_text),
            Create(error_circle), Write(error_text),
            Create(adjust_circle), Write(adjust_text)
        )
        self.wait()
        
        self.play(
            Create(arrow1),
            Create(arrow2),
            Create(arrow3)
        )
        self.wait(2)

        # Show example iterations with improving predictions
        iterations_text = Text("Example: Predicting House Price", font_size=24, color=WHITE)
        iterations_text.to_edge(DOWN, buff=1)
        self.play(Write(iterations_text))
        self.wait()
        
        # Iteration tracker
        iteration_examples = VGroup(
            Text("Iteration 1: $280,000 → Error: $20,000", font_size=20, color=RED),
            Text("Iteration 2: $290,000 → Error: $10,000", font_size=20, color=ORANGE),
            Text("Iteration 3: $295,000 → Error: $5,000", font_size=20, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        iteration_examples.next_to(iterations_text, DOWN, buff=0.2)
        
        # Animate cycle and show iterations
        for i, example in enumerate(iteration_examples):
            # Highlight cycle
            self.play(
                Indicate(predict_circle, color=BLUE),
                run_time=0.4
            )
            self.play(
                Indicate(error_circle, color=ORANGE),
                run_time=0.4
            )
            self.play(
                Indicate(adjust_circle, color=GREEN),
                run_time=0.4
            )
            
            # Show iteration result
            self.play(Write(example))
            self.wait()
        
        self.wait()
        
        # Final message
        final_message = Text(
            "Thousands of iterations → Steady improvement",
            font_size=28,
            color=ORANGE,
            weight=BOLD
        )
        final_message.move_to(ORIGIN)
        
        self.play(
            FadeOut(predict_circle), FadeOut(predict_text),
            FadeOut(error_circle), FadeOut(error_text),
            FadeOut(adjust_circle), FadeOut(adjust_text),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3),
            FadeOut(iteration_title),
            FadeOut(iterations_text),
            FadeOut(iteration_examples)
        )
        
        self.play(Write(final_message))
        self.wait()
        
        # Final visual: Progress bar showing improvement
        progress_text = Text("Predictions move closer to target", font_size=24, color=GREEN, slant=ITALIC)
        progress_text.next_to(final_message, DOWN, buff=0.5)

        progress_bar_empty = Rectangle(height=0.5, width=8, color=GRAY, fill_opacity=0.2)
        progress_bar_empty.next_to(progress_text, DOWN, buff=0.4)
        progress_bar_fill = Rectangle(height=0.5, width=8, color=GREEN, fill_opacity=0.8)
        progress_bar_fill.align_to(progress_bar_empty, LEFT)
        progress_bar_fill.next_to(progress_text, DOWN, buff=0.4)
        self.play(Write(progress_text), Create(progress_bar_empty))

        # Start with width 0 and stretch to full width
        progress_bar_fill.stretch_to_fit_width(0.01)
        progress_bar_fill.align_to(progress_bar_empty, LEFT)

        self.play(
            progress_bar_fill.animate.stretch_to_fit_width(8).align_to(progress_bar_empty, LEFT),
            run_time=2,
            rate_func=smooth
        )
        
        self.wait()

class LearningRateVisualization(Scene):
    def construct(self):
        # Color scheme
        HIGH_LR_COLOR = RED
        LOW_LR_COLOR = BLUE
        GOOD_LR_COLOR = GREEN
        STEP_COLOR = YELLOW
        
        self.wait(5)

        # Question appears
        question = Text(
            "How big should each weight change be?",
            font_size=34,
            color=YELLOW
        )
        
        self.play(Write(question))
        self.wait()
        
        # Answer: Learning Rate
        answer = Text("Learning Rate", font_size=40, color=STEP_COLOR, weight=BOLD)
        answer.move_to(ORIGIN)
        
        self.play(
            FadeOut(question)
        )
        self.play(Write(answer))
        self.wait(2.5)
        
        # Definition
        definition = Text(
            "The 'step size' for weight adjustments",
            font_size=24,
            color=WHITE,
            slant=ITALIC
        )
        definition.next_to(answer, DOWN, buff=0.4)
        
        self.play(Write(definition))
        self.wait()
        
        self.play(
            FadeOut(answer),
            FadeOut(definition),
        )
        self.wait(0.2)
        
        # Create loss landscape for all three scenarios
        landscape_title = Text("Loss Landscape Comparison", font_size=28, color=WHITE)
        landscape_title.to_edge(UP, buff=0.5)
        self.play(Write(landscape_title))
        
        # Create three side-by-side loss curves
        # High learning rate (left)
        axes_high = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 5, 1],
            x_length=3,
            y_length=2.5,
            axis_config={"color": GRAY, "stroke_width": 2},
            tips=False
        )
        axes_high.shift(LEFT * 4 + DOWN * 0.5)
        
        # Low learning rate (middle)
        axes_low = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 5, 1],
            x_length=3,
            y_length=2.5,
            axis_config={"color": GRAY, "stroke_width": 2},
            tips=False
        )
        axes_low.shift(ORIGIN + DOWN * 0.5)
        
        # Good learning rate (right)
        axes_good = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 5, 1],
            x_length=3,
            y_length=2.5,
            axis_config={"color": GRAY, "stroke_width": 2},
            tips=False
        )
        axes_good.shift(RIGHT * 4 + DOWN * 0.5)
        
        # Loss curves (same for all)
        loss_curve_high = axes_high.plot(
            lambda x: min(x**2 + 0.5, 5.8),
            color=HIGH_LR_COLOR,
            stroke_width=3
        )
        
        loss_curve_low = axes_low.plot(
            lambda x: min(x**2 + 0.5, 5.8),
            color=LOW_LR_COLOR,
            stroke_width=3
        )
        
        loss_curve_good = axes_good.plot(
            lambda x: min(x**2 + 0.5, 5.8),
            color=GOOD_LR_COLOR,
            stroke_width=3
        )
        
        # Labels above each
        label_high = Text("Too Large", font_size=20, color=HIGH_LR_COLOR, weight=BOLD)
        label_high.next_to(axes_high, UP, buff=0.3)
        
        label_low = Text("Too Small", font_size=20, color=LOW_LR_COLOR, weight=BOLD)
        label_low.next_to(axes_low, UP, buff=0.3)
        
        label_good = Text("Just Right", font_size=20, color=GOOD_LR_COLOR, weight=BOLD)
        label_good.next_to(axes_good, UP, buff=0.3)
        
        # Create one a time
        # HIGH LEARNING RATE
        self.play(
            Create(axes_high),
            Create(loss_curve_high),
            Write(label_high),
        )
        self.wait()
        
        # HIGH LEARNING RATE - Zigzagging wildly
        high_lr_desc = Text("Huge steps → Unstable", font_size=18, color=HIGH_LR_COLOR)
        high_lr_desc.next_to(axes_high, DOWN, buff=0.3)
        self.play(Write(high_lr_desc))
        self.wait()
        
        # Starting point for high LR
        start_x_high = -2
        positions_high = [start_x_high]
        
        # Simulate overshooting with large steps
        current_x = start_x_high
        for i in range(8):
            # Large step that overshoots
            if current_x < 0:
                current_x += 1.8  # Overshoot to the right
            else:
                current_x -= 1.8  # Overshoot to the left
            positions_high.append(current_x)
        
        # Create dots and path
        dots_high = VGroup()
        for i, x in enumerate(positions_high):
            y = x**2 + 0.5
            dot = Dot(axes_high.c2p(x, y), color=HIGH_LR_COLOR, radius=0.06)
            dots_high.add(dot)
        
        # Animate the chaotic path
        self.play(FadeIn(dots_high[0]))
        
        for i in range(len(positions_high) - 1):
            arrow = Arrow(
                dots_high[i].get_center(),
                dots_high[i+1].get_center(),
                color=HIGH_LR_COLOR,
                buff=0.06,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            self.play(
                GrowArrow(arrow),
                FadeIn(dots_high[i+1]),
                run_time=0.4
            )
            if i < len(positions_high) - 2:  # Don't fade the last arrow
                self.play(FadeOut(arrow), run_time=0.2)
        
        # Add explosion/unstable effect
        explosion = Star(color=RED, fill_opacity=0.5, outer_radius=0.3)
        explosion.move_to(dots_high[-1].get_center())
        self.play(
            FadeIn(explosion, scale=0.5),
            Flash(dots_high[-1], color=RED, flash_radius=0.5)
        )
        self.wait()

        self.play(
            Create(axes_low),
            Create(loss_curve_low),
            Write(label_low),
        )
        self.wait()
        
        # LOW LEARNING RATE - Barely moving
        low_lr_desc = Text("Tiny steps → Too slow", font_size=18, color=LOW_LR_COLOR)
        low_lr_desc.next_to(axes_low, DOWN, buff=0.3)
        self.play(Write(low_lr_desc))
        self.wait()
        
        # Starting point for low LR
        start_x_low = -2
        positions_low = [start_x_low]
        
        # Simulate very small steps
        current_x = start_x_low
        for i in range(15):
            current_x += 0.15  # Very small steps
            positions_low.append(current_x)
        
        # Create dots and path
        dots_low = VGroup()
        for i, x in enumerate(positions_low):
            y = x**2 + 0.5
            dot = Dot(axes_low.c2p(x, y), color=LOW_LR_COLOR, radius=0.05)
            dots_low.add(dot)
        
        # Animate the slow path
        self.play(FadeIn(dots_low[0]))
        
        path_low = VGroup()
        for i in range(0, len(positions_low) - 1, 2):  # Skip some to speed up animation
            arrow = Arrow(
                dots_low[i].get_center(),
                dots_low[i+1].get_center(),
                color=LOW_LR_COLOR,
                buff=0.05,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.2
            )
            path_low.add(arrow)
            self.play(
                GrowArrow(arrow),
                FadeIn(dots_low[i+1]),
                run_time=0.25
            )
        
        # Add sleeping/bored effect
        snail = Text("🐌", font_size=30)
        snail.next_to(dots_low[-1], RIGHT, buff=0.2)
        self.play(FadeIn(snail))
        self.wait()

        self.play(
            Create(axes_good),
            Create(loss_curve_good),
            Write(label_good),
        )
        self.wait()
        
        # GOOD LEARNING RATE - Smooth descent
        good_lr_desc = Text("Steady steps → Efficient", font_size=18, color=GOOD_LR_COLOR)
        good_lr_desc.next_to(axes_good, DOWN, buff=0.3)
        self.play(Write(good_lr_desc))
        self.wait()
        
        # Starting point for good LR
        start_x_good = -2
        positions_good = [start_x_good]
        
        # Simulate optimal steps
        current_x = start_x_good
        for i in range(10):
            # Calculate gradient and take appropriate step
            gradient = 2 * current_x  # derivative of x^2
            current_x -= 0.25 * gradient  # Good learning rate * gradient
            positions_good.append(current_x)
        
        # Create dots and path
        dots_good = VGroup()
        for i, x in enumerate(positions_good):
            y = x**2 + 0.5
            dot = Dot(axes_good.c2p(x, y), color=GOOD_LR_COLOR, radius=0.06)
            dots_good.add(dot)
        
        # Animate the smooth path
        self.play(FadeIn(dots_good[0]))
        
        path_good = VGroup()
        for i in range(len(positions_good) - 1):
            arrow = Arrow(
                dots_good[i].get_center(),
                dots_good[i+1].get_center(),
                color=GOOD_LR_COLOR,
                buff=0.06,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.15
            )
            path_good.add(arrow)
            self.play(
                GrowArrow(arrow),
                FadeIn(dots_good[i+1]),
                run_time=0.3
            )
        
        # Add checkmark for success
        checkmark = Text("✓", font_size=40, color=GOOD_LR_COLOR, weight=BOLD)
        checkmark.next_to(dots_good[-1], DOWN, buff=0.2)
        self.play(
            FadeIn(checkmark, scale=0.5),
            Flash(dots_good[-1], color=GOOD_LR_COLOR, flash_radius=0.5)
        )
        self.wait()
        
        # Zoom out to show summary
        self.play(
            FadeOut(landscape_title),
        )
        self.wait()
        
        # Summary comparison table
        summary_title = Text("Learning Rate: Finding Balance", font_size=32, color=YELLOW, weight=BOLD)
        summary_title.to_edge(UP, buff=0.5)
        
        self.play(
            FadeIn(summary_title)
        )
        self.wait()
        
        # Create comparison boxes below the graphs
        comparison_y = -3
        
        # Too High box
        high_box = Rectangle(height=1, width=2.5, color=HIGH_LR_COLOR, stroke_width=3)
        high_box.move_to(LEFT * 4 + DOWN * 3)
        high_content = VGroup(
            Text("Too High", font_size=18, color=HIGH_LR_COLOR, weight=BOLD),
            Text("Overshoots", font_size=14, color=HIGH_LR_COLOR),
            Text("Unstable", font_size=14, color=HIGH_LR_COLOR)
        ).arrange(DOWN, buff=0.1)
        high_content.move_to(high_box.get_center())
        
        # Too Low box
        low_box = Rectangle(height=1, width=2.5, color=LOW_LR_COLOR, stroke_width=3)
        low_box.move_to(ORIGIN + DOWN * 3)
        low_content = VGroup(
            Text("Too Low", font_size=18, color=LOW_LR_COLOR, weight=BOLD),
            Text("Slow", font_size=14, color=LOW_LR_COLOR),
            Text("Inefficient", font_size=14, color=LOW_LR_COLOR)
        ).arrange(DOWN, buff=0.1)
        low_content.move_to(low_box.get_center())
        
        # Just Right box
        good_box = Rectangle(height=1, width=2.5, color=GOOD_LR_COLOR, stroke_width=3, fill_opacity=0.1, fill_color=GOOD_LR_COLOR)
        good_box.move_to(RIGHT * 4 + DOWN * 3)
        good_content = VGroup(
            Text("Just Right", font_size=18, color=GOOD_LR_COLOR, weight=BOLD),
            Text("Steady", font_size=14, color=GOOD_LR_COLOR),
            Text("Efficient", font_size=14, color=GOOD_LR_COLOR)
        ).arrange(DOWN, buff=0.1)
        good_content.move_to(good_box.get_center())
        
        self.play(
            Create(high_box), Write(high_content),
            Create(low_box), Write(low_content),
            Create(good_box), Write(good_content)
        )
        self.wait()
        
        # Highlight the winner
        winner_text = Text("Optimal Choice", font_size=20, color=GOOD_LR_COLOR, weight=BOLD)
        winner_text.next_to(good_box, DOWN, buff=0.1)
        
        self.play(
            Write(winner_text),
            good_box.animate.set_stroke(width=5),
            Flash(good_box, color=GOOD_LR_COLOR, line_length=0.4, num_lines=12)
        )
        self.wait(3)
        
        # Final key insight
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait()
        
        # Final message with visual metaphor
        final_message = Text(
            "A well-chosen learning rate:\nSteady, controlled steps that gradually reduce loss",
            font_size=26,
            color=GREEN,
            line_spacing=1.3
        )
        final_message.move_to(ORIGIN)
        
        final_box = SurroundingRectangle(final_message, color=GREEN, buff=0.4)
        final_box.set_stroke(width=3)
        
        self.play(Write(final_message), Create(final_box))
        self.wait()
        
        # Show step-by-step staircase metaphor
        staircase = VGroup()
        num_steps = 8
        step_width = 0.6
        step_height = 0.3
        
        for i in range(num_steps):
            step = Rectangle(
                height=step_height,
                width=step_width,
                color=GREEN,
                fill_opacity=0.3,
                stroke_width=2
            )
            step.shift(RIGHT * i * step_width + DOWN * i * step_height)
            staircase.add(step)
        
        staircase.next_to(final_message, DOWN, buff=0.7)
        staircase.shift(LEFT * 2)
        
        # Ball rolling down stairs
        ball = Dot(color=YELLOW, radius=0.15)
        ball.move_to(staircase[0].get_top())
        
        self.play(FadeIn(staircase), FadeIn(ball))
        
        # Animate ball going down stairs smoothly
        for i in range(num_steps - 1):
            self.play(
                ball.animate.move_to(staircase[i+1].get_top()),
                run_time=0.4,
                rate_func=smooth
            )
        
        self.wait()
        
        # Add label
        stair_label = Text("Gradual descent", font_size=20, color=GREEN, slant=ITALIC)
        stair_label.next_to(staircase, RIGHT, buff=0.5)
        self.play(Write(stair_label))
        self.wait()
        
        self.wait()

class CollectiveLearning(Scene):
    def construct(self):
        # Color scheme
        INPUT_COLOR = BLUE
        HIDDEN1_COLOR = TEAL
        HIDDEN2_COLOR = GREEN
        OUTPUT_COLOR = ORANGE
        ERROR_COLOR = RED
        SIGNAL_COLOR = YELLOW
        UPDATE_COLOR = PURPLE
        
        # Title
        title = Text("The Entire Network Learns Together", font_size=36, color=BLUE)
        title.to_edge(UP)
        
        # Subtitle
        subtitle = Text("Not one neuron at a time", font_size=24, color=GRAY, slant=ITALIC)
        subtitle.next_to(title, DOWN, buff=0.2)
        
        # Build the complete network
        # Input layer (3 neurons)
        input_neurons = VGroup(*[Circle(radius=0.25, color=INPUT_COLOR, fill_opacity=0.4, stroke_width=2) for _ in range(3)])
        input_neurons.arrange(DOWN, buff=0.4)
        input_neurons.shift(LEFT * 5)
        
        input_labels = VGroup(
            Text("Size", font_size=16),
            Text("Location", font_size=16),
            Text("Rooms", font_size=16)
        )
        for i, label in enumerate(input_labels):
            label.next_to(input_neurons[i], LEFT, buff=0.2)
        
        # Hidden layer 1 (4 neurons)
        hidden1_neurons = VGroup(*[Circle(radius=0.25, color=HIDDEN1_COLOR, fill_opacity=0.4, stroke_width=2) for _ in range(4)])
        hidden1_neurons.arrange(DOWN, buff=0.35)
        hidden1_neurons.shift(LEFT * 2.5)
        
        # Hidden layer 2 (3 neurons)
        hidden2_neurons = VGroup(*[Circle(radius=0.25, color=HIDDEN2_COLOR, fill_opacity=0.4, stroke_width=2) for _ in range(3)])
        hidden2_neurons.arrange(DOWN, buff=0.4)
        hidden2_neurons.shift(RIGHT * 0.5)
        
        # Output layer (1 neuron)
        output_neuron = Circle(radius=0.3, color=OUTPUT_COLOR, fill_opacity=0.4, stroke_width=2)
        output_neuron.shift(RIGHT * 3.5)
        
        output_label = Text("Price", font_size=16)
        output_label.next_to(output_neuron, RIGHT, buff=0.2)
        
        # Create all connections
        input_to_h1 = VGroup()
        for inp in input_neurons:
            for h1 in hidden1_neurons:
                line = Line(inp.get_right(), h1.get_left(), stroke_width=1, color=GRAY, stroke_opacity=0.3)
                input_to_h1.add(line)
        
        h1_to_h2 = VGroup()
        for h1 in hidden1_neurons:
            for h2 in hidden2_neurons:
                line = Line(h1.get_right(), h2.get_left(), stroke_width=1, color=GRAY, stroke_opacity=0.3)
                h1_to_h2.add(line)
        
        h2_to_output = VGroup()
        for h2 in hidden2_neurons:
            line = Line(h2.get_right(), output_neuron.get_left(), stroke_width=1, color=GRAY, stroke_opacity=0.3)
            h2_to_output.add(line)
        
        # Draw the network
        self.play(
            Create(input_to_h1),
            Create(h1_to_h2),
            Create(h2_to_output),
            Create(input_neurons),
            Create(hidden1_neurons),
            Create(hidden2_neurons),
            Create(output_neuron),
            Write(input_labels),
            Write(output_label),
            run_time=2
        )

        self.wait(3)

        self.play(Write(title))
        self.play(Write(subtitle))

        network = VGroup(
            input_to_h1,
            h1_to_h2,
            h2_to_output,
            input_neurons,
            hidden1_neurons,
            hidden2_neurons,
            output_neuron,
            input_labels,
            output_label
        )
        self.wait()
        
        self.play(FadeOut(subtitle))
        self.wait()
        
        # Show error signal from output
        error_text = Text("Error Signal", font_size=20, color=ERROR_COLOR, weight=BOLD)
        error_text.next_to(output_neuron, DOWN, buff=0.3)
        
        self.play(
            Write(error_text),
            output_neuron.animate.set_fill(ERROR_COLOR, opacity=0.8),
            Flash(output_neuron, color=ERROR_COLOR, flash_radius=0.5)
        )
        self.wait()
        
        # Error flows backward - layer by layer coordination
        flow_text = Text("Each layer receives signal from  the layer ahead", font_size=22, color=SIGNAL_COLOR)
        flow_text.to_edge(DOWN, buff=0.8)
        self.play(Write(flow_text))
        self.wait()
        
        # Signal to hidden layer 2
        signal_arrows_h2 = VGroup()
        for h2 in hidden2_neurons:
            arrow = Arrow(
                output_neuron.get_left(),
                h2.get_right(),
                color=SIGNAL_COLOR,
                stroke_width=2,
                buff=0.25,
                max_tip_length_to_length_ratio=0.15
            )
            signal_arrows_h2.add(arrow)
        
        self.play(
            *[GrowArrow(arrow) for arrow in signal_arrows_h2],
            *[line.animate.set_color(SIGNAL_COLOR).set_stroke(opacity=0.6) for line in h2_to_output],
            run_time=1
        )
        
        # Hidden layer 2 receives and processes
        h2_sensitivities = [0.8, 0.5, 0.9]  # Different sensitivities
        for i, (h2, sensitivity) in enumerate(zip(hidden2_neurons, h2_sensitivities)):
            self.play(
                h2.animate.set_fill(ERROR_COLOR, opacity=sensitivity),
                run_time=0.3
            )
        self.wait(5)
        
        # Show sensitivity concept
        sensitivity_text = Text("Each neuron considers its sensitivity to  the error", font_size=22, color=WHITE)
        sensitivity_text.move_to(flow_text.get_center())
        self.play(Transform(flow_text, sensitivity_text))
        self.wait()
        
        # Highlight neurons with different sensitivities
        high_sens_label = Text("High", font_size=14, color=RED, weight=BOLD)
        high_sens_label.next_to(hidden2_neurons[2], RIGHT + DOWN * 0.4, buff=0.1)
        low_sens_label = Text("Low", font_size=14, color=YELLOW)
        low_sens_label.next_to(hidden2_neurons[1], RIGHT + DOWN * 0.4, buff=0.1)
        
        self.play(Write(high_sens_label), Write(low_sens_label))
        self.wait()
        
        self.play(FadeOut(high_sens_label), FadeOut(low_sens_label))
        
        # Signal to hidden layer 1
        signal_arrows_h1 = VGroup()
        for h1 in hidden1_neurons:
            for h2 in hidden2_neurons:
                arrow = Arrow(
                    h2.get_left(),
                    h1.get_right(),
                    color=SIGNAL_COLOR,
                    stroke_width=1.5,
                    buff=0.25,
                    max_tip_length_to_length_ratio=0.09
                )
                signal_arrows_h1.add(arrow)
        
        self.play(
            *[GrowArrow(arrow) for arrow in signal_arrows_h1],
            *[line.animate.set_color(SIGNAL_COLOR).set_stroke(opacity=0.6) for line in h1_to_h2],
            run_time=1.2
        )
        
        # Hidden layer 1 processes
        h1_sensitivities = [0.6, 0.9, 0.4, 0.7]
        for h1, sensitivity in zip(hidden1_neurons, h1_sensitivities):
            self.play(
                h1.animate.set_fill(ERROR_COLOR, opacity=sensitivity),
                run_time=0.25
            )
        self.wait()
        
        # Signal to input layer
        signal_arrows_input = VGroup()
        for inp in input_neurons:
            for h1 in hidden1_neurons:
                arrow = Arrow(
                    h1.get_left(),
                    inp.get_right(),
                    color=SIGNAL_COLOR,
                    stroke_width=1.5,
                    buff=0.25,
                    max_tip_length_to_length_ratio=0.09
                )
                signal_arrows_input.add(arrow)
        
        self.play(
            *[GrowArrow(arrow) for arrow in signal_arrows_input],
            *[line.animate.set_color(SIGNAL_COLOR).set_stroke(opacity=0.6) for line in input_to_h1],
            run_time=1.2
        )
        
        # Input layer receives signals
        input_sensitivities = [0.7, 0.8, 0.5]
        for inp, sensitivity in zip(input_neurons, input_sensitivities):
            self.play(
                inp.animate.set_fill(ERROR_COLOR, opacity=sensitivity),
                run_time=0.25
            )
        self.wait(3)
        
        # Coordinated update message
        coordinated_text = Text("Coordinated weight updates across all layers", font_size=22, color=UPDATE_COLOR, weight=BOLD)
        coordinated_text.move_to(flow_text.get_center())
        self.play(Transform(flow_text, coordinated_text))
        self.wait()
        
        # Show simultaneous weight updates
        # Create weight update indicators on connections
        weight_updates = VGroup()
        
        # Sample some connections to show updates
        update_connections = [
            input_to_h1[2], input_to_h1[7], input_to_h1[10],
            h1_to_h2[3], h1_to_h2[8], h1_to_h2[11],
            h2_to_output[0], h2_to_output[1], h2_to_output[2]
        ]
        
        for conn in update_connections:
            # Small circle on the connection to show update
            update_dot = Dot(conn.get_center(), color=UPDATE_COLOR, radius=0.08)
            weight_updates.add(update_dot)
        
        self.play(
            *[FadeIn(dot, scale=0.5) for dot in weight_updates],
            *[Flash(dot, color=UPDATE_COLOR, flash_radius=0.2) for dot in weight_updates],
            run_time=1
        )
        self.wait()
        
        # Pulse all neurons to show synchronized update
        self.play(
            *[neuron.animate.scale(1.15) for neuron in input_neurons],
            *[neuron.animate.scale(1.15) for neuron in hidden1_neurons],
            *[neuron.animate.scale(1.15) for neuron in hidden2_neurons],
            output_neuron.animate.scale(1.15),
            run_time=0.4
        )
        self.play(
            *[neuron.animate.scale(1/1.15) for neuron in input_neurons],
            *[neuron.animate.scale(1/1.15) for neuron in hidden1_neurons],
            *[neuron.animate.scale(1/1.15) for neuron in hidden2_neurons],
            output_neuron.animate.scale(1/1.15),
            run_time=0.4
        )
        self.wait()
        
        # Clean up for internal representation section
        self.play(
            FadeOut(error_text),
            FadeOut(signal_arrows_h2),
            FadeOut(signal_arrows_h1),
            FadeOut(signal_arrows_input),
            FadeOut(weight_updates),
            FadeOut(flow_text)
        )
        self.wait()
        
        # Show internal representation transformation
        representation_text = Text("Reshaping internal representations", font_size=24, color=TEAL, weight=BOLD)
        representation_text.to_edge(DOWN, buff=0.8)
        self.play(Write(representation_text))
        self.wait()
        
        # Show features being extracted
        feature_labels_before = VGroup(
            Text("raw features", font_size=12, color=GRAY, slant=ITALIC),
            Text("simple patterns", font_size=12, color=GRAY, slant=ITALIC),
            Text("complex concepts", font_size=12, color=GRAY, slant=ITALIC)
        )
        feature_labels_before[0].next_to(input_neurons, DOWN, buff=0.3)
        feature_labels_before[1].next_to(hidden1_neurons, DOWN, buff=0.3)
        feature_labels_before[2].next_to(hidden2_neurons, DOWN, buff=0.3)
        
        self.play(Write(feature_labels_before))
        self.wait()
        
        # Transform to show improved understanding
        feature_labels_after = VGroup(
            Text("size, location, rooms", font_size=12, color=INPUT_COLOR, weight=BOLD),
            Text("neighborhood quality", font_size=12, color=HIDDEN1_COLOR, weight=BOLD),
            Text("market value indicators", font_size=12, color=HIDDEN2_COLOR, weight=BOLD)
        )
        feature_labels_after[0].move_to(feature_labels_before[0].get_center())
        feature_labels_after[1].move_to(feature_labels_before[1].get_center())
        feature_labels_after[2].move_to(feature_labels_before[2].get_center())
        
        self.play(
            Transform(feature_labels_before[0], feature_labels_after[0]),
            Transform(feature_labels_before[1], feature_labels_after[1]),
            Transform(feature_labels_before[2], feature_labels_after[2]),
            *[neuron.animate.set_fill(INPUT_COLOR, opacity=0.6) for neuron in input_neurons],
            *[neuron.animate.set_fill(HIDDEN1_COLOR, opacity=0.6) for neuron in hidden1_neurons],
            *[neuron.animate.set_fill(HIDDEN2_COLOR, opacity=0.6) for neuron in hidden2_neurons],
            output_neuron.animate.set_fill(OUTPUT_COLOR, opacity=0.6),
            *[line.animate.set_color(BLUE).set_stroke(opacity=0.5) for line in input_to_h1],
            *[line.animate.set_color(TEAL).set_stroke(opacity=0.5) for line in h1_to_h2],
            *[line.animate.set_color(GREEN).set_stroke(opacity=0.5) for line in h2_to_output],
            run_time=1.5
        )
        
        self.play(
            FadeOut(representation_text),
            FadeOut(feature_labels_before)
        )

        self.play(FadeOut(title))
        
        self.play(network.animate.shift(UP * 0.6).scale(0.9))
        
        # Create cycle diagram
        cycle_steps = VGroup(
            Text("1. Forward Propagation", font_size=20, color=BLUE),
            Text("2. Loss Calculation", font_size=20, color=ORANGE),
            Text("3. Backpropagation", font_size=20, color=RED),
            Text("4. Weight Updates", font_size=20, color=PURPLE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        cycle_steps.to_edge(DOWN, buff=1).shift(DOWN * 0.5)
        
        
        
        self.play(Write(cycle_steps))
        self.wait()
        
        # Animate the cycle repeating on the network
        num_cycles = 2
        for cycle in range(num_cycles):
            cycle_counter = Text(f"Cycle {cycle + 1}", font_size=26, color=YELLOW, weight=BOLD)
            cycle_counter.to_edge(UP, buff=0.5)
            self.play(FadeIn(cycle_counter))
            
            # Forward pass (quick)
            self.play(Indicate(cycle_steps[0], color=BLUE), run_time=0.3)
            self.play(
                *[neuron.animate.set_fill(BLUE, opacity=0.7) for neuron in input_neurons],
                run_time=0.3
            )
            self.play(
                *[neuron.animate.set_fill(TEAL, opacity=0.7) for neuron in hidden1_neurons],
                run_time=0.3
            )
            self.play(
                *[neuron.animate.set_fill(GREEN, opacity=0.7) for neuron in hidden2_neurons],
                run_time=0.3
            )
            self.play(
                output_neuron.animate.set_fill(ORANGE, opacity=0.9),
                run_time=0.3
            )
            
            # Loss calculation
            self.play(Indicate(cycle_steps[1], color=ORANGE), run_time=0.3)
            self.play(Flash(output_neuron, color=ORANGE), run_time=0.3)
            
            # Backprop (quick)
            self.play(Indicate(cycle_steps[2], color=RED), run_time=0.3)
            self.play(
                output_neuron.animate.set_fill(RED, opacity=0.7),
                *[neuron.animate.set_fill(RED, opacity=0.5) for neuron in hidden2_neurons],
                *[neuron.animate.set_fill(RED, opacity=0.4) for neuron in hidden1_neurons],
                *[neuron.animate.set_fill(RED, opacity=0.3) for neuron in input_neurons],
                run_time=0.8
            )
            
            # Weight update
            self.play(Indicate(cycle_steps[3], color=PURPLE), run_time=0.3)
            self.play(
                *[neuron.animate.scale(1.1) for neuron in input_neurons],
                *[neuron.animate.scale(1.1) for neuron in hidden1_neurons],
                *[neuron.animate.scale(1.1) for neuron in hidden2_neurons],
                output_neuron.animate.scale(1.1),
                run_time=0.3
            )
            self.play(
                *[neuron.animate.scale(1/1.1) for neuron in input_neurons],
                *[neuron.animate.scale(1/1.1) for neuron in hidden1_neurons],
                *[neuron.animate.scale(1/1.1) for neuron in hidden2_neurons],
                output_neuron.animate.scale(1/1.1),
                run_time=0.3
            )
            
            self.play(FadeOut(cycle_counter))
        
        self.wait()
        
        # Show "many more cycles" with fade effect
        many_cycles_text = Text("+ thousands more cycles...", font_size=26, color=GRAY, slant=ITALIC)
        many_cycles_text.to_edge(UP, buff=0.5)
        self.play(Write(many_cycles_text))
        self.wait()
        
        # Show network getting better with glow effect
        self.play(
            *[neuron.animate.set_fill(GREEN, opacity=0.8).set_stroke(GREEN, width=3) for neuron in input_neurons],
            *[neuron.animate.set_fill(GREEN, opacity=0.8).set_stroke(GREEN, width=3) for neuron in hidden1_neurons],
            *[neuron.animate.set_fill(GREEN, opacity=0.8).set_stroke(GREEN, width=3) for neuron in hidden2_neurons],
            output_neuron.animate.set_fill(GREEN, opacity=0.9).set_stroke(GREEN, width=3),
            *[line.animate.set_color(GREEN).set_stroke(opacity=0.8, width=2) for line in input_to_h1],
            *[line.animate.set_color(GREEN).set_stroke(opacity=0.8, width=2) for line in h1_to_h2],
            *[line.animate.set_color(GREEN).set_stroke(opacity=0.8, width=2) for line in h2_to_output],
            run_time=2
        )
        self.wait()
        
        # Clean up for final message
        self.play(
            FadeOut(cycle_steps),
            FadeOut(many_cycles_text),
            FadeOut(network)
        )
        self.wait()
        
        # Final message
        final_message = VGroup(
            Text("Learning doesn't happen all at once", font_size=26, color=WHITE),
            Text("It emerges from many small,", font_size=26, color=YELLOW),
            Text("synchronized updates", font_size=26, color=YELLOW, weight=BOLD),
            Text("across the entire network", font_size=26, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.3, center=False, aligned_edge=LEFT)
        final_message.move_to(ORIGIN).shift(RIGHT * 0.5)
        
        final_box = SurroundingRectangle(final_message, color=YELLOW, buff=0.4)
        final_box.set_stroke(width=3)
        
        self.play(Write(final_message), Create(final_box))
        
        self.wait()

class BackpropOpening(Scene):
    def construct(self):
        # Color scheme
        QUESTION_COLOR = YELLOW
        ANSWER_COLOR = ORANGE
        ERROR_COLOR = RED
        NETWORK_COLOR = BLUE
        
        # The big question
        big_question = Text(
            "How does the network actually\nlearn from its mistakes?",
            font_size=36,
            color=QUESTION_COLOR,
            weight=BOLD,
            line_spacing=1.2
        )
        big_question.move_to(ORIGIN)
        
        self.play(Write(big_question))
        self.wait()
        
        # Transition to answer
        self.play(
            FadeOut(big_question),
        )
        
        # The answer appears
        answer_label = Text("The Answer:", font_size=28, color=WHITE)
        answer_label.shift(UP * 1)
        
        self.play(Write(answer_label))
        
        # "Backpropagation" appears with impact
        backprop_title = Text("Backpropagation", font_size=56, color=YELLOW, weight=BOLD)
        backprop_title.next_to(answer_label, DOWN, buff=0.5)
        
        self.play(
            Write(backprop_title),
        )
        self.wait()
        
        # Clear for preview
        self.play(
            FadeOut(answer_label),
            backprop_title.animate.move_to(ORIGIN)
        )
        self.wait()
        
        # Show what we'll learn - breakdown
        breakdown_title = Text("What we'll explore:", font_size=28, color=WHITE)
        breakdown_title.to_edge(UP, buff=0.8)
        
        breakdown_items = VGroup(
            Text("• How error flows backward through the network", font_size=24, color=BLUE),
            Text("• How each neuron learns to adjust", font_size=24, color=GREEN),
            Text("• How weights and biases are updated", font_size=24, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        breakdown_items.next_to(breakdown_title, DOWN, buff=0.5)
        
        self.play(
            Transform(backprop_title, breakdown_title)
        )
        self.wait()
        
        # Animate items appearing one by one
        for item in breakdown_items:
            self.play(Write(item))
            self.wait()
        
        # Transition to visualization
        self.play(
            FadeOut(backprop_title),
            FadeOut(breakdown_items)
        )
        
        # Final call to action
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        dive_in = Text("Let's dive in!", font_size=48, color=BLUE, weight=BOLD)
        dive_in.move_to(ORIGIN)
        
        self.play(
            Write(dive_in),
        )
        self.wait()

class BackpropTakeaways(Scene):
    def construct(self):
        # Title
        title = Text("Key Takeaways", font_size=42, color=BLUE, weight=BOLD)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title))
        self.wait()
        
        # Bullet points
        takeaway_1 = Text(
            "• Backpropagation is the learning engine of neural networks",
            font_size=26,
            color=WHITE
        )
        takeaway_1.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=1)
        
        takeaway_2 = Text(
            "• It sends error backward, telling weights and biases how to adjust",
            font_size=26,
            color=WHITE
        )
        takeaway_2.next_to(takeaway_1, DOWN, buff=0.5, aligned_edge=LEFT)
        
        takeaway_3 = Text(
            "• Repeated thousands of times, networks learn and improve",
            font_size=26,
            color=WHITE
        )
        takeaway_3.next_to(takeaway_2, DOWN, buff=0.5, aligned_edge=LEFT)
        
        takeaway_4 = Text(
            "• In deeper networks, gradient updates face challenges:",
            font_size=26,
            color=YELLOW,
            weight=BOLD
        )
        takeaway_4.next_to(takeaway_3, DOWN, buff=0.6, aligned_edge=LEFT)
        
        challenge_1 = Text(
            "  - Updates can become too small",
            font_size=24,
            color=ORANGE
        )
        challenge_1.next_to(takeaway_4, DOWN, buff=0.3, aligned_edge=LEFT)
        
        challenge_2 = Text(
            "  - Updates can become too large",
            font_size=24,
            color=ORANGE
        )
        challenge_2.next_to(challenge_1, DOWN, buff=0.3, aligned_edge=LEFT)
        
        challenge_3 = Text(
            "  - Learning becomes slow, unstable, or impossible",
            font_size=24,
            color=RED
        )
        challenge_3.next_to(challenge_2, DOWN, buff=0.3, aligned_edge=LEFT)
        
        # Animate each takeaway appearing
        self.play(Write(takeaway_1))
        self.wait(2.5)
        
        self.play(Write(takeaway_2))
        self.wait(5)
        
        self.play(Write(takeaway_3))
        self.wait(9)
        
        self.play(Write(takeaway_4))
        self.wait(5)
        
        self.play(Write(challenge_1))
        self.wait()
        
        self.play(Write(challenge_2))
        self.wait()
        
        self.play(Write(challenge_3))
        
        # Fade out for next section
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Next video section
        next_title = Text("Coming Up Next", font_size=40, color=ORANGE, weight=BOLD)
        next_title.move_to(ORIGIN + UP * 1)
        
        self.play(Write(next_title))
        
        next_content = VGroup(
            Text("Exploring the challenges of deep learning:", font_size=28, color=WHITE),
            Text("• Why gradient problems happen", font_size=26, color=YELLOW),
            Text("• How modern optimization overcome them", font_size=26, color=GREEN)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        next_content.next_to(next_title, DOWN, buff=0.8)
        
        self.play(Write(next_content[0]))
        self.wait()
        
        self.play(Write(next_content[1]))
        self.wait()
        
        self.play(Write(next_content[2]))
        self.wait()
        
        self.wait()

class BackpropBridge(Scene):
    def construct(self):
        # Color scheme
        ERROR_COLOR = RED
        QUESTION_COLOR = YELLOW
        NETWORK_COLOR = BLUE
        BACKPROP_COLOR = ORANGE
        
        # "Knowing the error isn't enough"
        not_enough = Text(
            "Knowing the error isn't enough",
            font_size=32,
            color=ERROR_COLOR,
            weight=BOLD
        )
        not_enough.move_to(ORIGIN)
        
        self.play(Write(not_enough))
        self.wait()
        
        self.play(not_enough.animate.to_edge(UP, buff=1))
        self.wait()
        
        # Two important questions
        questions_title = Text("The network needs to answer:", font_size=26, color=WHITE)
        questions_title.next_to(not_enough, DOWN, buff=0.6)
        
        question_1 = Text(
            "1. Which weights led to this error?",
            font_size=28,
            color=QUESTION_COLOR
        )
        question_1.next_to(questions_title, DOWN, buff=0.5).shift(LEFT * 0.5)
        
        question_2 = Text(
            "2. How should they change?",
            font_size=28,
            color=QUESTION_COLOR
        )
        question_2.next_to(question_1, DOWN, buff=0.4, aligned_edge=LEFT)
        
        self.play(Write(questions_title))
        self.wait()
        
        self.play(Write(question_1))
        self.wait(2)
        
        self.play(Write(question_2))
        self.wait(6)
        
        # Clear for network visualization
        self.play(
            FadeOut(not_enough),
            FadeOut(questions_title),
            FadeOut(question_1),
            FadeOut(question_2)
        )
        self.wait()
        
        # Simple network showing many layers working together
        reminder = Text(
            "Many layers and weights working together",
            font_size=28,
            color=WHITE,
            slant=ITALIC
        )
        reminder.to_edge(UP, buff=0.8)
        
        self.play(Write(reminder))
        self.wait()
        
        # Create simple multi-layer network
        layer1 = VGroup(*[Circle(radius=0.2, color=BLUE, fill_opacity=0.5) for _ in range(3)])
        layer1.arrange(DOWN, buff=0.3).shift(LEFT * 4)
        
        layer2 = VGroup(*[Circle(radius=0.2, color=BLUE, fill_opacity=0.5) for _ in range(4)])
        layer2.arrange(DOWN, buff=0.25).shift(LEFT * 2)
        
        layer3 = VGroup(*[Circle(radius=0.2, color=BLUE, fill_opacity=0.5) for _ in range(3)])
        layer3.arrange(DOWN, buff=0.3).shift(ORIGIN)
        
        output = Circle(radius=0.25, color=BLUE, fill_opacity=0.5)
        output.shift(RIGHT * 2.5)
        
        # All connections
        all_connections = VGroup()
        layers = [layer1, layer2, layer3]
        for i in range(len(layers) - 1):
            for n1 in layers[i]:
                for n2 in layers[i + 1]:
                    line = Line(n1.get_right(), n2.get_left(), stroke_width=1, color=GRAY, stroke_opacity=0.3)
                    all_connections.add(line)
        
        for n in layer3:
            line = Line(n.get_right(), output.get_left(), stroke_width=1, color=GRAY, stroke_opacity=0.3)
            all_connections.add(line)
        
        network = VGroup(all_connections, layer1, layer2, layer3, output)
        
        self.play(FadeIn(network))
        self.wait()
        
        # Show error at output
        error_label = Text("Error", font_size=24, color=ERROR_COLOR, weight=BOLD)
        error_label.next_to(output, RIGHT, buff=0.3)
        
        self.play(
            output.animate.set_fill(ERROR_COLOR, opacity=0.9),
            Write(error_label),
            Flash(output, color=ERROR_COLOR)
        )
        self.wait()
        
        # Backpropagation enters
        self.play(FadeOut(reminder))
        
        backprop_title = Text("Backpropagation", font_size=32, color=BACKPROP_COLOR, weight=BOLD)
        backprop_title.to_edge(UP, buff=0.8)
        
        self.play(Write(backprop_title))
        self.wait()
        
        # Show backward flow with simple arrows
        backward_text = Text(
            "Sends error backward, layer by layer",
            font_size=24,
            color=BACKPROP_COLOR
        )
        backward_text.to_edge(DOWN, buff=1)
        
        self.play(Write(backward_text))
        self.wait()
        
        # Animate backward arrows
        arrow1 = Arrow(output.get_left(), layer3[1].get_right(), color=BACKPROP_COLOR, stroke_width=3, buff=0.2)
        self.play(GrowArrow(arrow1), run_time = 0.5)
        self.play(*[n.animate.set_fill(BACKPROP_COLOR, opacity=0.7) for n in layer3])
        self.wait()
        
        arrow2 = Arrow(layer3[1].get_left(), layer2[1].get_right(), color=BACKPROP_COLOR, stroke_width=3, buff=0.2)
        self.play(GrowArrow(arrow2), run_time = 0.5)
        self.play(*[n.animate.set_fill(BACKPROP_COLOR, opacity=0.6) for n in layer2])
        self.wait()
        
        arrow3 = Arrow(layer2[1].get_left(), layer1[1].get_right(), color=BACKPROP_COLOR, stroke_width=3, buff=0.2)
        self.play(GrowArrow(arrow3), run_time = 0.5)
        self.play(*[n.animate.set_fill(BACKPROP_COLOR, opacity=0.5) for n in layer1])
        
        # Final message
        self.play(FadeOut(backward_text))
        
        bridge_message = Text(
            "The bridge between measuring mistakes\nand learning from them",
            font_size=28,
            color=GREEN,
            weight=BOLD,
            line_spacing=1.2
        )
        bridge_message.to_edge(DOWN, buff=0.8)
        
        self.play(Write(bridge_message))
        self.wait()
        
        self.wait()