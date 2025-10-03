import csv
import boto3
from boto3.dynamodb.conditions import Attr

# please set these values to the number of performers you have and your CSV directory
num_performers = 4
csv_filename = 'temp'

# please set these values accordingly for the controller (read/write access)
ACCESS_KEY = 'temp'
SECRET_ACCESS_KEY = 'temp'
TABLE_NAME = 'tablename'
REGION_NAME = 'servername'

dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME,
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_ACCESS_KEY)

table = dynamodb.Table(TABLE_NAME)

# Returns all items in the table
def scan_all_items(table):
    items = []
    response = table.scan()
    items.extend(response.get('Items', []))

    # Keep scanning until there's no more data
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response.get('Items', []))
    return items

# Uses scan_all_items to print all the items in the table
def print_all_items(table):
    try:
        all_items = scan_all_items(table)
        for item in all_items:
            print(item)
        print(f"\nTotal items retrieved: {len(all_items)}")
    except Exception as e:
        print(e)

# Changes the specified item in the table.
# Takes in table, key (int), attribute (String, see add_an_item for options), value (any)
def change_an_item(table, key, attribute, value):
    try:
        response = table.update_item(
            Key={
                'key': key   # primary key of the item you want to update
            },
            UpdateExpression="SET #attr = :val",
            ExpressionAttributeNames={
                '#attr': attribute    # replace 'name' with the attribute you want to edit
            },
            ExpressionAttributeValues={
                ':val': value
            },
            ReturnValues="ALL_NEW"
        )

        print("Update succeeded!")
        print("Updated item:", response['Attributes'])

    except Exception as e:
        print("Update failed:", e)

# Adds an item to the table. Takes in table, key (int), performer (int), link (String)
def add_an_item(table, key, performer, link):
    try:
        response = table.put_item(
            Item={
                'key': key,          # required primary key
                'performer': performer,
                'link': link
            },
            # only add an item if it doesn't already exist
            # (by attribute key. key is reserved, so use placeholder #k & define it as key)
            ConditionExpression="attribute_not_exists(#k)",
            ExpressionAttributeNames={'#k': 'key'}
        )

        print("Item added successfully!")

    except Exception as e:
        print("Failed to add item:", e)

# Removes a single item from the table
def delete_an_item(table, key):
    try:
        response = table.delete_item(
            Key={
                'key': key   # the primary key of the item you want to delete
            }
        )
        print("Item deleted successfully!")
    except Exception as e:
        print("Delete failed:", e)

# Removes all items from the table (using a loop)
def delete_all_items(table):
    # First, get all items
    items = scan_all_items(table)
    print(f"Found {len(items)} items to delete...")

    # Delete each one
    for item in items:
        try:
            table.delete_item(Key={'key': item['key']})
            print(f"Deleted item with key = {item['key']}")
        except Exception as e:
            print(f"Failed to delete item {item['key']}: {e}")

# open the CSV file and create a reader that skips the header, then add all items from the CSV file
def add_csv_items(table, csv_filename):
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for i, row in enumerate(csv_reader): #skip first item (header)
            if i == 0:
                continue
            item = row[0][9:].strip()
            add_an_item(table, i-1, 0, item)

# Empties the table and populate it using the current csv file state!
def clear_then_populate(table, csv_filename):
    delete_all_items(table)
    add_csv_items(table, csv_filename)
    print_all_items(table)



# Controller downloads the CSV file from Jotform and copies the contents to responses.csv (see directory below)
# Get the CSV file from the set directory and upload its contents to the DynamoDB table

clear_then_populate(table, csv_filename)

# Used for storing controller input
c_entry = num_performers + 1

# Controller enters a performer number for each Kahoot round
# Table is scanned, the entry with performer number c_entry is replaced with 69,
# and the first entry with performer value 0 is chosen
while c_entry > 0:
    c_entry = int(input("Who lost the Kahoot (in a tie, pick whichever)\n"
                    f"Enter your choice (1-{num_performers}): "))
    if c_entry <= num_performers and c_entry > 0: #input validation
        # find the selected performer's current item and change the performer value to num_performers+1
        items = scan_all_items(table)
        for item in items:
            if item['performer'] == c_entry:
                change_an_item(table, item['key'], 'performer', num_performers+1)

        # find the first value set to 0 and set it to c_entry, then end loop
        for item in items:
            if item['performer'] == 0:
                change_an_item(table, item['key'], 'performer', c_entry)
                c_entry = num_performers + 1
                break
        if c_entry != num_performers + 1:
            print("Out of entries, nothing changed! Please end the performance shortly!")
    elif c_entry > 0:
        print("!!!You don't have that many performers! Try again.")
    else:
        print("Ending program...")

print("-----Final table-----")
print_all_items(table)

