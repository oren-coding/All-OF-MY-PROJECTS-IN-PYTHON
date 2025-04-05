import turtle
import math
import time

# Set up the window
window = turtle.Screen()
window.title("Graphing Calculator")
window.bgcolor("white")
window.setup(width=800, height=600)

# Set up the turtle
graph_turtle = turtle.Turtle()
graph_turtle.speed(0)
graph_turtle.hideturtle()

# Set up the axes with markings
def draw_axes():
    graph_turtle.penup()
    graph_turtle.goto(-400, 0)
    graph_turtle.pendown()
    graph_turtle.goto(400, 0)
    graph_turtle.penup()
    graph_turtle.goto(0, -300)
    graph_turtle.pendown()
    graph_turtle.goto(0, 300)
    
    # Draw x-axis markings
    for x in range(-400, 401, 20):
        graph_turtle.penup()
        graph_turtle.goto(x, -5)
        graph_turtle.pendown()
        graph_turtle.goto(x, 5)
        if x != 0:
            graph_turtle.penup()
            graph_turtle.goto(x, -20)
            graph_turtle.write(f'{x//20}', align="center", font=("Arial", 8, "normal"))
    
    # Draw y-axis markings
    for y in range(-300, 301, 20):
        graph_turtle.penup()
        graph_turtle.goto(-5, y)
        graph_turtle.pendown()
        graph_turtle.goto(5, y)
        if y != 0:
            graph_turtle.penup()
            graph_turtle.goto(-20, y - 5)
            graph_turtle.write(f'{y//20}', align="center", font=("Arial", 8, "normal"))

draw_axes()

def evaluate_expression(expression, x):
    try:
        return eval(expression)
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None

def draw_graph(expression, color):
    scale = 20  # Pixels per unit
    graph_turtle.penup()
    graph_turtle.color(color)
    for x in range(-400, 400):
        x_val = x / scale
        y_val = evaluate_expression(expression, x_val)
        if y_val is not None:
            y = y_val * scale
            if -300 <= y <= 300:
                graph_turtle.goto(x, y)
                graph_turtle.pendown()
            else:
                graph_turtle.penup()
    graph_turtle.penup()

# Main loop to input multiple functions
functions = []
colors = ["red", "blue", "green", "purple", "orange"]
color_index = 0

while True:
    input_text = window.textinput("Graphing Calculator", "Enter a function of x (e.g., x**2) or 'done' to finish:")
    if input_text.lower() == 'done':
        break
    try:
        # Validate the expression by evaluating it with a test value
        test_value = evaluate_expression(input_text, 1)
        if test_value is not None:
            functions.append((input_text, colors[color_index % len(colors)]))
            color_index += 1
        else:
            window.textinput("Error", "Invalid function. Please enter a valid function of x.")
    except Exception as e:
        window.textinput("Error", f"Invalid function: {e}. Please enter a valid function of x.")

# Draw all functions
for func, color in functions:
    draw_graph(func, color)

# Add zooming and panning features
scale = 20
origin_x, origin_y = 0, 0

def zoom_in():
    global scale
    scale *= 1.1
    graph_turtle.clear()
    draw_axes()
    for func, color in functions:
        draw_graph(func, color)

def zoom_out():
    global scale
    scale /= 1.1
    graph_turtle.clear()
    draw_axes()
    for func, color in functions:
        draw_graph(func, color)

def pan_left():
    global origin_x
    origin_x -= 20
    graph_turtle.clear()
    draw_axes()
    for func, color in functions:
        draw_graph(func, color)

def pan_right():
    global origin_x
    origin_x += 20
    graph_turtle.clear()
    draw_axes()
    for func, color in functions:
        draw_graph(func, color)

def pan_up():
    global origin_y
    origin_y += 20
    graph_turtle.clear()
    draw_axes()
    for func, color in functions:
        draw_graph(func, color)

def pan_down():
    global origin_y
    origin_y -= 20
    graph_turtle.clear()
    draw_axes()
    for func, color in functions:
        draw_graph(func, color)

# Bind keys for zooming and panning
window.listen()
window.onkey(zoom_in, "i")
window.onkey(zoom_out, "o")
window.onkey(pan_left, "Left")
window.onkey(pan_right, "Right")
window.onkey(pan_up, "Up")
window.onkey(pan_down, "Down")

# Main loop with FPS control
FPS = 2048
while True:
    start_time = time.time()
    window.update()
    elapsed_time = time.time() - start_time
    time.sleep(max(1.0/ FPS - elapsed_time, 0))

window.mainloop()