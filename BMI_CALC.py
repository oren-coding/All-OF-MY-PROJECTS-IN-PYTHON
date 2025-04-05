mass = float(input("Enter your mass in kg: "))
height = float(input("Enter your height in meters: "))

bmi = mass / (height ** 2)

print("BMI:", round(bmi, 1))
