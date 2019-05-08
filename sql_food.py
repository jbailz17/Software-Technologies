# Task 2 Script - List the distinctive businesses that have had at least
# 1 violation and store their information into a new database table.
# Then list the distinctive businesses along with their total amount
# of violations 

import sqlite3

# Setup connection to the database
connection = sqlite3.connect('violations.db')
cursor = connection.cursor()

# Drop the Previous_Violations table if it already exists
connection.execute('DROP TABLE IF EXISTS Previous_Violations')

# Create the Previous_Violations table
print('Creating Table...\n')
sql_command = '''
    CREATE TABLE Previous_Violations (
        pre_violation_id INTEGER NOT NULL,
        facility_name VARCHAR(255),
        facility_address VARCHAR(255),
        facility_zip INTEGER,
        facility_city VARCHAR(255),
        CONSTRAINT PK_pre_violation_id PRIMARY KEY (pre_violation_id)
    )
'''

cursor.execute(sql_command)
print('Table Created\n')

print('Importing Data...\n')

# Query the database for information of each distinctive business 
# that has at least one violation
sql_command = '''
    Select DISTINCT
        facility_id,
        facility_name,
        facility_address,
        facility_zip,
        facility_city
    FROM Inspections i, Violations v
    WHERE i.serial_number = v.serial_number
    ORDER BY facility_name
'''

cursor.execute(sql_command)
result = cursor.fetchall()

# List the business information to the console and insert it into
# the Previous_Violations table
for r in result:
    print('%-30s : %-30s' %(r[1], r[2]))
    sql_command = '''
        INSERT INTO Previous_Violations (
            facility_name,
            facility_address,
            facility_zip,
            facility_city
        )
        VALUES (?,?,?,?)
    '''

    cursor.execute(sql_command, (r[1], r[2], r[3], r[4]))

print('\nData Imported\n')

# Query the database for the total amount of violations made by
# each distinctive business
print('Results:\n')
sql_command = '''
    SELECT facility_id, 
        facility_name,
        facility_address,
        COUNT(*)
    FROM Inspections i
        INNER JOIN Violations v
        ON i.serial_number = v.serial_number
    GROUP BY facility_id, facility_name, facility_address
    ORDER BY COUNT(*)
'''

cursor.execute(sql_command)
result = cursor.fetchall()

# Display the result of the above query to the console
for r in result:
    print('%-30s : %-30s : %-5d' %(r[1], r[2], r[3]))

# Save the changes made to the database and close the connection
connection.commit()
connection.close()