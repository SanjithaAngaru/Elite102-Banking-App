#I connected SQL to VS Code with the code given to me from C2C. Template from C2C
import mysql.connector

#connecting to the SQL database
conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Baba1010$',
        database='Elite-102-2026'
)
cursor = conn.cursor()


def choice_one(): #choice 1  (completed) CREATING AN ACCOUNT
    print("You have chosen to create an account.\n")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    balance = float(input("Enter your initial deposit: "))
    cursor.execute("INSERT INTO accounts (first_name, last_name, balance, status) VALUES (%s, %s, %s, %s)",(first_name, last_name, balance, "Active"))
     #NOTE: According to google, the %s is are used to tell SQL not to enter in the variable name, but the content of the variables.
    print(f"Account created successfully {first_name}! Click 'View Existing Accounts' to view your account details.")
    conn.commit()

def choice_two(): #choice two (completed) DEPOSIT/WITHDRAW
    print("You have chosen to deposit/withdraw.\n")
    choice = input("Enter 1 to deposit or 2 to withdraw: ")
    with conn.cursor() as cursor: 
        if choice == '1': # Deposit to account
            print("You have chosen to deposit.")
            account_id = int(input("Enter your account ID:"))
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            cursor.execute("SELECT first_name, last_name FROM accounts WHERE account_id = (%s)", (account_id,))
            result = cursor.fetchone()
            if result[0].lower() != first_name.lower() or result[1].lower() != last_name.lower(): #lines 30 -36 to check if the first and last name match the account ID
                print("Account ID not found. Please try again.")
                return

            cursor.execute("SELECT first_name, last_name FROM accounts WHERE account_id = %s", (account_id,))
            result = cursor.fetchone()
            if not result:
                    print("Account ID not found. Please try again.")
                    return
            amount = float(input("Enter the amount to deposit: "))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, account_id))
            #updates transactions table with deposit
            account_name = f"{result[0]} {result[1]}"
            cursor.execute("INSERT INTO transactions (account_name, transaction_type, amount) VALUES (%s, %s, %s)",(account_name, 'Deposit', amount))
            #NOTE: I asked Google to help me with the UPDATE query in SQL.
            conn.commit()
            print(f"Deposited ${amount} to account {account_name}.")
        elif choice == '2': # Withdraw from account
            print("You have chosen to withdraw.")
            account_id = int(input("Enter your account ID:"))
            first_name = input("Enter your first name: ")
            last_name = input("Enter your last name: ")
            cursor.execute("SELECT first_name, last_name FROM accounts WHERE account_id = (%s)", (account_id,))
            result = cursor.fetchone()
            if result[0].lower() != first_name.lower() or result[1].lower() != last_name.lower(): #(copied here)lines 30 -36 to check if the first and last name match the account ID
                print("Account ID not found. Please try again.")
                return                       
            with conn.cursor() as cursor:
                cursor.execute("SELECT first_name, last_name FROM accounts WHERE account_id = %s", (account_id,))
                result = cursor.fetchone()
                if not result:
                    print("Account ID not found. Please try again.")
                    return
                amount = float(input("Enter the amount to withdraw: "))
                cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, account_id))
                #updates transactions table with withdrawal
                account_name = f"{result[0]} {result[1]}"
                cursor.execute("INSERT INTO transactions (account_name, transaction_type, amount) VALUES (%s, %s, %s)",(account_name, 'Withdrawal', amount))
                conn.commit()
                
                cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,)) #withdrawal check 
                current_balance = cursor.fetchone()[0]
                if amount > float(current_balance):
                    print("Insufficient funds.")
                    return
                print(f"Withdrew ${amount} from account {account_name}.")
        else:
            print("Invalid option. please try again.")

#MINI FUNCTION FOR ---UNITTEST CHECKING--- Withdrawal Validation
def validate_withdrawal(amount, current_balance):
    if amount < 0:
        return "Negative Number"
    if amount > current_balance:
        return "Insufficient Funds"
    return "Valid Withdrawal"

def choice_three(): #choice three (completed) VIEW ACTIVE ACCOUNTS
    print("\nYou have chosen to view active accounts.\nHere are the active accounts:")
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM accounts WHERE status = 'Active'")
        rows = cursor.fetchall()
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} {row[2]} | Balance: ${row[3]} | Status: {row[4]}")
    
'''I asked Google and Github Copilot for help with the use of fetchone() and the [0]. 
Fetchone is used to get one row from the database and converts it into a tuple. 
The zero brings the first element of the tuple which is the new balance.'''

def choice_four(): #choice four (completed) CHECK BALANCE
    print("\nYou have chosen to check balance.")
    account_id = int(input("Enter your account ID:"))
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    with conn.cursor() as cursor:
        cursor.execute("SELECT first_name, last_name FROM accounts WHERE account_id = (%s)", (account_id,))
        result = cursor.fetchone()
        if not result:
            print(f"Account ID {account_id} not found. Please try again.")
            return
        elif result[0].lower() != first_name.lower() or result[1].lower() != last_name.lower(): #copied here lines 30 -36 to check if the first and last name match the account ID
            print("Account ID not found. Please try again.")
            return

        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (account_id,))
        balance = cursor.fetchone()[0]
        print(f"Your current balance is: ${balance}")
        return
    

# MAIN MENU loop - CLS Version. TO-DO: Change into Tkinter version (COMPLETED)
if __name__ == "__main__": #it only runs this file directly, not the other imported files
    while True:     #Terminal UI created -- (may add updates)
        print("\n----Welcome to Elite 102 Banking App. Choose one of the following:----")
        print("1. Create Account\n2. Deposit/Withdraw\n3. View Active Accounts\n4. Check Balance\n5. Exit")
        choice = input("Enter your number: ")
        if choice == '1':
            choice_one()
        elif choice == '2':
            choice_two()
        elif choice == '3':
            choice_three()
        elif choice == '4':
            choice_four()
        elif choice == '5':
            print("Thank you for using Elite 102 Banking App.")
            break

    conn.close()
