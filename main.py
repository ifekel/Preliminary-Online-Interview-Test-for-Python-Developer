import re
import random
from collections import Counter
import statistics
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

# Define the HTML data
html_data = """
<h3>TABLE SHOWING COLOURS OF DRESS BY WORKERS AT BINCOM ICT FOR THE WEEK</h3>
<table>
    <thead>
        <th>DAY</th>
        <th>COLOURS</th>
    </thead>
    <tbody>
        <tbody>
			<tr>
				<td>MONDAY</td>
				<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE,
					WHITE, BLUE, BLUE, BLUE, GREEN</td>
			</tr>
			<tr>
				<td>TUESDAY</td>
				<td>ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE,
					WHITE, BLUE, BLUE, BLUE</td>
			</tr>
			<tr>
				<td>WEDNESDAY</td>
				<td>GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE,
					BLUE, BLUE, WHITE, WHITE</td>
			</tr>
			<tr>
				<td>THURSDAY</td>
				<td>BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE,
					BLUE, BLUE, BLUE, GREEN</td>
			</tr>
			<tr>
				<td>FRIDAY</td>
				<td>GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE,
					BLUE, BLUE, BLUE, WHITE</td>
			</tr>
		</tbody>
    </tbody>
</table>
"""

# Extract the color data from HTML using regular expressions
color_pattern = r'([A-Z]+)'
colors = re.findall(color_pattern, html_data)

# Count the occurrences of each color
color_counts = Counter(colors)


# 1. Calculate the mean color
mean_color = statistics.mode(colors)


# 2. Find the most worn color throughout the week
most_worn_color = color_counts.most_common(1)[0][0]


# 3. Calculate the median color
# We'll use the statistics module to find the median
color_occurrences = list(color_counts.elements())
median_color = statistics.median(color_occurrences)


# 4. Calculate the variance of the colors
# We'll use the statistics module to find the variance
color_frequencies = list(color_counts.values())
variance = statistics.variance(color_frequencies)


# Print the results
print("1. Mean Color:", mean_color)
print("2. Most Worn Color:", most_worn_color)
print("3. Median Color:", median_color)
print("4. Variance of Color Frequencies:", variance)


# 5. BONUS: If a color is chosen at random, what is the probability that the color is red?
# Calculate the probability of choosing red at random
total_colors = len(colors)
red_count = color_counts.get('RED', 0)
probability_red = red_count / total_colors

print("5. Probability of Choosing Red at Random:", probability_red)


# 6. Save the colours and their frequencies in postgresql database
# Database connection parameters
db_params = {
    "database": os.getenv("db_name"),
    "user": os.getenv("db_user"),
    "password": os.getenv("db_password"),
    "host": os.getenv("db_host"),
    "port": os.getenv("db_port"),
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)

# Create a cursor
cur = conn.cursor()

# Define the table name
table_name = "color_frequencies"

# Create the table if it doesn't exist
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        color TEXT PRIMARY KEY,
        frequency INT
    )
"""
cur.execute(create_table_query)
conn.commit()

# Insert color frequencies into the table
for color, frequency in color_counts.items():
    insert_query = sql.SQL("INSERT INTO {} (color, frequency) VALUES (%s, %s)").format(sql.Identifier(table_name))
    cur.execute(insert_query, (color, frequency))
    conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
print("6. Color frequencies saved to PostgreSQL database.")


# 7. BONUS write a recursive searching algorithm to search for a number
def recursive_binary_search(arr, target, low, high):
    if low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid  # Element found, return its index
        elif arr[mid] < target:
            return recursive_binary_search(arr, target, mid + 1, high)  # Search right half
        else:
            return recursive_binary_search(arr, target, low, mid - 1)  # Search left half
    else:
        return -1  # Element not found


numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17]
target = int(input("Enter a number to search for: "))
index = recursive_binary_search(numbers, target, 0, len(numbers) - 1)

if index != -1:
    print(f"Found {target} at index {index}.")
else:
    print(f"{target} not found in the list.")


# 8. Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.
binary_number = ''.join(random.choice('01') for _ in range(4))

# Convert the binary number to base 10
decimal_number = int(binary_number, 2)

print(f"Random 4-digit binary number: {binary_number}")
print(f"Converted to base 10: {decimal_number}")


# 9. Write a program to sum the first 50 fibonacci sequence.
def fibonacci(n):
    fib_series = [0, 1]
    while len(fib_series) < n:
        next_fib = fib_series[-1] + fib_series[-2]
        fib_series.append(next_fib)
    return fib_series

# Calculate the first 50 Fibonacci numbers
n = 50
fib_series = fibonacci(n)

# Sum the first 50 Fibonacci numbers
fib_sum = sum(fib_series)

print(f"The sum of the first {n} Fibonacci numbers is: {fib_sum}")

