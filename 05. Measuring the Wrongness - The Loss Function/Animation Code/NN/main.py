from turtle import circle
from manim import *
import numpy as np

class LossFunctionIntro(Scene):
    def construct(self):
        # Part 1: Quick recap of forward propagation
        self.recap_forward_propagation()
        self.wait()
        
        # Part 2: Introduce the measurement question
        self.introduce_measurement_question()
        self.wait()
        
        # Part 3: House price example with error
        self.show_house_price_example()
        self.wait()
        
        # Part 4: Loss function concept
        self.show_loss_function_concept()
        self.wait()
        
        # Part 5: Small vs Large loss
        self.show_loss_comparison()
        self.wait()
        
        # Part 6: Performance score metaphor
        self.show_performance_score()
        self.wait()
    
    def recap_forward_propagation(self):
        """Brief visual recap of forward propagation"""
        title = Text("Forward Propagation Recap", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Simple neural network
        input_layer = VGroup(*[Circle(radius=0.3, color=GREEN, fill_opacity=0.5) for _ in range(3)])
        input_layer.arrange(DOWN, buff=0.5).shift(LEFT * 4)
        
        hidden_layer = VGroup(*[Circle(radius=0.3, color=BLUE, fill_opacity=0.5) for _ in range(4)])
        hidden_layer.arrange(DOWN, buff=0.4).shift(LEFT * 1)
        
        output_layer = Circle(radius=0.3, color=RED, fill_opacity=0.5).shift(RIGHT * 2)
        
        # Labels
        input_labels = VGroup(
            Text("Size", font_size=16).next_to(input_layer[0], LEFT),
            Text("Bedrooms", font_size=16).next_to(input_layer[1], LEFT),
            Text("Location", font_size=16).next_to(input_layer[2], LEFT)
        )
        
        output_label = Text("Price", font_size=16).next_to(output_layer, RIGHT)
        
        # Create connections
        connections = VGroup()
        for input_node in input_layer:
            for hidden_node in hidden_layer:
                connections.add(Line(input_node.get_right(), hidden_node.get_left(), 
                                   stroke_width=1, color=GRAY, stroke_opacity=0.3))
        
        for hidden_node in hidden_layer:
            connections.add(Line(hidden_node.get_right(), output_layer.get_left(),
                               stroke_width=1, color=GRAY, stroke_opacity=0.3))
        
        self.play(Create(connections), run_time=0.5)
        self.play(
            FadeIn(input_layer),
            FadeIn(hidden_layer),
            FadeIn(output_layer),
            Write(input_labels),
            Write(output_label)
        )
        self.wait()
        
        # Animate data flow
        data_dots = VGroup(*[Dot(color=YELLOW).move_to(node) for node in input_layer])
        self.play(FadeIn(data_dots))
        
        # Flow to hidden layer
        self.play(*[dot.animate.move_to(hidden_layer[i % len(hidden_layer)]) 
                   for i, dot in enumerate(data_dots)], run_time=1.5)
        
        # Flow to output
        self.play(*[dot.animate.move_to(output_layer) for dot in data_dots], run_time=1.5)

        self.wait(3)
        
        # Show prediction
        prediction = Text("First Guess!", font_size=24, color=YELLOW).next_to(output_layer, DOWN)
        self.play(Write(prediction))
        self.wait(5)
        
        # Clear for next section
        self.play(
            FadeOut(VGroup(connections, input_layer, hidden_layer, output_layer, 
                          input_labels, output_label, data_dots, prediction, title))
        )
    
    def introduce_measurement_question(self):
        """Show the key question about measuring prediction quality"""
        question = Text("How do we measure\nif it's any good?", font_size=48, color=YELLOW)
        question.move_to(ORIGIN)
        
        self.play(Write(question))
        self.wait(4)
        
        # Transition to loss function
        answer = Text("Loss Function", font_size=56, color=RED, weight=BOLD)
        answer.move_to(ORIGIN)
        
        self.play(Transform(question, answer))
        self.wait()
        
        subtitle = Text("A scoring system for predictions", font_size=28, color=WHITE)
        subtitle.next_to(answer, DOWN, buff=0.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait()
        
        self.play(FadeOut(question), FadeOut(subtitle))
    
    def show_house_price_example(self):
        """Show the house price prediction vs actual example"""
        title = Text("House Price Prediction", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # House icon
        house = VGroup(
            Polygon([-0.5, 0, 0], [0.5, 0, 0], [0, 0.7, 0], color=BLUE, fill_opacity=0.7),
            Rectangle(width=1, height=0.8, color=BLUE, fill_opacity=0.7).shift(DOWN * 0.4)
        ).scale(1.5).shift(UP * 1.5)
        
        self.play(FadeIn(house))
        self.wait()
        
        # Show prediction and actual values
        prediction_box = VGroup(
            Rectangle(width=4, height=1, color=ORANGE, fill_opacity=0.2),
            Text("Network Predicts:", font_size=20, color=WHITE).shift(UP * 0.25),
            Text("$280,000", font_size=32, color=ORANGE, weight=BOLD).shift(DOWN * 0.15)
        ).shift(LEFT * 3 + DOWN * 1)
        
        actual_box = VGroup(
            Rectangle(width=4, height=1, color=GREEN, fill_opacity=0.2),
            Text("Actual Price:", font_size=20, color=WHITE).shift(UP * 0.25),
            Text("$300,000", font_size=32, color=GREEN, weight=BOLD).shift(DOWN * 0.15)
        ).shift(RIGHT * 3 + DOWN * 1)
        
        self.play(FadeIn(prediction_box, shift=RIGHT))
        self.wait(3)
        self.play(FadeIn(actual_box, shift=LEFT))
        self.wait(3)
        
        # Show the difference with red bar
        difference_label = Text("Error (Difference)", font_size=28, color=RED)
        difference_label.shift(DOWN * 2.5)
        
        # Visual bar showing the error
        error_bar = Rectangle(width=2, height=0.4, color=RED, fill_opacity=0.7)
        error_bar.next_to(difference_label, DOWN, buff=0.3)
        
        error_value = Text("$20,000", font_size=28, color=WHITE, weight=BOLD).move_to(error_bar.get_center())
        
        self.play(Write(difference_label))
        self.play(GrowFromCenter(error_bar))
        self.play(Write(error_value))
        self.wait(1.5)
        
        # Store for transition
        self.house_example = VGroup(title, house, prediction_box, actual_box, 
                                    difference_label, error_bar, error_value)
    
    def show_loss_function_concept(self):
        """Show how loss function converts error to loss value"""
        self.play(FadeOut(self.house_example))
        
        title = Text("Loss Function", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # Show the conversion process
        error_text = Text("Error: $20,000", font_size=32, color=ORANGE)
        error_text.shift(LEFT * 3)
        
        arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, color=YELLOW, buff=0.2, stroke_width=6)
        
        loss_func_box = VGroup(
            RoundedRectangle(width=2, height=1.0, corner_radius=0.2, color=BLUE, fill_opacity=0.3),
            Text("Loss\nFunction", font_size=24, color=WHITE)
        ).next_to(arrow, UP, buff=0.5)
        
        loss_value = VGroup(
            Text("Loss Value:", font_size=28, color=WHITE),
            Text("eg: 400,000,000", font_size=30, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.2).shift(RIGHT * 3.5)
        
        self.play(Write(error_text))
        self.wait()
        self.play(GrowArrow(arrow))
        self.play(FadeIn(loss_func_box, scale=0.8))
        self.wait()
        self.play(Write(loss_value))
        self.wait()
        
        # Show interpretation
        interpretation = VGroup(
            Text("Small Loss = Good Prediction", font_size=28, color=GREEN),
            Text("Large Loss = Poor Prediction", font_size=28, color=RED)
        ).arrange(DOWN, buff=0.4)
        
        self.play(FadeOut(error_text), FadeOut(arrow), FadeOut(loss_func_box), 
                  FadeOut(loss_value), FadeOut(title))
        self.play(Write(interpretation[0]))
        self.wait()
        self.play(Write(interpretation[1]))
        self.wait()
        
        self.play(FadeOut(interpretation))
    
    def show_loss_comparison(self):
        """Visual comparison of small vs large loss"""
        title = Text("Understanding Loss Values", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # Good prediction scenario
        good_scenario = VGroup(
            Text("Prediction: $298,000", font_size=24, color=ORANGE),
            Text("Actual: $300,000", font_size=24, color=GREEN),
            Rectangle(width=0.5, height=0.3, color=GREEN, fill_opacity=0.7),
            Text("Loss = 4,000,000", font_size=20, color=GREEN, weight=BOLD),
            Text("✓ Good!", font_size=28, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.3).shift(LEFT * 3.5 + DOWN * 0.5)
        
        # Poor prediction scenario
        poor_scenario = VGroup(
            Text("Prediction: $200,000", font_size=24, color=ORANGE),
            Text("Actual: $300,000", font_size=24, color=GREEN),
            Rectangle(width=3, height=0.3, color=RED, fill_opacity=0.7),
            Text("Loss = 2,500,000,000", font_size=20, color=RED, weight=BOLD),
            Text("✗ Poor!", font_size=28, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.3).shift(RIGHT * 3.5 + DOWN * 0.5)
        
        self.play(FadeIn(good_scenario, shift=RIGHT))
        self.wait()
        self.play(FadeIn(poor_scenario, shift=LEFT))
        self.wait()
        
        self.play(FadeOut(title), FadeOut(good_scenario), FadeOut(poor_scenario))
    
    def show_performance_score(self):
        """Show loss as a performance score"""
        title = Text("Loss = Performance Score", font_size=44, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Report card visual
        report_card = VGroup(
            RoundedRectangle(width=6, height=4, corner_radius=0.3, color=WHITE, stroke_width=3),
            Text("Network Performance", font_size=28, color=BLUE, weight=BOLD).shift(UP * 1.3),
            Text("Loss Score: 400,000,000", font_size=24, color=RED).shift(UP * 0.5),
            Text("Grade: Needs Improvement", font_size=22, color=ORANGE).shift(DOWN * 0.2),
            Line(LEFT * 2.5, RIGHT * 2.5, color=GRAY).shift(DOWN * 0.7),
            Text("This score guides learning", font_size=20, color=WHITE, slant=ITALIC).shift(DOWN * 1.3)
        )
        
        self.play(FadeIn(report_card, scale=0.9))
        self.wait()
        
        # Final message
        final_message = Text(
            "The network uses this score\nto improve over time",
            font_size=28,
            color=YELLOW,
            weight=BOLD
        ).shift(DOWN * 3)
        
        self.play(Write(final_message))
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(VGroup(title, report_card, final_message)))
        self.wait()

class LossFunctionBehavior(Scene):
    def construct(self):
        # Part 1: Introduce the concept of multiple predictions
        self.introduce_multiple_predictions()
        self.wait()
        
        # Part 2: Show 10 houses with predictions
        self.show_ten_houses()
        self.wait()
        
        # Part 3: Individual errors to average loss
        self.show_error_aggregation()
        self.wait()
        
        # Part 4: Practical meaning - good vs poor performance
        self.show_performance_scenarios()
        self.wait()
        
        # Part 5: Single reliable signal
        self.show_single_signal_concept()
        self.wait()
    
    def introduce_multiple_predictions(self):
        """Introduce concept of loss across dataset"""
        title = Text("Loss Across the Dataset", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        subtitle = Text(
            "The loss function measures performance\nacross ALL examples",
            font_size=28,
            color=WHITE
        ).next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(subtitle, shift=UP))
        self.wait()
        
        # Show transition from one to many
        one_house = Text("1 House", font_size=36, color=ORANGE)
        one_house.shift(LEFT * 3)
        
        arrow = Arrow(LEFT * 1, RIGHT * 1, color=YELLOW, stroke_width=6)
        
        many_houses = Text("Multiple Houses", font_size=36, color=GREEN)
        many_houses.shift(RIGHT * 3.5)
        
        self.play(Write(one_house))
        self.wait()
        self.play(GrowArrow(arrow))
        self.play(Write(many_houses))
        self.wait()
        
        self.play(FadeOut(VGroup(title, subtitle, one_house, arrow, many_houses)))
    
    def show_ten_houses(self):
        """Show 10 houses with predictions and actuals"""
        title = Text("10 House Predictions", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # Create 10 small house icons in two rows
        houses = VGroup()
        for i in range(10):
            house = self.create_small_house()
            houses.add(house)
        
        houses.arrange_in_grid(rows=2, cols=5, buff=0.8)
        houses.scale(0.7).shift(UP * 0.5)
        
        self.play(LaggedStart(*[FadeIn(house, scale=0.5) for house in houses], lag_ratio=0.1))
        self.wait()
        
        # Sample data: (predicted, actual) for 10 houses
        self.house_data = [
            (295, 300),  # Close
            (310, 300),  # Close
            (250, 300),  # Far
            (305, 300),  # Close
            (280, 300),  # Moderate
            (298, 300),  # Very close
            (320, 300),  # Moderate
            (270, 300),  # Far
            (302, 300),  # Very close
            (290, 300),  # Close
        ]
        
        # Show predictions vs actuals for each house
        predictions_text = Text("Predictions", font_size=20, color=ORANGE).shift(DOWN * 1.8 + LEFT * 4)
        actuals_text = Text("Actuals", font_size=20, color=GREEN).shift(DOWN * 1.8 + RIGHT * 4)
        
        self.play(Write(predictions_text), Write(actuals_text))
        
        # Display some sample values
        sample_predictions = VGroup()
        for i in range(5):
            pred, actual = self.house_data[i]
            text = Text(f"${pred}k", font_size=14, color=ORANGE)
            text.next_to(houses[i], DOWN, buff=0.1)
            sample_predictions.add(text)
        
        sample_actuals = VGroup()
        for i in range(5):
            pred, actual = self.house_data[i]
            text = Text(f"${actual}k", font_size=14, color=GREEN)
            text.next_to(houses[i+5], DOWN, buff=0.1)
            sample_actuals.add(text)
        
        self.play(LaggedStart(*[Write(text) for text in sample_predictions], lag_ratio=0.1))
        self.play(LaggedStart(*[Write(text) for text in sample_actuals], lag_ratio=0.1))
        self.wait()
        
        # Store for next section
        self.houses_group = VGroup(title, houses, predictions_text, actuals_text, 
                                   sample_predictions, sample_actuals)
    
    def show_error_aggregation(self):
        """Show individual errors combining into average loss"""
        self.play(FadeOut(self.houses_group))
        
        title = Text("Combining Individual Errors", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # Create chart showing individual errors
        axes = Axes(
            x_range=[0, 11, 1],
            y_range=[0, 60, 10],
            x_length=10,
            y_length=4,
            axis_config={"color": GRAY},
            tips=False
        ).shift(DOWN * 0.5)
        
        x_label = Text("House #", font_size=20).next_to(axes.x_axis, DOWN)
        y_label = Text("Error ($k)", font_size=20).next_to(axes.y_axis, LEFT)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        
        # Calculate errors and create bars
        errors = [abs(pred - actual) for pred, actual in self.house_data]
        bars = VGroup()
        
        for i, error in enumerate(errors):
            bar_height = error / 60 * 4  # Scale to axes
            bar = Rectangle(
                width=0.6,
                height=bar_height,
                color=RED,
                fill_opacity=0.7,
                stroke_width=2
            )
            bar.move_to(axes.c2p(i + 1, 0), aligned_edge=DOWN)
            bars.add(bar)
        
        # Animate bars appearing
        self.play(LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.08))
        
        error_labels = VGroup()
        # Label some bars with error values
        for i in [2, 7]:  # Show largest errors
            error_label = Text(f"${errors[i]}k", font_size=12, color=RED)
            error_label.next_to(bars[i], UP, buff=0.1)
            self.play(FadeIn(error_label, scale=0.5), run_time=0.3)
            error_labels.add(error_label)
        
        self.wait()
        
        # Show averaging process
        avg_text = Text("Taking the Average...", font_size=28, color=YELLOW)
        avg_text.next_to(axes, DOWN, buff=0.8)
        self.play(Write(avg_text))
        
        # Calculate average error
        avg_error = sum(errors) / len(errors)
        
        # Show all bars moving towards average
        avg_line = DashedLine(
            axes.c2p(0, avg_error), 
            axes.c2p(11, avg_error),
            color=YELLOW,
            stroke_width=4
        )
        
        self.play(Create(avg_line))
        
        avg_label = Text(f"Average \nError: \n${avg_error:.1f}k", font_size=24, color=YELLOW, weight=BOLD)
        avg_label.next_to(avg_line, RIGHT, buff=0.2)
        self.play(Write(avg_label))
        self.wait()
        
        # Transform to single overall loss bar
        self.play(FadeOut(VGroup(axes, x_label, y_label, bars, avg_line, avg_text, error_labels)))
        
        overall_loss_box = VGroup(
            RoundedRectangle(width=5, height=2, corner_radius=0.2, color=BLUE, fill_opacity=0.3),
            Text("Overall Loss", font_size=32, color=WHITE, weight=BOLD).shift(UP * 0.4),
            Text(f"${avg_error**2:.0f}k", font_size=28, color=RED).shift(DOWN * 0.3)
        ).shift(DOWN * 0.5)
        
        self.play(
            Transform(avg_label, overall_loss_box),
            FadeOut(title)
        )
        self.wait()
        
        self.play(FadeOut(avg_label))
    
    def show_performance_scenarios(self):
        """Show what happens when predictions improve vs stay poor"""
        title = Text("What Does This Mean?", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title))
        
        # Scenario 1: Improving model (low loss)
        good_scenario = VGroup(
            Text("Most Predictions Accurate", font_size=24, color=GREEN, weight=BOLD),
            self.create_loss_bar(0.3, GREEN, "Low Loss"),
            Arrow(UP * 0.5, DOWN * 0.5, color=GREEN, stroke_width=6),
            Text("Model Improving! ✓", font_size=22, color=GREEN)
        ).arrange(DOWN, buff=0.4).shift(LEFT * 3.5)
        
        # Scenario 2: Poor model (high loss)
        poor_scenario = VGroup(
            Text("Predictions Scattered", font_size=24, color=RED, weight=BOLD),
            self.create_loss_bar(0.8, RED, "High Loss"),
            Arrow(UP * 0.5, DOWN * 0.5, color=RED, stroke_width=6),
            Text("Needs Adjustment ✗", font_size=22, color=RED)
        ).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5)
        
        self.play(FadeIn(good_scenario, shift=RIGHT))
        self.wait()
        self.play(FadeIn(poor_scenario, shift=LEFT))
        self.wait(2)
        
        # Animate improvement - show loss dropping
        improvement_text = Text("As Training Progresses...", font_size=28, color=YELLOW)
        improvement_text.to_edge(DOWN, buff=0.5)
        self.play(Write(improvement_text))
        
        # Animate the good scenario bar shrinking even more
        small_bar = self.create_loss_bar(0.15, GREEN, "Lower Loss")
        small_bar.move_to(good_scenario[1].get_center())
        
        self.play(Transform(good_scenario[1], small_bar))
        self.wait()
        
        self.play(FadeOut(VGroup(title, good_scenario, poor_scenario, improvement_text)))
    
    def show_single_signal_concept(self):
        """Show how loss provides a single reliable signal"""
        title = Text("One Reliable Signal", font_size=44, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Show multiple scattered errors
        scattered_errors = VGroup()
        for i in range(15):
            error_dot = Dot(color=RED, radius=0.08)
            angle = i * 2 * PI / 15
            radius = 2 + np.random.random() * 0.5
            error_dot.move_to([radius * np.cos(angle), radius * np.sin(angle), 0])
            scattered_errors.add(error_dot)
        
        scattered_label = Text("Many Individual Errors", font_size=24, color=RED)
        scattered_label.next_to(scattered_errors, DOWN, buff=0.8)
        
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in scattered_errors], lag_ratio=0.05))
        self.play(Write(scattered_label))
        self.wait()
        
        # Converge to single signal
        center_signal = VGroup(
            Circle(radius=0.8, color=YELLOW, fill_opacity=0.8, stroke_width=4),
            Text("Overall\nLoss", font_size=24, color=BLACK, weight=BOLD)
        )
        
        self.play(
            *[dot.animate.move_to(ORIGIN) for dot in scattered_errors],
            FadeOut(scattered_label),
            run_time=1.5
        )
        self.play(
            FadeOut(scattered_errors),
            FadeIn(center_signal, scale=0.5)
        )
        self.wait()
        
        # Show what it guides
        arrow = Arrow(UP * 0.5, DOWN * 1.5, color=YELLOW, stroke_width=8)
        arrow.next_to(center_signal, DOWN, buff=0.3)
        
        guides_text = Text(
            "Guides Weight Updates\n& Learning",
            font_size=28,
            color=GREEN,
            weight=BOLD
        )
        guides_text.next_to(arrow, DOWN, buff=0.3)
        
        self.play(GrowArrow(arrow))
        self.play(Write(guides_text))
        self.wait()
        
        # Final summary
        summary = VGroup(
            Text("Loss summarizes total error", font_size=24, color=WHITE),
            Text("↓", font_size=36, color=YELLOW),
            Text("Network adjusts weights", font_size=24, color=WHITE),
            Text("↓", font_size=36, color=YELLOW),
            Text("Better predictions next time", font_size=24, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.2)
        
        self.play(
            FadeOut(VGroup(title, center_signal, arrow, guides_text))
        )
        
        self.play(LaggedStart(*[FadeIn(item, shift=UP) for item in summary], lag_ratio=0.3))
        self.wait(2)
        
        self.play(FadeOut(summary))
    
    def create_small_house(self):
        """Helper function to create a small house icon"""
        house = VGroup(
            Polygon([-0.3, 0, 0], [0.3, 0, 0], [0, 0.4, 0], 
                   color=BLUE, fill_opacity=0.7, stroke_width=2),
            Rectangle(width=0.6, height=0.5, color=BLUE, fill_opacity=0.7, stroke_width=2)
            .shift(DOWN * 0.25)
        )
        return house
    
    def create_loss_bar(self, height_ratio, color, label_text):
        """Helper function to create a loss bar visualization"""
        bar_group = VGroup(
            Rectangle(width=2, height=height_ratio * 3, color=color, fill_opacity=0.7),
            Text(label_text, font_size=18, color=color, weight=BOLD)
        )
        bar_group[1].next_to(bar_group[0], DOWN, buff=0.2)
        return bar_group

class LossFunctionTypes(Scene):
    def construct(self):
        # Part 1: Introduce multiple loss functions
        self.introduce_multiple_loss_functions()
        self.wait()
        
        # Part 2: MSE for regression
        self.show_mse_regression()
        self.wait()
        
        # Part 3: Why squaring matters
        self.show_squaring_effects()
        self.wait()
        
        # Part 4: MSE example with two houses
        self.show_mse_example()
        self.wait()
        
        # Part 5: Cross-entropy for classification
        self.show_cross_entropy()
        self.wait()
        
        # Part 6: Final takeaway
        self.show_final_message()
        self.wait()
    
    def introduce_multiple_loss_functions(self):
        """Introduce that different problems need different loss functions"""
        title = Text("Different Problems, Different Loss Functions", 
                    font_size=38, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Show problem types branching
        center_text = Text("Loss Functions", font_size=32, color=BLUE, weight=BOLD).shift(UP * 0.8)
        
        # Two branches
        regression_branch = VGroup(
            Text("Regression", font_size=28, color=ORANGE, weight=BOLD),
            Text("(Predicting Numbers)", font_size=18, color=ORANGE)
        ).arrange(DOWN, buff=0.2).shift(LEFT * 3.5 + DOWN * 1)
        
        classification_branch = VGroup(
            Text("Classification", font_size=28, color=GREEN, weight=BOLD),
            Text("(Predicting Categories)", font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.2).shift(RIGHT * 3.5 + DOWN * 1)
        
        # Arrows
        left_arrow = Arrow(UP * 0.5, LEFT * 2 + DOWN * 0.5, color=ORANGE, stroke_width=4)
        right_arrow = Arrow(UP * 0.5, RIGHT * 2 + DOWN * 0.5, color=GREEN, stroke_width=4)
        
        self.play(Write(center_text))
        self.wait(4)
        self.play(GrowArrow(left_arrow), GrowArrow(right_arrow))
        self.play(FadeIn(regression_branch, shift=RIGHT))
        self.wait()
        self.play(FadeIn(classification_branch, shift=LEFT))
        self.wait(1)
        
        self.play(FadeOut(VGroup(title, center_text, left_arrow, right_arrow, 
                                regression_branch, classification_branch)))
    
    def show_mse_regression(self):
        """Show MSE for regression problems"""
        title = Text("Mean Squared Error (MSE)", font_size=40, color=ORANGE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Show the MSE formula in stages
        formula_box = VGroup(
            RoundedRectangle(width=10, height=2, corner_radius=0.2, 
                        color=ORANGE, stroke_width=3, fill_opacity=0.1)
        )
        formula_box.move_to(ORIGIN)

        self.play(Create(formula_box))

        # Stage 1: Difference (y_pred - y_actual)
        formula_stage1 = MathTex(
            r"(y_{\text{pred}} - y_{\text{actual}})",
            font_size=44,
            color=YELLOW
        )
        formula_stage1.move_to(formula_box.get_center())
        self.play(Write(formula_stage1))
        self.wait()

        # Stage 2: Squaring
        formula_stage2 = MathTex(
            r"(y_{\text{pred}} - y_{\text{actual}})",
            r"^2",
            font_size=44
        )
        formula_stage2[0].set_color(YELLOW)
        formula_stage2[1].set_color(ORANGE)
        formula_stage2.move_to(formula_box.get_center())
        self.play(Transform(formula_stage1, formula_stage2))
        self.wait()

        # Stage 3: Taking average (full formula)
        formula = MathTex(
            r"\text{MSE} = ",
            r"\frac{1}{n}",
            r"\sum_{i=1}^{n}",
            r"(y_{\text{pred}} - y_{\text{actual}})^2",
            font_size=44,
            color=WHITE
        )
        formula[1].set_color(GREEN)  # Highlight the averaging part
        formula.move_to(formula_box.get_center())
        self.play(Transform(formula_stage1, formula))
        self.wait()
        
        self.play(FadeOut(VGroup(title, formula_box, formula_stage1)))
    
    def show_squaring_effects(self):
        """Show why squaring is important"""
        title = Text("Why Squaring Matters", font_size=40, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Effect 1: Makes errors positive
        effect1_title = Text("1. Makes All Errors Positive", 
                           font_size=28, color=GREEN, weight=BOLD)
        effect1_title.shift(UP * 1.5)
        self.play(Write(effect1_title))
        
        # Show positive and negative errors
        pos_error = MathTex(r"+20^2 = ", r"400", font_size=36, color=GREEN)
        pos_error.shift(LEFT * 2 + UP * 0.3)
        
        neg_error = MathTex(r"(-20)^2 = ", r"400", font_size=36, color=GREEN)
        neg_error.shift(RIGHT * 2 + UP * 0.3)
        
        self.play(Write(pos_error))
        self.play(Write(neg_error))
        
        no_cancel = Text("Errors don't cancel out!", font_size=22, color=YELLOW, slant=ITALIC)
        no_cancel.shift(UP * 0.3 + DOWN * 0.8)
        self.play(FadeIn(no_cancel, scale=0.8))
        self.wait(0.5)
        
        self.play(FadeOut(VGroup(effect1_title, pos_error, neg_error, no_cancel)))
        
        # Effect 2: Punishes large errors
        effect2_title = Text("2. Punishes Large Errors More", 
                           font_size=28, color=RED, weight=BOLD)
        effect2_title.shift(UP * 1.8)
        self.play(Write(effect2_title))
        
        # Comparison of small vs large errors
        comparison = VGroup(
            VGroup(
                Text("Small Error", font_size=24, color=GREEN),
                MathTex(r"5^2 = 25", font_size=32, color=GREEN),
                Rectangle(width=0.5, height=0.5, color=GREEN, fill_opacity=0.7)
            ).arrange(DOWN, buff=0.3),
            
            VGroup(
                Text("Large Error", font_size=24, color=RED),
                MathTex(r"20^2 = 400", font_size=32, color=RED),
                Rectangle(width=2, height=2, color=RED, fill_opacity=0.7)
            ).arrange(DOWN, buff=0.3)
        ).arrange(RIGHT, buff=2).shift(DOWN * 0.3)
        
        self.play(FadeIn(comparison[0], shift=RIGHT))
        self.wait(0.5)
        self.play(FadeIn(comparison[1], shift=LEFT))
        self.wait(0.5)
        
        self.play(FadeOut(VGroup(title, effect2_title, comparison)))
    
    def show_mse_example(self):
        """Show concrete MSE example with two houses"""
        title = Text("MSE Example: Two Houses", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # House 1
        house1 = VGroup(
            self.create_house(),
            Text("House 1", font_size=20, color=WHITE, weight=BOLD),
            Text("Predicted: $280k", font_size=18, color=ORANGE),
            Text("Actual: $300k", font_size=18, color=GREEN),
            Text("Error: -$20k", font_size=18, color=RED)
        ).arrange(DOWN, buff=0.2).shift(LEFT * 4 + UP * 0.5)
        
        # House 2
        house2 = VGroup(
            self.create_house(),
            Text("House 2", font_size=20, color=WHITE, weight=BOLD),
            Text("Predicted: $290k", font_size=18, color=ORANGE),
            Text("Actual: $300k", font_size=18, color=GREEN),
            Text("Error: -$10k", font_size=18, color=RED)
        ).arrange(DOWN, buff=0.2).shift(RIGHT * 4 + UP * 0.5)
        
        self.play(FadeIn(house1, shift=RIGHT))
        self.wait()
        self.play(FadeIn(house2, shift=LEFT))
        self.wait()
        
        # Calculate MSE
        calculation = VGroup(
            Text("Calculating MSE:", font_size=24, color=YELLOW, weight=BOLD),
            MathTex(r"\text{MSE} = \frac{1}{2}[(-20)^2 + (-10)^2]", font_size=32),
            MathTex(r"= \frac{1}{2}[400 + 100]", font_size=32),
            MathTex(r"= \frac{500}{2} = ", r"250", font_size=32)
        ).arrange(DOWN, buff=0.4).shift(DOWN * 1.8)
        
        self.play(Write(calculation[0]))
        self.play(Write(calculation[1]))
        self.play(Write(calculation[2]))
        self.play(Write(calculation[3]))
        
        self.play(FadeOut(VGroup(title, house1, house2, calculation)))
    
    def show_cross_entropy(self):
        """Show cross-entropy for classification"""
        title = Text("Cross-Entropy Loss", font_size=40, color=GREEN, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        subtitle = Text("For Classification Problems", font_size=24, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle, shift=UP))
        
        # Example: Cat vs Dog
        example = Text("Example: Cat or Dog?", font_size=26, color=BLUE)
        example.shift(UP * 1.5)
        self.play(Write(example))
        self.wait()
        
        # Show image and predictions
        image_box = Square(side_length=1.5, color=WHITE, stroke_width=3, fill_opacity=0.1)
        image_box.shift(LEFT * 4)
        
        dog_svg = SVGMobject("dog.svg")
        dog_svg.scale_to_fit_width(1.2)  # Adjust size to fit the box
        dog_svg.move_to(image_box.get_center())
        
        actual_label = Text("Actual: Dog", font_size=20, color=GREEN, weight=BOLD)
        actual_label.next_to(image_box, DOWN, buff=0.3)
        
        self.play(Create(image_box))
        self.play(FadeIn(dog_svg, scale=0.5))
        self.play(Write(actual_label))
        self.wait(4)
        
        # Network predictions (probabilities)
        predictions = VGroup(
            Text("Network Predicts:", font_size=24, color=WHITE, weight=BOLD),
            VGroup(
                self.create_probability_bar(0.9, "Cat", RED),
                self.create_probability_bar(0.1, "Dog", GREEN)
            ).arrange(DOWN, buff=0.4)
        ).arrange(DOWN, buff=0.5).shift(RIGHT * 2.5)
        
        self.play(FadeIn(predictions, shift=LEFT))
        self.wait(8)
        
        # Show the problem
        problem = VGroup(
            Text("High confidence", font_size=20, color=RED),
            Text("in WRONG  direction!", font_size=20, color=RED, weight=BOLD)
        ).arrange(DOWN, buff=0.1).next_to(predictions, DOWN, buff=0.8)
        
        self.play(Write(problem))
        self.wait()
    
        
        self.play(FadeOut(VGroup(title, subtitle, example, image_box, dog_svg, 
                                actual_label, predictions, problem)))
    
    def show_final_message(self):
        """Show the key takeaway message"""
        title = Text("The Key Takeaway", font_size=44, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Main message box
        message_box = VGroup(
            RoundedRectangle(width=11, height=4, corner_radius=0.3, 
                           color=BLUE, stroke_width=4, fill_opacity=0.2)
        )
        
        message = VGroup(
            Text("Every Loss Function Has One Job:", 
                font_size=28, color=WHITE, weight=BOLD),
            Text("Give the network feedback on", font_size=24, color=WHITE),
            Text("how far its prediction was from the truth", 
                font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.4)
        
        message_box.move_to(ORIGIN + UP * 0.3)
        message.move_to(message_box.get_center())
        
        self.play(Create(message_box))
        self.play(LaggedStart(*[FadeIn(line, shift=UP) for line in message], lag_ratio=0.3))
        self.wait()
        
        # No need to memorize
        note = Text("You don't need to memorize the formulas", 
                   font_size=22, color=GRAY, slant=ITALIC)
        note.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP))
        self.wait(9)
        
        self.play(FadeOut(VGroup(title, message_box, message, note)))
    
    def create_house(self):
        """Helper to create house icon"""
        house = VGroup(
            Polygon([-0.4, 0, 0], [0.4, 0, 0], [0, 0.5, 0], 
                   color=BLUE, fill_opacity=0.7, stroke_width=2),
            Rectangle(width=0.8, height=0.6, color=BLUE, fill_opacity=0.7, stroke_width=2)
            .shift(DOWN * 0.3)
        )
        return house
    
    def create_probability_bar(self, probability, label, color):
        """Helper to create probability visualization"""
        bar_width = probability * 4
        
        bar_group = VGroup(
            Rectangle(width=4, height=0.4, color=GRAY, fill_opacity=0.2, stroke_width=2),
            Rectangle(width=bar_width, height=0.4, color=color, fill_opacity=0.7, stroke_width=0)
            .align_to(ORIGIN, LEFT).shift(LEFT * 2),
            Text(f"{label}: {probability:.1f}", font_size=18, color=color, weight=BOLD)
            .shift(LEFT * 2.8)
        )
        
        return bar_group

class LossReductionTraining(Scene):
    def construct(self):
        # Part 1: What happens after calculating loss
        self.introduce_next_step()
        self.wait()
        
        # Part 2: Loss as feedback signal
        self.show_feedback_signal()
        self.wait()
        
        # Part 3: How it works in practice - iterative improvement
        self.show_iterative_improvement()
        self.wait()
        
        # Part 4: Training progress with loss curve
        self.show_training_progress()
        self.wait()
        
        # Part 5: Final message - purpose of training
        self.show_training_purpose()
        self.wait()
    
    def introduce_next_step(self):
        """Introduce what happens after calculating loss"""
        title = Text("After Calculating Loss...", font_size=40, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Show loss value
        loss_display = VGroup(
            RoundedRectangle(width=4, height=1.5, corner_radius=0.2, 
                           color=RED, stroke_width=3, fill_opacity=0.2),
            Text("Loss = 400", font_size=32, color=RED, weight=BOLD)
        ).shift(UP * 1)
        loss_display[1].move_to(loss_display[0].get_center())
        
        self.play(FadeIn(loss_display, scale=0.8))
        self.wait()
        
        # Network knows it's wrong
        knows = Text("Network knows it's wrong", font_size=26, color=WHITE)
        knows.next_to(loss_display, DOWN, buff=0.5)
        self.play(Write(knows))
        self.wait(3)
        
        # The real goal
        goal = VGroup(
            Text("The Real Goal:", font_size=30, color=GREEN, weight=BOLD),
            Text("Adjust weights & biases", font_size=26, color=GREEN),
            Text("to REDUCE the loss", font_size=26, color=GREEN, weight=BOLD)
        ).arrange(DOWN, buff=0.3).shift(DOWN * 1.7)
        
        self.play(LaggedStart(*[FadeIn(line, shift=UP) for line in goal], lag_ratio=0.3))
        self.wait(8)
        
        self.play(FadeOut(VGroup(title, loss_display, knows, goal)))
    
    def show_feedback_signal(self):
        """Show loss as a feedback/performance signal"""
        title = Text("Loss as a Feedback Signal", font_size=38, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create a gauge/meter visualization
        # High loss scenario
        high_scenario = VGroup(
            Text("High Loss", font_size=28, color=RED, weight=BOLD),
            self.create_gauge(0.8, RED),
            Text("Predictions far from truth", font_size=20, color=RED)
        ).arrange(DOWN, buff=0.4).shift(LEFT * 3.5 + DOWN * 0.5)
        
        # Low loss scenario
        low_scenario = VGroup(
            Text("Low Loss", font_size=28, color=GREEN, weight=BOLD),
            self.create_gauge(0.2, GREEN),
            Text("Getting closer to target", font_size=20, color=GREEN)
        ).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5 + DOWN * 0.5)
        
        self.play(FadeIn(high_scenario, shift=RIGHT))
        self.wait(4)
        self.play(FadeIn(low_scenario, shift=LEFT))
        self.wait()
        
        # Arrow showing direction
        improvement_arrow = Arrow(LEFT * 2, RIGHT * 2, color=YELLOW, 
                                 stroke_width=8, buff=0.5)
        improvement_arrow.shift(DOWN * 2.5)
        
        improve_label = Text("Training Direction", font_size=24, color=YELLOW, weight=BOLD)
        improve_label.next_to(improvement_arrow, UP, buff=0.2)
        
        self.play(GrowArrow(improvement_arrow))
        self.play(Write(improve_label))
        self.wait()
        
        self.play(FadeOut(VGroup(title, high_scenario, low_scenario, 
                                improvement_arrow, improve_label)))
    
    def show_iterative_improvement(self):
        """Show how network improves through iterations"""
        title = Text("How It Works in Practice", font_size=38, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # House reference
        house_icon = self.create_house().scale(1.2).shift(LEFT * 5 + UP * 1.5)
        actual_price = Text("Actual: $300k", font_size=22, color=GREEN, weight=BOLD)
        actual_price.next_to(house_icon, DOWN, buff=0.3)
        
        self.play(FadeIn(house_icon, scale=0.5))
        self.play(Write(actual_price))
        self.wait()
        
        # Iterations
        iterations = [
            ("$280k", 400, RED),
            ("$290k", 100, ORANGE),
            ("$298k", 4, YELLOW),
            ("$300k", 0, GREEN)
        ]
        
        iteration_display = VGroup().shift(RIGHT * 1.5)
        
        for i, (prediction, loss, color) in enumerate(iterations):
            # Create iteration box
            iter_box = VGroup(
                Text(f"Iteration {i+1}", font_size=20, color=WHITE, weight=BOLD),
                Text(f"Predicts: {prediction}", font_size=24, color=color),
                Text(f"Loss: {loss}", font_size=20, color=color),
                Arrow(UP * 0.3, DOWN * 0.3, color=YELLOW, stroke_width=4) if i < 3 else VGroup()
            ).arrange(DOWN, buff=0.2)
            
            position = UP * (2 - i * 1.7)
            iter_box.shift(position)
            
            # Animate appearance
            self.play(FadeIn(iter_box[:3], shift=UP), run_time=0.7)

            if (i == 0):
                self.wait(9)
            else:
                self.wait(2) 
            
            # Show parameter adjustment (except for last iteration)
            if i < 3:
                adjust_text = Text("Adjust parameters →", font_size=16, 
                                  color=YELLOW, slant=ITALIC)
                adjust_text.next_to(iter_box, RIGHT, buff=0.5)
                self.play(FadeIn(adjust_text, shift=LEFT), run_time=0.8)
                self.play(FadeOut(adjust_text), run_time=0.3)
            
            iteration_display.add(iter_box)
        
        # Highlight the improvement
        improvement_bracket = BraceBetweenPoints(
            iteration_display[0].get_right() + RIGHT * 0.3,
            iteration_display[-1].get_right() + RIGHT * 0.3,
            direction=RIGHT,
            color=GREEN
        )
        
        improvement_label = Text("Gradually\nImproving!", font_size=20, 
                               color=GREEN, weight=BOLD)
        improvement_label.next_to(improvement_bracket, RIGHT, buff=0.3)
        
        self.play(GrowFromCenter(improvement_bracket))
        self.play(Write(improvement_label))
        self.wait()
        
        self.play(FadeOut(VGroup(title, house_icon, actual_price, 
                                iteration_display, improvement_bracket, improvement_label)))
    
    def show_training_progress(self):
        """Show training progress with loss curve"""
        title = Text("Training Progress Over Time", font_size=38, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create axes for loss curve
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 500, 100],
            x_length=9,
            y_length=5,
            axis_config={"color": GRAY, "include_tip": True},
            x_axis_config={"numbers_to_include": [0, 20, 40, 60, 80, 100]},
            y_axis_config={"numbers_to_include": [0, 100, 200, 300, 400, 500]}
        ).shift(DOWN * 0.5)
        
        x_label = Text("Training Iterations", font_size=20).next_to(axes.x_axis, DOWN)
        y_label = Text("Loss", font_size=20).next_to(axes.y_axis, LEFT).rotate(90 * DEGREES)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait()
        
        # Create loss curve (exponential decay)
        def loss_func(x):
            return 450 * np.exp(-0.03 * x) + 10
        
        loss_curve = axes.plot(loss_func, x_range=[0, 100], color=RED, stroke_width=4)
        
        # Animate the curve being drawn
        self.play(Create(loss_curve), run_time=3, rate_func=linear)
        self.wait()
        
        # Add labels at key points
        start_dot = Dot(axes.c2p(0, loss_func(0)), color=RED, radius=0.1)
        start_label = Text("High Loss\n(Start)", font_size=18, color=RED)
        start_label.next_to(start_dot, UP + RIGHT, buff=0.2)
        
        end_dot = Dot(axes.c2p(100, loss_func(100)), color=GREEN, radius=0.1)
        end_label = Text("Low Loss\n(Trained)", font_size=18, color=GREEN)
        end_label.next_to(end_dot, RIGHT, buff=0.2)
        
        self.play(FadeIn(start_dot), Write(start_label))
        self.wait()
        self.play(FadeIn(end_dot), Write(end_label))
        self.wait()
        
        # Show house price predictions along the curve
        checkpoints = [(10, "$280k"), (30, "$290k"), (60, "$298k"), (90, "$300k")]
        
        for x, price in checkpoints:
            y = loss_func(x)
            point = Dot(axes.c2p(x, y), color=YELLOW, radius=0.08)
            price_label = Text(price, font_size=14, color=YELLOW, weight=BOLD)
            price_label.next_to(point, DOWN, buff=0.15)
            
            self.play(FadeIn(point), Write(price_label), run_time=0.5)
        
        self.wait()
        
        # Student analogy
        analogy = Text(
            "Like a student improving with each test!",
            font_size=24,
            color=YELLOW,
            slant=ITALIC
        ).to_edge(UP, buff=3)
        
        self.play(Write(analogy))
        self.wait()
        
        # Fade out remaining dots and labels
        self.play(FadeOut(*[mob for mob in self.mobjects]))
    
    def show_training_purpose(self):
        """Show that reducing loss is the entire purpose"""
        title = Text("The Purpose of Training", font_size=44, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Show the result
        result_box = VGroup(
            RoundedRectangle(width=8, height=2, corner_radius=0.3, 
                           color=BLUE, stroke_width=4, fill_opacity=0.2),
            VGroup(
                Text("Lower Loss =", font_size=28, color=WHITE),
                Text("Smarter & More Accurate Model", font_size=28, 
                    color=GREEN, weight=BOLD)
            ).arrange(DOWN, buff=0.3)
        )
        result_box[1].move_to(result_box[0].get_center())
        
        self.play(FadeIn(result_box, scale=0.9))
        self.wait()
        
        self.play(FadeOut(VGroup(title, result_box)))
    
    def create_house(self):
        """Helper to create house icon"""
        house = VGroup(
            Polygon([-0.4, 0, 0], [0.4, 0, 0], [0, 0.5, 0], 
                   color=BLUE, fill_opacity=0.7, stroke_width=2),
            Rectangle(width=0.8, height=0.6, color=BLUE, fill_opacity=0.7, stroke_width=2)
            .shift(DOWN * 0.3)
        )
        return house
    
    def create_gauge(self, fill_ratio, color):
        """Helper to create a gauge/meter visualization"""
        # Background arc
        bg_arc = Arc(
            radius=1.2,
            start_angle=PI,
            angle=PI,
            color=GRAY,
            stroke_width=8,
            stroke_opacity=0.3
        )
        
        # Filled arc
        filled_arc = Arc(
            radius=1.2,
            start_angle=PI,
            angle=PI * fill_ratio,
            color=color,
            stroke_width=8
        )
        
        # Needle
        needle_angle = PI - (PI * fill_ratio)
        needle_end = 1.2 * np.array([np.cos(needle_angle), np.sin(needle_angle), 0])
        needle = Arrow(
            ORIGIN, needle_end,
            color=color,
            stroke_width=3,
            buff=0,
            max_tip_length_to_length_ratio=0.2
        )
        
        # Center dot
        center_dot = Dot(ORIGIN, radius=0.1, color=WHITE)
        
        gauge = VGroup(bg_arc, filled_arc, needle, center_dot)
        
        return gauge

class GolfAnalogy(Scene):
    def construct(self):
        # Part 1: Introduce golf analogy
        self.introduce_golf_analogy()
        self.wait()
        
        # Part 2: Show multiple putt attempts
        self.show_putt_attempts()
        self.wait()
        
        # Part 3: Parallel to neural network
        self.show_network_parallel()
        self.wait()
        
        # Part 4: Side by side comparison
        self.show_side_by_side_comparison()
        self.wait()
        
        # Part 5: Final message - feedback loop
        self.show_feedback_loop()
        self.wait()
    
    def introduce_golf_analogy(self):
        """Introduce the golf putting analogy"""
        title = Text("Real-World Analogy: Golf", font_size=40, color=GREEN, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        subtitle = Text("Learning Through  Trial and Adjustment", 
                       font_size=22, color=WHITE, slant=ITALIC)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait()
        
        # Create golf scene
        grass = Rectangle(width=14, height=6, color=GREEN_D, fill_opacity=0.3, stroke_width=0)
        grass.shift(DOWN * 0.7)
        self.play(FadeIn(grass))
        
        # Golf hole (target)
        hole = Circle(radius=0.2, color=BLACK, fill_opacity=1, stroke_width=2, stroke_color=WHITE)
        hole.shift(RIGHT * 4 + UP * 0.5)
        
        hole_flag = VGroup(
            Line(ORIGIN, UP * 1, color=WHITE, stroke_width=2),
            Polygon([0, 1, 0], [0.3, 0.9, 0], [0, 0.8, 0], 
                   color=RED, fill_opacity=1, stroke_width=0)
        ).scale(0.6)
        hole_flag.move_to(hole.get_center())
        
        self.play(GrowFromCenter(hole))
        self.play(FadeIn(hole_flag, shift=DOWN))
        
        target_label = Text("Target", font_size=18, color=YELLOW, weight=BOLD)
        target_label.next_to(hole, UP, buff=0.5)
        self.play(Write(target_label))
        self.wait()
        
        self.golf_scene = VGroup(grass, hole, hole_flag, target_label)
        self.hole_position = hole.get_center()
        
        self.play(FadeOut(title), FadeOut(subtitle))
    
    def show_putt_attempts(self):
        """Show golfer making multiple attempts"""
        
        # Starting position for golf ball
        start_pos = LEFT * 5 + UP * 0.5
        
        # Golf ball
        ball = Circle(radius=0.12, color=WHITE, fill_opacity=1, stroke_color=GRAY, stroke_width=2)
        ball.move_to(start_pos)
        
        # Attempts data: (end_x, end_y, distance_from_hole, color, label)
        attempts = [
            (5, 0.5, "Too Far", RED, "Attempt 1"),
            (3, 0.5, "Too Short", ORANGE, "Attempt 2"),
            (4.2, 0.5, "Very Close", YELLOW, "Attempt 3"),
            (4, 0.5, "Perfect!", GREEN, "Attempt 4")
        ]
        
        attempt_markers = VGroup()
        
        for i, (end_x, end_y, description, color, label) in enumerate(attempts):
            # Reset ball to start
            ball_copy = ball.copy()
            self.add(ball_copy)
            
            end_pos = np.array([end_x, end_y, 0])
            
            # Animate ball rolling
            self.play(ball_copy.animate.move_to(end_pos), 
                     rate_func=rate_functions.ease_out_cubic, run_time=1.2)
            
            # Calculate distance from hole
            distance = np.linalg.norm(end_pos - self.hole_position)
            
            # Show distance measurement
            if i < 3:  # Don't show distance line for perfect shot
                distance_line = DashedLine(
                    end_pos, self.hole_position,
                    color=color, stroke_width=3
                )
                self.play(Create(distance_line), run_time=0.5)
                
                # Distance label
                mid_point = (end_pos + self.hole_position) / 2
                distance_label = VGroup(
                    Text(description, font_size=16, color=color, weight=BOLD),
                    Text("(Loss)", font_size=14, color=color, slant=ITALIC)
                ).arrange(DOWN, buff=0.05)
                distance_label.next_to(self.hole_position, DOWN, buff=0.5)
                
                self.play(Write(distance_label), run_time=0.5)
                self.wait()
                self.play(FadeOut(distance_label))
                
                attempt_markers.add(ball_copy, distance_line)
            else:
                # Perfect shot - celebration
                self.play(ball_copy.animate.move_to(self.hole_position), run_time=0.5)
                
                success_text = Text("Perfect! ✓", font_size=20, color=GREEN, weight=BOLD)
                success_text.next_to(self.hole_position, DOWN, buff=0.5)
                self.play(Write(success_text))
                
                # Show "Loss = 0"
                loss_zero = Text("Loss = 0", font_size=18, color=GREEN, weight=BOLD)
                loss_zero.next_to(success_text, DOWN, buff=0.2)
                self.play(Write(loss_zero))
                
                attempt_markers.add(ball_copy, success_text, loss_zero)
            
            # Adjustment text
            if i < 3:
                adjust_text = Text("Adjust aim & strength →", 
                                  font_size=16, color=YELLOW, slant=ITALIC)
                adjust_text.move_to(start_pos + DOWN * 1)
                self.play(FadeIn(adjust_text, shift=RIGHT), run_time=0.5)
                self.play(FadeOut(adjust_text), run_time=0.3)
        
        self.wait()
        
        # Show learning progression
        learning_text = Text("Getting Better With Practice!", 
                           font_size=24, color=GREEN, weight=BOLD)
        learning_text.to_edge(DOWN, buff=0.5)
        self.play(Write(learning_text))
        self.wait(8)
        
        self.play(FadeOut(VGroup(attempt_markers, learning_text)))
        self.play(FadeOut(self.golf_scene))
    
    def show_network_parallel(self):
        """Show how this parallels neural network learning"""
        title = Text("Just Like a Neural Network!", font_size=40, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Split screen concept
        divider = DashedLine(UP * 3, DOWN * 3, color=GRAY, stroke_width=2)
        
        self.play(Create(divider))
        
        # Left side: Golfer
        golfer_side = VGroup(
            Text("Golfer", font_size=28, color=GREEN, weight=BOLD),
            Text("🏌️", font_size=60),
            VGroup(
                Text("• Observes distance from hole", font_size=16, color=WHITE),
                Text("• Adjusts aim & strength", font_size=16, color=WHITE),
                Text("• Tries again", font_size=16, color=WHITE),
                Text("• Gets closer each time", font_size=16, color=WHITE)
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        ).arrange(DOWN, buff=0.4).shift(LEFT * 3.5)
        
        # Right side: Neural Network
        network_side = VGroup(
            Text("Neural Network", font_size=28, color=BLUE, weight=BOLD),
            Text("🧠", font_size=60),
            VGroup(
                Text("• Measures loss (error)", font_size=16, color=WHITE),
                Text("• Adjusts weights & biases", font_size=16, color=WHITE),
                Text("• Makes new prediction", font_size=16, color=WHITE),
                Text("• Gets more accurate", font_size=16, color=WHITE)
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        ).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5)
        
        self.play(FadeIn(golfer_side[0:2], shift=RIGHT))
        self.wait()
        self.play(FadeIn(network_side[0:2], shift=LEFT))
        self.wait()
        
        # Show steps in parallel
        for i in range(4):
            self.play(
                FadeIn(golfer_side[2][i], shift=RIGHT),
                FadeIn(network_side[2][i], shift=LEFT),
                run_time=0.7
            )
            self.wait()
        
        # Highlight similarity
        similarity = Text("Same Process!", font_size=32, color=YELLOW, weight=BOLD)
        similarity.next_to(divider, DOWN, buff=0.5)
        
        arrow_left = Arrow(similarity.get_left() + LEFT * 0.5, 
                          golfer_side.get_bottom() + DOWN * 0.3,
                          color=YELLOW, stroke_width=4)
        arrow_right = Arrow(similarity.get_right() + RIGHT * 0.5,
                           network_side.get_bottom() + DOWN * 0.3,
                           color=YELLOW, stroke_width=4)
        
        self.play(Write(similarity))
        self.play(GrowArrow(arrow_left), GrowArrow(arrow_right))
        self.wait()
        
        self.play(FadeOut(VGroup(title, divider, golfer_side, network_side, 
                                similarity, arrow_left, arrow_right)))
    
    def show_side_by_side_comparison(self):
        """Show visual side-by-side of attempts getting better"""
        title = Text("Each Pass Gets Better", font_size=38, color=BLUE, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create mini golf scenes showing progression
        attempts_visual = VGroup()
        
        for i in range(4):
            mini_scene = self.create_mini_attempt_scene(i)
            attempts_visual.add(mini_scene)
        
        attempts_visual.arrange(RIGHT, buff=0.8).shift(UP * 0.5)
        
        # Animate each attempt appearing
        for i, attempt in enumerate(attempts_visual):
            self.play(FadeIn(attempt, scale=0.8), run_time=0.6)
            self.wait()
        
        # Add arrows showing progression
        arrows = VGroup()
        for i in range(3):
            arrow = Arrow(
                attempts_visual[i].get_right() + RIGHT * 0.1,
                attempts_visual[i+1].get_left() + LEFT * 0.1,
                color=YELLOW, stroke_width=4, buff=0.1
            )
            arrows.add(arrow)
        
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.3))
        self.wait()
        
        # Bottom comparison with network
        comparison_text = Text(
            "Network's predictions align with reality over time",
            font_size=24, color=GREEN, weight=BOLD
        ).to_edge(DOWN, buff=0.8)
        
        self.play(Write(comparison_text))
        self.wait()
        
        self.play(FadeOut(VGroup(title, attempts_visual, arrows, comparison_text)))
    
    def show_feedback_loop(self):
        """Show the feedback loop process"""
        title = Text("Built on Feedback", font_size=44, color=YELLOW, weight=BOLD)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create circular feedback loop
        steps = [
            ("Try", BLUE),
            ("Measure", RED),
            ("Adjust", ORANGE),
            ("Improve", GREEN)
        ]
        
        # Create circle of steps
        radius = 2
        step_objects = VGroup()
        
        for i, (step_name, color) in enumerate(steps):
            angle = PI/2 - i * (2 * PI / len(steps))
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            step_box = VGroup(
                Circle(radius=0.6, color=color, fill_opacity=0.3, stroke_width=3),
                Text(step_name, font_size=20, color=color, weight=BOLD)
            )
            step_box[1].move_to(step_box[0].get_center())
            step_box.move_to([x, y, 0])
            
            step_objects.add(step_box)
        
        # Create arrows between steps
        arrows = VGroup()
        for i in range(len(steps)):
            next_i = (i + 1) % len(steps)
            
            start = step_objects[i].get_center()
            end = step_objects[next_i].get_center()
            
            # Calculate direction for curved arrow
            direction = end - start
            direction = direction / np.linalg.norm(direction)
            
            # Offset start and end points
            arrow = CurvedArrow(
                start + direction * 0.6,
                end - direction * 0.6,
                color=YELLOW,
                stroke_width=4,
                angle=-TAU/8
            )
            arrows.add(arrow)
        
        self.play(LaggedStart(*[FadeIn(step, scale=0.5) for step in step_objects], 
                             lag_ratio=0.2))
        self.wait()
        
        self.play(LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.2))
        self.wait()
        
        # Add center text
        center_text = VGroup(
            Text("Until Loss", font_size=18, color=WHITE),
            Text("Is Minimal", font_size=18, color=WHITE, weight=BOLD)
        ).arrange(DOWN, buff=0.1)
        center_text.move_to(ORIGIN)
        
        self.play(Write(center_text))
        self.wait()
        
        self.play(FadeOut(VGroup(title, step_objects, arrows, center_text)))
    
    def create_mini_attempt_scene(self, attempt_num):
        """Helper to create mini golf attempt visualization"""
        # Small golf scene
        base = Rectangle(width=2, height=1.2, color=GREEN_D, 
                        fill_opacity=0.2, stroke_width=1, stroke_color=GREEN)
        
        # Hole
        hole = Circle(radius=0.08, color=BLACK, fill_opacity=1, stroke_width=1)
        hole.move_to(base.get_center() + RIGHT * 0.7)
        
        # Ball positions for each attempt
        ball_offsets = [
            RIGHT * 1.2,   # Too far
            RIGHT * 0.3,   # Too short
            RIGHT * 0.9,  # Close
            RIGHT * 0.7    # Perfect
        ]
        
        ball = Circle(radius=0.08, color=WHITE, fill_opacity=1, stroke_width=1)
        ball.move_to(base.get_center() + ball_offsets[attempt_num])
        
        # Distance line (except for perfect shot)
        if attempt_num < 3:
            distance_line = Line(
                ball.get_center(), hole.get_center(),
                color=RED if attempt_num == 0 else ORANGE if attempt_num == 1 else YELLOW,
                stroke_width=2
            )
        else:
            distance_line = VGroup()  # Empty for perfect shot
        
        # Label
        labels = ["Attempt 1", "Attempt 2", "Attempt 3", "Perfect!"]
        colors = [RED, ORANGE, YELLOW, GREEN]
        
        label = Text(labels[attempt_num], font_size=14, 
                    color=colors[attempt_num], weight=BOLD)
        label.next_to(base, DOWN, buff=0.2)
        
        mini_scene = VGroup(base, hole, ball, distance_line, label)
        
        return mini_scene

class LossFunctionHook(Scene):
    def construct(self):
        # Part 1: The big question (5 seconds)
        self.show_big_question()
        self.wait(0.5)
        
        # Part 2: Loss function reveal (4 seconds)
        self.reveal_loss_function()
        self.wait(0.5)
        
        # Part 3: Three key points (8 seconds)
        self.show_key_points()
        self.wait(0.5)
        
        # Part 4: Ready? Let's dive in! (5 seconds)
        self.show_call_to_action()
        self.wait()
    
    def show_big_question(self):
        """Show the big question"""
        question = VGroup(
            Text("But the BIG question...", font_size=32, color=YELLOW, slant=ITALIC),
            Text("How does the network know", font_size=38, color=WHITE),
            Text("if the guess was right or wrong?", font_size=38, color=WHITE, weight=BOLD)
        ).arrange(DOWN, buff=0.4)
        
        # Question mark animation
        question_mark = Text("?", font_size=120, color=RED, weight=BOLD)
        question_mark.next_to(question, DOWN, buff=0.5)
        
        self.play(FadeIn(question[0], shift=DOWN))
        self.play(Write(question[1]))
        self.play(Write(question[2]))
        self.play(GrowFromCenter(question_mark, scale=2))
        
        self.play(FadeOut(VGroup(question, question_mark)))
    
    def reveal_loss_function(self):
        """Reveal the loss function"""
        answer = Text("Loss Function", font_size=72, color=BLUE, weight=BOLD)
        
        self.play(
            Write(answer),
            run_time=1.0
        )
        
        self.wait(0.5)
        self.play(FadeOut(VGroup(answer)))
    
    def show_key_points(self):
        """Show three key points"""
        title = Text("In This Video:", font_size=36, color=YELLOW, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        points = VGroup(
            VGroup(
                Text("1", font_size=32, color=BLUE, weight=BOLD),
                Text("What is a loss function?", font_size=28, color=WHITE)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("2", font_size=32, color=ORANGE, weight=BOLD),
                Text("How does it measure error?", font_size=28, color=WHITE)
            ).arrange(RIGHT, buff=0.3),
            
            VGroup(
                Text("3", font_size=32, color=GREEN, weight=BOLD),
                Text("Why minimize the error?", font_size=28, color=WHITE)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT).shift(DOWN * 0.3)
        
        # Animate each point appearing
        for point in points:
            self.play(FadeIn(point, shift=RIGHT), run_time=0.8)
        
        self.wait(2.5)
        self.play(FadeOut(VGroup(title, points)))
    
    def show_call_to_action(self):
        """Show call to action"""
        ready = Text("Ready?", font_size=48, color=YELLOW, weight=BOLD)
        ready.shift(UP * 0.5)
        
        self.play(Write(ready))
        self.wait(0.5)
        
        dive_in = Text("Let's Dive In!", font_size=56, color=GREEN, weight=BOLD)
        dive_in.shift(DOWN * 0.8)
        
        self.play(
            Write(dive_in),
            run_time=1.2
        )
        
        self.wait(0.8)
        self.play(FadeOut(VGroup(ready, dive_in)))

class LossFunctionSummary(Scene):
    def construct(self):
        # Color scheme
        TITLE_COLOR = "#f39c12"  # Orange
        POINT_COLOR = "#3498db"  # Blue
        HIGHLIGHT_COLOR = "#e74c3c"  # Red
        SUCCESS_COLOR = "#2ecc71"  # Green
        
        # ===== TITLE (2s) =====
        title = Text("Key Takeaways", font_size=48, weight=BOLD, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # ===== KEY POINTS (20s) =====
        # Create all points
        point1 = VGroup(
            Text("1.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            Text("Loss function measures mistakes", font_size=28, color=WHITE)
        ).arrange(RIGHT, buff=0.3)
        
        point2 = VGroup(
            Text("2.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            Text("Compares prediction vs. actual answer", font_size=28, color=WHITE)
        ).arrange(RIGHT, buff=0.3)
        
        point3 = VGroup(
            Text("3.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            Text("Assigns a number to the error", font_size=28, color=WHITE)
        ).arrange(RIGHT, buff=0.3)
        
        point4 = VGroup(
            Text("4.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            VGroup(
                Text("Smaller loss = ", font_size=28, color=WHITE),
                Text("Better prediction", font_size=28, color=SUCCESS_COLOR, weight=BOLD)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(RIGHT, buff=0.3)
        
        point5 = VGroup(
            Text("5.", font_size=32, color=TITLE_COLOR, weight=BOLD),
            Text("Goal: Minimize the loss", font_size=28, color=HIGHLIGHT_COLOR, weight=BOLD)
        ).arrange(RIGHT, buff=0.3)
        
        # Arrange all points
        points = VGroup(point1, point2, point3, point4, point5)
        points.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        points.shift(DOWN * 0.3)
        
        # Animate each point appearing
        self.play(FadeIn(point1, shift=RIGHT), run_time=0.8)
        self.wait(3)
        
        self.play(FadeIn(point2, shift=RIGHT), run_time=0.8)
        self.wait(3)
        
        self.play(FadeIn(point3, shift=RIGHT), run_time=0.8)
        self.wait(3)
        
        self.play(FadeIn(point4, shift=RIGHT), run_time=0.8)
        self.wait(1)
        
        # Highlight "smaller loss = better prediction"
        better_pred = point4[1]
        highlight_box = SurroundingRectangle(
            better_pred, 
            color=SUCCESS_COLOR, 
            stroke_width=3, 
            buff=0.1
        )
        self.play(Create(highlight_box), run_time=0.5)
        self.wait(1.5)
        self.play(FadeOut(highlight_box), run_time=0.3)
        
        self.play(FadeIn(point5, shift=RIGHT), run_time=0.8)
        self.wait(0.8)
        
        # Highlight "Minimize the loss"
        minimize_text = point5[1]
        highlight_box2 = SurroundingRectangle(
            minimize_text, 
            color=HIGHLIGHT_COLOR, 
            stroke_width=3, 
            buff=0.1
        )
        self.play(Create(highlight_box2), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(highlight_box2), run_time=0.3)
        
        # ===== NEXT VIDEO (3s) =====
        next_section = VGroup(
            Text("Next Video:", font_size=26, color=WHITE),
            Text("How the network uses loss", font_size=24, color=POINT_COLOR),
            Text("to update its weights", font_size=24, color=POINT_COLOR)
        ).arrange(DOWN, buff=0.2)
        next_section.next_to(points, DOWN, buff=0.6)
        
        # Arrow pointing to next section
        arrow = Arrow(point5.get_bottom(), next_section.get_top(), 
                     color=POINT_COLOR, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        
        self.play(GrowArrow(arrow), run_time=0.4)
        self.play(FadeIn(next_section, shift=UP), run_time=0.6)
        self.wait(0.5)
        
        # Final emphasis: Backpropagation
        backprop = Text("BACKPROPAGATION", 
                       font_size=32, 
                       color=HIGHLIGHT_COLOR,
                       weight=BOLD)
        backprop.next_to(next_section, DOWN, buff=0.4)
        
        self.play(Write(backprop), run_time=0.8)
        self.wait(5)

        # Fade out everything on screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])


