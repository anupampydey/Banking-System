import random, sqlite3
global conn, cur

def create_database():
    global conn, cur
    database = r'C:\sqlite3\database\card.s3db'
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    sqlquery1 = '''CREATE TABLE IF NOT EXISTS card
                            (id Integer Not Null, 
                            number varchar(20) Primary Key, 
                            pin varchar(4) Not Null, 
                            balance Integer Default 0)'''
    cur.execute(sqlquery1)
    conn.commit()

def create_accnt():
    global conn, cur
    random.seed()
    iin = str(400000)
    bin_st = int(0)
    bin_ed = int(1e9 - 1)
    binn = str(random.randint(bin_st, bin_ed))
    binn = binn.zfill(9)
    card15digit = iin + binn
    checksum = luhn_checksum(card15digit)
    valid_no = card15digit + str(checksum)
    idr = binn[:3] + str(checksum)
    pin = str(random.randint(0, 9999)).zfill(4)

    sqlquery2 = '''INSERT into card (id, number, pin) 
                            VALUES (?, ?, ?)'''
    cur.execute(sqlquery2, (idr, valid_no, pin))
    conn.commit()

    print('\nYour Card has been created')
    print('Your card Number:')
    print(valid_no)
    print('Your card PIN:')
    print(pin)
    print()


def luhn_checksum(card15lst):
    odin = 1
    luhnlst = []
    for dgt in card15lst:
        if odin % 2 != 0:
            digit = int(dgt) * 2
            if digit > 9:
                digit = digit - 9
                luhnlst.append(str(digit))
            else:
                luhnlst.append((str(digit)))
        else:
            luhnlst.append(dgt)
        odin += 1
    dgtsum = 0
    for dgt in luhnlst:
        dgtsum += int(dgt)
    if dgtsum % 10 == 0:  # checksum value
        return 0
    else:
        return 10 - (dgtsum % 10)


def validate_card(cardno, pin):  # Validate the card no by Luhn Algorithm
    global conn, cur
    cardlst = list(cardno)
    checksum = cardlst.pop()
    luhnchksum = luhn_checksum(cardlst)

    sqlquerys = '''Select number, pin
                   from card
                   where number = ?'''
    cur.execute(sqlquerys, (cardno,))
    row = cur.fetchone()

    if int(checksum) == luhnchksum:
        # "This is a valid card number"
        if row is not None and pin == row[1]:
            print('\nYou have successfully logged in!\n')
            login_accnt(row)
        else:
            print('\nWrong card number or PIN!\n')
    else:
        print("\nThis is an invalid card number\n")


def bal_transfer(cardinfo):
    print('\nTransfer')
    print('Enter your card number:')
    new_card = input().strip()
    ncardlst = list(new_card)
    checksum = ncardlst.pop()
    luhnchksum = luhn_checksum(ncardlst)

    if int(checksum) != luhnchksum:
        print('Probably you made a mistake in the card number. Please try again!\n')
        return
    if new_card == cardinfo[0]:
        print("You can't transfer money to the same account!\n")
        return

    sqlqryck = '''SELECT number from card where number = ?'''
    cur.execute(sqlqryck, (new_card,))
    row = cur.fetchone()

    if row is None:
        print('Such a card does not exist.')
    else:
        print('Enter how much money you want to transfer:')
        money = int(input().strip())
        querybal = '''SELECT balance from card WHERE number = ?'''
        cur.execute(querybal, (cardinfo[0],))
        balance = cur.fetchone()
        if money > balance[0]:
            print('Not enough money!\n')
        else:
            updquery1 = '''UPDATE card set balance = balance - ? WHERE number = ?'''
            updquery2 = '''UPDATE card set balance = balance + ? WHERE number = ?'''
            cur.execute(updquery1, (money, cardinfo[0]))
            conn.commit()
            cur.execute(updquery2, (money, new_card))
            conn.commit()
            print('Success!\n')


def login_accnt(rowout):
    global user_ch, conn, cur
    log_ch = 1
    while log_ch != 0:
        print('1. Balance')
        print('2. Add Income')
        print('3. Do Transfer')
        print('4. Close Account')
        print('5. Log out')
        print('0. Exit')
        log_ch = int(input('Enter Choice >').strip())
        if log_ch == 1:
            querybal = '''SELECT balance from card WHERE number = ?'''
            cur.execute(querybal, (rowout[0],))
            balance = cur.fetchone()
            print('\nBalance: ', balance[0], '\n')
        elif log_ch == 2:
            print('Enter Income: ')
            income = int(input().strip())
            sqlqryup = '''UPDATE card SET balance = balance + ? WHERE number = ?'''
            cur.execute(sqlqryup, (income, rowout[0]))
            conn.commit()
            print('Income was added!\n')
        elif log_ch == 3:
            bal_transfer(rowout)
        elif log_ch == 4:
            sqlqrdel = '''DELETE FROM card WHERE number = ?'''
            cur.execute(sqlqrdel, (rowout[0],))
            conn.commit()
            print('The account has been closed!')
        elif log_ch == 5:
            print('\nYou have successfully logged out!\n')
            break
        else:
            user_ch = 0


def display_main():
    global user_ch
    while user_ch != 0:
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        user_ch = int(input('Enter Choice >').strip())
        if user_ch == 1:
            create_accnt()
        elif user_ch == 2:  # Read the Card No & PIN from the user
            print('Enter your card number:')
            ucard = input().strip()
            print('Enter your PIN:')
            upin = input().strip()
            validate_card(ucard, upin)


user_ch = 1
create_database()
display_main()
conn.close()
