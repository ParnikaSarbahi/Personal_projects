import mysql.connector
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
import pandas
from datetime import date

mydb=mysql.connector.connect(host='localhost',user="root",passwd="mysql")
mycursor=mydb.cursor()
mycursor.execute("create database if not exists ShoppingMall")
mycursor.execute("use ShoppingMall") 
mycursor.execute("create table  if not exists login(username varchar(25) not null ,password varchar(25) not null)")
mycursor.execute("create table if not exists purchase(name varchar(25) not null,amount int,purchase_date date)")
mycursor.execute("create table if not exists stock(pcode int,pname varchar(25),price int,quantity int)")
mydb.commit()#to save changes
def addItem():
    pcode=int(input("Enter product code:"))
    pname=input("Enter product name:")
    price=int(input("Enter product price:"))
    stock=int(input("Enter stock quantity:"))
    mycursor.execute("INSERT INTO stock VALUES (%s, %s, %s,%s)", (pcode, pname, price,stock))
    mydb.commit()
    print("Record inserted successfully\n")
    op=input("Do you want to add another item in this table?(y/n):")
    return op

def DisplayItems(n):
    if n==1:
        mycursor.execute("SELECT * FROM stock")
        results = mycursor.fetchall()
        if not results:
            print("No stock available")
            return False
        else:
            headers = ["PCODE", "PNAME", "PRICE", "QUANTITY"]
            print(tabulate(results, headers, tablefmt="grid"))
            return True
    elif n==2:
        mycursor.execute("SELECT * FROM stock")
        results = mycursor.fetchall()
        if not results:
            print("No stock available")
            return False

        product_names = [result[1] for result in results]
        stock_quantities = [result[3] for result in results]
        fig, ax = plt.subplots()
        ax.bar(product_names, stock_quantities)

        #Set labels and title
        ax.set_xlabel('Product Name')
        ax.set_ylabel('Stock Quantity')
        ax.set_title('Stock Quantity of Products')

        #Set ticks for the x-axis
        ax.set_xticks(product_names)
        ax.set_xticklabels(product_names, rotation=45, ha='right')
        
        ax.set_ylim(0, 100)#Setting y-axis ki limit

        # Show plot
        plt.show()

def adjustPrices(factor, condition):
    mycursor.execute("SELECT pcode, price FROM stock")
    items = mycursor.fetchall()
    if items:
        codes, prices = zip(*items)#Unzips into two tuples
        prices = np.array(prices)
        if condition == "markup":
            prices=prices+prices*(factor/100)
        elif condition == "discount":
            prices=prices-prices*(factor/100)
        
    # Update prices in the database
    for code, new_price in zip(codes, prices):
        mycursor.execute("UPDATE stock SET price = %s WHERE pcode = %s", (int(new_price), code))
    mydb.commit()
    print("Prices updated successfully.")

def admin():
    epass=input("Enter password:")
    mycursor.execute("select * from login")
    for username,password in mycursor:
        if(epass==password):  
            print("\nPassword verified,Welcome Admin!")
            loop2='y'
            while(loop2=='y' or loop2=='Y'):
                print("\nWhich function would you like to perform?")
                print("1.Adding new item")
                print("2.Updating price")
                print("3.Adjusting prices")
                print("4.Deleting Item")
                print("5.Displaying all Items")
                print("6.Changing Password")
                print("7.Log out")
                ch1=int(input("Admin enter your choice:"))
                if(ch1==1):#adding item
                    loop='y'
                    while(loop.lower()=='y'):
                        loop=addItem()
                    loop2=input("Do you want to continue functioning as an admin?(y/n):") 
                    
                elif(ch1==2):#updating item
                    loop='y'
                    while(loop.lower()=='y'):
                        DisplayItems(1)
                        pcode=int(input("\nEnter code of product you want to change price of:"))
                        new_price=int(input("Enter new price of selected product:"))
                        mycursor.execute("UPDATE stock SET price = %s WHERE pcode = %s", (new_price, pcode))
                        mydb.commit()
                        print("Price updated successfully\n")
                        loop=input("Do you want to update another item in this table?(y/n):")
                    loop2=input("Do you want to continue functioning as an admin?(y/n)")
                    
                elif(ch1==3):#Adjusting prices
                    ch=int(input("Enter 1 for applying discount on all items\nEnter 2 for marking up the price on all items"))
                    if(ch==1):
                        factor=int(input("Enter factor by which you want to apply discount:"))
                        adjustPrices(factor,"discount")
                        
                    elif(ch==2):
                        factor=int(input("Enter factor by which you want to mark up the price:"))
                        adjustPrices(factor,"markup")
                        
                    loop2=input("Do you want to continue functioning as an admin?(y/n):")
                elif(ch1==4):#deleting item
                    loop='y'
                    while(loop.lower()=='y'):
                        DisplayItems(1)
                        pcode=int(input("enter code of product you want to delete:"))
                        mycursor.execute("DELETE FROM stock WHERE pcode = %s",(pcode,))
                        mydb.commit()
                        loop=input("Do you want to delete another item in this table?(y/n):")
                    loop2=input("Do you want to continue functioning as an admin?(y/n):")  
                elif ch1 == 5:# Displaying all items
                        n=int(input("Enter 1 for tabular data or 2 for charts"))
                        DisplayItems(n)
                
                elif(ch1==6):
                    old_password=input("Enter old password:")
                    mycursor.execute("SELECT * FROM login")
                    for username1,password in mycursor:
                        if(old_password==password):
                            print("\nSuccessfully verified")
                            new_password=input("enter new password:")
                            mycursor.execute("UPDATE login SET password = %s", (new_password,))
                            mydb.commit()
                            print("Updated successfully")
                        else:
                            print("wrong password")
                            print()
                
                elif(ch1==7):
                    break
                else:
                    print("Invalid choice")
        else:
            print("wrong password")

