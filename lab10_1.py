import psycopg2
import csv

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='your_db',
    user='your_user',
    password='your_password',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        phone VARCHAR(20) NOT NULL
    );
""")
conn.commit()


# Insert data from CSV
def insert_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    print("Data inserted from CSV.")


# Insert data from console
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    print("Data inserted from console.")


# Update data
def update_data():
    target = input("Update by name or phone? ").strip().lower()
    if target == "name":
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    elif target == "phone":
        old_phone = input("Enter current phone: ")
        new_phone = input("Enter new phone: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, old_phone))
    conn.commit()
    print("Data updated.")


# Query data with filters
def query_data():
    print("Search by:")
    print("1. All entries")
    print("2. Name")
    print("3. Phone")
    choice = input("Choose option: ")

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
    elif choice == "2":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (name,))
    elif choice == "3":
        phone = input("Enter phone: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))

    rows = cur.fetchall()
    for row in rows:
        print(row)


# Delete data
def delete_data():
    target = input("Delete by name or phone? ").strip().lower()
    if target == "name":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif target == "phone":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    print("Data deleted.")


# Menu
def menu():
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update")
        print("4. Query")
        print("5. Delete")
        print("6. Exit")
        option = input("Choose an option: ")

        if option == "1":
            insert_from_csv("phonebook.csv")
        elif option == "2":
            insert_from_console()
        elif option == "3":
            update_data()
        elif option == "4":
            query_data()
        elif option == "5":
            delete_data()
        elif option == "6":
            break
        else:
            print("Invalid option.")


menu()

# Clean up
cur.close()
conn.close()
