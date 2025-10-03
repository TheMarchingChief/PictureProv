import webbrowser
import boto3

# your personal performer number. Set using input()
performer_num = int(input("Please enter your performer number: "))

# please set these values accordingly for the performer (read-only)
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

# to ensure no infinite loop of tab opening
storeditem = 0
print("Please press Ctrl + C to end the program")

# Infinite loop! User must end the program with Ctrl + C
# Continuously scans the table, if performer value == performer_num, open the image!
while True:
    items = scan_all_items(table)
    for item in items:
        if item['performer'] == performer_num and item != storeditem:
            webbrowser.open_new_tab(item['link'])
            storeditem=item