def customer():
    loop2='y'
    while(loop2=='y' or loop2=='Y'):
        print("Which function would you like to perform?\n1.Shop\n2.Payment\n3.Viewing all Items\n4.Go back")
        ch2=int(input("Enter choice:"))
        if(ch2==1):#shop
                name=input("Enter your name:")
                name=name.lower()
                loop='y'
                DisplayItems(1)
                while(loop.lower()=='y'):
                    today = date.today()
                    pcode = int(input("Enter product code of item you wish to purchase:"))
                    quant = int(input("Enter quantity of item you wish to purchase:"))
                    mycursor.execute("SELECT * FROM stock WHERE pcode = %s",(pcode,))
                    for t_code, t_name, t_price,t_stock in mycursor:
                        amount = t_price*quant
                    mycursor.execute("SELECT * FROM purchase WHERE name = %s",(name,))
                    c=0
                    for i in mycursor:
                        c+=1
                    mydb.commit()
                    if c>0:
                        mycursor.execute("UPDATE purchase SET amount = amount + %s WHERE name = %s",(amount, name))
                        mycursor.execute("UPDATE stock SET quantity =quantity-%s WHERE pcode = %s",(quant,pcode))
                        mydb.commit()
                        print("item added\n")
                        loop=input("Do you want to purchase another item?(y/n):")
                    else:
                        mycursor.execute("INSERT INTO purchase VALUES (%s, %s,%s)",(name,amount,today))
                        mycursor.execute("UPDATE stock SET quantity =quantity-%s WHERE pcode = %s",(quant,pcode))
                        mydb.commit()
                        print("purchase successful\n")
                        loop=input("Do you want to purchase another item?(y/n):")
                    
                loop2 = input("\nDo you want to continue functioning as a customer? (y/n):")  
                
        elif(ch2==2):#payment
            name = input("\nEnter your name:")
            name=name.lower()
            mycursor.execute("SELECT * FROM purchase WHERE name = %s", (name,))
            for n,a,d in mycursor:
                print("\nHello", n, "!! Amount needed to be paid by you = ₹", a, "\n")
            
        elif(ch2==3):
            n=int(input("Enter 1 for tabular data or 2 for charts"))
            DisplayItems(n)
            print("\n")
        elif(ch2==4):
            break
        else:
            print("Invalid choice!Please try again")                           

#MAIN FUNCTION STARTS    
z=0
mycursor.execute("select * from login")
for i in mycursor:
    z+=1
if(z==0):
    mycursor.execute("insert into login values('username','password')")
    mydb.commit()
while True:
    print("┌────────────────────•✧•────────────────────┐")
    print("  WELCOME TO SHOPPING MALL MANAGEMENT SYSTEM")
    print("└────────────────────•✧• ───────────────────┘")
    print("Enter 1 for Admin\n"+"Enter 2 for Customer\n"+"Enter 3 to Exit\n")
    ch=int(input("Enter your choice here:"))
    if(ch==1):
        admin()
    elif(ch==2):
        customer()         
    elif(ch==3):
        print("Exiting the system. Goodbye!")
        break
    else:
        print("Invalid choice! Please try again")
