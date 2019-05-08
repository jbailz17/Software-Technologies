# Task 4 Script - Creates 2 seperate figures displaying the 
# total monthly violations for the below:
#
# Fig 1:
# - Zip code with the highest total violations
# - Zip code with the lowest total violations
# - Average total violations
#
# Fig 2:
# - McDonald's average total monthly violations
# - Burger King average total monthly violations

import sqlite3
import numpy as np
import matplotlib.pyplot as plt

# Define functions for the script


def plot_res(average, result, line, label):
    # Plot the result data onto the figure

    x_axis = []
    y_axis = []

    # Check to see if plotting the average or total
    if (average):
        for r in result:
            x_axis.append(r[0])
            y_axis.append((r[1] / r[2]))
    else:
        for r in result:
            x_axis.append(r[1])
            y_axis.append(r[2])

    plt.plot(x_axis, y_axis, ('%s' % (line)), label=label)

def plot_setup(title):
    # General setup for the figure

    plt.title(title)
    plt.legend()
    plt.grid(linestyle='--', which='both')
    plt.minorticks_on()
    plt.xticks(np.arange(0, len(x_axis_range), step=4), 
           rotation=20, horizontalalignment='right')
    plt.xlabel('Month')
    plt.ylabel('Number of Violations')
    plt.tight_layout()

def zip_query(zip):
    # Query database for total monthly violations based on zip code

    sql_command = ('''
        SELECT 
            facility_zip,
            strftime("%%Y-%%m", activity_date),
            COUNT(v.serial_number)
        FROM Inspections i
        LEFT JOIN Violations v ON i.serial_number = v.serial_number
        WHERE facility_zip = '%s'
        GROUP BY facility_zip, strftime("%%Y-%%m", activity_date)
    ''' % (zip))

    cursor.execute(sql_command)
    return cursor.fetchall()

def avg_query(name):
    # Query database for total monthly violations and the total amount
    # of stores that where inspected each month based on facility id

    sql_command = ('''
    SELECT 
        strftime("%%Y-%%m", activity_date), 
        total_violations, 
        total_stores
    FROM Inspections i
        LEFT JOIN (
            SELECT 
                strftime('%%Y-%%m', activity_date) as v_date,
                COUNT(*) as total_violations
            FROM Inspections i
                LEFT JOIN Violations v
                ON i.serial_number = v.serial_number
            WHERE facility_name LIKE '%s%%'
            GROUP BY strftime('%%Y-%%m', activity_date) 
        ) AS v_count
        ON v_count.v_date = strftime("%%Y-%%m", i.activity_date)
        LEFT JOIN (
            SELECT
                strftime('%%Y-%%m', activity_date) as s_date, 
                COUNT(DISTINCT facility_id) as total_stores
            FROM Inspections i
                LEFT JOIN Violations v
                ON i.serial_number = v.serial_number
            WHERE facility_name LIKE '%s%%'
            GROUP BY strftime('%%Y-%%m', activity_date)
        ) AS s_count
        ON s_count.s_date = strftime("%%Y-%%m", i.activity_date)
    GROUP BY strftime("%%Y-%%m", activity_date)
    ''' % (name, name))

    cursor.execute(sql_command)
    return cursor.fetchall()

# Setup connection with the database
connection = sqlite3.connect('violations.db')
cursor = connection.cursor()

# Query database for total violations made by each zip code
sql_command = '''
    Select facility_zip, COUNT(v.serial_number)
    FROM Inspections i
        LEFT JOIN Violations v 
        ON i.serial_number = v.serial_number
    GROUP BY facility_zip
    ORDER BY COUNT(v.serial_number) DESC
'''

cursor.execute(sql_command)
result = cursor.fetchall()

# Store the zip codes with the highest and lowest 
# total violations based on the results from the above query
highest = result[0]
lowest = result[(len(result) - 1)]

# Query the database to retrieve the range of dates
sql_command = '''
    SELECT strftime('%Y-%m', activity_date)
    FROM Inspections
    GROUP BY strftime('%Y-%m', activity_date)
'''

cursor.execute(sql_command)
result = cursor.fetchall()

# Set the x axis range for the figures
x_axis_range = []
for r in result:
    x_axis_range.append(r[0])

print('Creating Figure 1...')
plt.figure(1)

# Retrieve the total monthly violations for the "highest" zip code
# and plot the results
result = zip_query(highest[0])
plot_res(False, result, 'bd-', ('%s (Highest Total Violations)' % (highest[0])))

# Retreive the total monthly violations for the "lowest" zip code
# and plot the results
result = zip_query(lowest[0])
plot_res(False, result, 'rd-', ('%s (Lowest Total Violations)' % (lowest[0])))

# Query the data base for the total amount of violations and the total
# total amount of zip codes that were inspected for each month
sql_command = '''
    SELECT 
        strftime("%Y-%m", activity_date), 
        total_violations, 
        total_zip
    FROM Inspections i
        LEFT JOIN (
            SELECT 
                strftime('%Y-%m', activity_date) as v_date,
                COUNT(*) as total_violations
            FROM Inspections i
                LEFT JOIN Violations v
                ON i.serial_number = v.serial_number
            GROUP BY strftime('%Y-%m', activity_date) 
        ) AS v_count
        ON v_count.v_date = strftime("%Y-%m", i.activity_date)
        LEFT JOIN (
            SELECT
                strftime('%Y-%m', activity_date) as z_date, 
                COUNT(DISTINCT facility_zip) as total_zip
            FROM Inspections i
                LEFT JOIN Violations v
                ON i.serial_number = v.serial_number
            GROUP BY strftime('%Y-%m', activity_date)
        ) AS z_count
        ON z_count.z_date = strftime("%Y-%m", i.activity_date)
    GROUP BY strftime("%Y-%m", activity_date)
'''

cursor.execute(sql_command)
result = cursor.fetchall()

# Plot the average total monthly violations for all zip codes
plot_res(True, result, 'gd-', 'Average Total Violations')

# Setup the first figure and save it
plot_setup('Total Monthly Violations')
plt.savefig('Fig1.png')

print('Creating Figure 2...')
plt.figure(2)

# Plot the average total monthly violations for all McDonald's stores
result = avg_query("MCDONALD''S")
plot_res(True, result, 'bd-', "McDonald's")

# Plot the average total monthly violations for all Burger King stores
result = avg_query('BURGER KING')
plot_res(True, result, 'rd-', 'Burger King')

# Setup figure 2 and save it
plot_setup("McDonald's Vs Burger King (Total Monthly Violations)")
plt.savefig('Fig2.png')

# Show both figures
print('Figures Created')
plt.show()

# Close database connection
connection.close()