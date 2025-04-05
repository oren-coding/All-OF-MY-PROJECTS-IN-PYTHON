import calendar

# Create a plain text calendar
text_cal = calendar.TextCalendar(calendar.SUNDAY)
print("Text Calendar for March 2025:")
print(text_cal.formatmonth(2025, 3))

# Get the weekday of the first day of the month and the number of days in the month
first_weekday, num_days = calendar.monthrange(2025, 3)
print(f"First weekday: {first_weekday}, Number of days: {num_days}")