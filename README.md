# Audience Interaction Prep
Create a JotForm, and insert a Drawing Board widget onto your form
Create a blank Kahoot with 20 or so questions, set the number of answers to each question == the number of performers you have on stage
Place the link to the Kahoot on the Thank You page in the JotForm
Create a QR code that links to the JotForm, and print it/make it available for the audience to see/scan in some way on the day of the show

# AWS DynamoDB Table
In AWS, create a DynamoDB table. All default settings are fine.
Create 2 IAM users:
- The first user, Controller, should have read/write permissions to your DynamoDB table
- The second user, Performer, should only have read permissions to your DynamoDB table
Make sure you save the access key and secret access key for each user somewhere safe. You'll need them

# Python Programs
In both Python programs, controller.py and performer.py, ensure that the variables at the top are set properly:
Performer.py:
- ACCESS_KEY, SECRET_ACCESS_KEY, TABLE_NAME, REGION_NAME
Controller.py:
- ACCESS_KEY, SECRET_ACCESS_KEY, TABLE_NAME, REGION_NAME, num_performers, csv_filename

# Creating executables
open a terminal in this directory. Use:
pip install pyinstaller

Then, to create an executable:
For Performers:
pyinstaller performer.py --onefile

For Controllers:
pyinstaller controller.py --onefile

# That's it!
That is a lot of setup, but you'll have a killer performance!
