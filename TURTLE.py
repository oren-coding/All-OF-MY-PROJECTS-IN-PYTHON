import turtle
import math
import time

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("3D Rotating Cube")
screen.tracer(0)  # Turn off automatic screen updates

# Create a turtle named "t"
t = turtle.Turtle()
t.speed(0)  # Set the turtle speed to the maximum

# Define the vertices of the cube
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Define the edges of the cube
edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7]
]

# Function to draw a line between two points
def draw_line(x1, y1, x2, y2):
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.goto(x2, y2)

# Function to project 3D coordinates to 2D
def project(x, y, z, angle_x, angle_y, angle_z):
    # Rotate around the x-axis
    y, z = y * math.cos(angle_x) - z * math.sin(angle_x), y * math.sin(angle_x) + z * math.cos(angle_x)
    
    # Rotate around the y-axis
    x, z = x * math.cos(angle_y) + z * math.sin(angle_y), -x * math.sin(angle_y) + z * math.cos(angle_y)
    
    # Rotate around the z-axis
    x, y = x * math.cos(angle_z) - y * math.sin(angle_z), x * math.sin(angle_z) + y * math.cos(angle_z)
    
    # Project the 3D coordinates to 2D
    factor = 200 / (z + 5)
    x, y = x * factor, y * factor
    return x, y

# Rotation angles
angle_x = 0
angle_y = 0
angle_z = 0

# Flags to indicate whether a key is pressed
rotate_left_flag = False
rotate_right_flag = False
rotate_up_flag = False
rotate_down_flag = False
rotate_clockwise_flag = False
rotate_counterclockwise_flag = False

# Functions to update rotation flags
def rotate_left():
    global rotate_left_flag
    rotate_left_flag = True

def stop_rotate_left():
    global rotate_left_flag
    rotate_left_flag = False

def rotate_right():
    global rotate_right_flag
    rotate_right_flag = True

def stop_rotate_right():
    global rotate_right_flag
    rotate_right_flag = False

def rotate_up():
    global rotate_up_flag
    rotate_up_flag = True

def stop_rotate_up():
    global rotate_up_flag
    rotate_up_flag = False

def rotate_down():
    global rotate_down_flag
    rotate_down_flag = True

def stop_rotate_down():
    global rotate_down_flag
    rotate_down_flag = False

def rotate_clockwise():
    global rotate_clockwise_flag
    rotate_clockwise_flag = True

def stop_rotate_clockwise():
    global rotate_clockwise_flag
    rotate_clockwise_flag = False

def rotate_counterclockwise():
    global rotate_counterclockwise_flag
    rotate_counterclockwise_flag = True

def stop_rotate_counterclockwise():
    global rotate_counterclockwise_flag
    rotate_counterclockwise_flag = False

# Bind the arrow keys to the rotation functions
screen.listen()
screen.onkeypress(rotate_left, "Left")
screen.onkeyrelease(stop_rotate_left, "Left")
screen.onkeypress(rotate_right, "Right")
screen.onkeyrelease(stop_rotate_right, "Right")
screen.onkeypress(rotate_up, "Up")
screen.onkeyrelease(stop_rotate_up, "Up")
screen.onkeypress(rotate_down, "Down")
screen.onkeyrelease(stop_rotate_down, "Down")
screen.onkeypress(rotate_clockwise, "a")
screen.onkeyrelease(stop_rotate_clockwise, "a")
screen.onkeypress(rotate_counterclockwise, "d")
screen.onkeyrelease(stop_rotate_counterclockwise, "d")

# Main loop to rotate and draw the cube
while True:
    t.clear()
    projected_vertices = []
    for vertex in vertices:
        x, y, z = vertex
        x, y = project(x, y, z, angle_x, angle_y, angle_z)
        projected_vertices.append((x, y))
    
    for edge in edges:
        x1, y1 = projected_vertices[edge[0]]
        x2, y2 = projected_vertices[edge[1]]
        draw_line(x1, y1, x2, y2)
    
    # Update rotation angles based on flags
    if rotate_left_flag:
        angle_y -= 0.01
    if rotate_right_flag:
        angle_y += 0.01
    if rotate_up_flag:
        angle_x -= 0.01
    if rotate_down_flag:
        angle_x += 0.01
    if rotate_clockwise_flag:
        angle_z += 0.01
    if rotate_counterclockwise_flag:
        angle_z -= 0.01

    screen.update()  # Manually update the screen
    time.sleep(0.0001)  # Control the FPS (adjust the sleep time as needed)

# Close the turtle graphics window when clicked
screen.exitonclick()