import mysql.connector
mydb=mysql.connector.connect(host='localhost',user="root",passwd="mysql")
mycursor=mydb.cursor()
mycursor.execute("create database if not exists project")
mycursor.execute("use project")
mycursor.execute("create table if not exists login(username varchar(25) not null,password varchar(25) not null)")
mycursor.execute("create table if not exists purchase(name varchar(25) not null,amount int)")
mycursor.execute("create table if not exists stock(pcode int,pname varchar(25),price int)")
mydb.commit()#to save changes

def admin():
    epass=input("Enter password:")
    mycursor.execute("select * from login")
    for i in mycursor:
        username,password=i 
        if(epass==password):
            print("\nPassword verified,Welcome Admin!")
            loop2='y'
            while(loop2=='y' or loop2=='Y'):
                print("\nWhich function would you like to perform?\n1.Adding new item\n2.Updating price\n3.Deleting Item\n4.Displaying all Items\n5.Changing Password\n6.Log out\n")
                ch1=int(input("Admin enter your choice:"))
                if(ch1==1):#adding item
                    loop='y'
                    while(loop=='y' or loop=='Y'):
                        pcode=int(input("Enter product code:"))
                        pname=input("Enter product name:")
                        price=int(input("Enter product price:"))
                        mycursor.execute("insert into stock values('"+str(pcode)+"','"+pname+"','"+str(price)+"')")
                        mydb.commit()
                        print("Record inserted successfully\n")
                        loop=input("Do you want to add another item in this table?(y/n):")
                    loop2=input("Do you want to continue functioning as an admin?(y/n):") 
                    
                elif(ch1==2):#updating item
                    loop='y'
                    while(loop=='y' or loop=='Y'):
                        #code to display all items for ease of selection
                        mycursor.execute("select * from stock")
                        print("LIST OF PRODUCTS")
                        print("pcode||pname||price")
                        for i in mycursor:
                            t_code,t_name,t_price=i
                            print(t_code,"||",t_name,"||",t_price)
                        pcode=int(input("\nEnter code of product you want to change price of:"))
                        new_price=int(input("Enter new price of selected product:"))
                        mycursor.execute("update stock set price='"+str(new_price)+"'where pcode='"+str(pcode)+"'")
                        mydb.commit()
                        loop=input("Do you want to update another item in this table?(y/n):")
                    loop2=input("Do you want to continue functioning as an admin?(y/n)")
                    
                elif(ch1==3):#deleting item
                    loop='y'
                    while(loop=='y' or loop=='Y'):
                        #code to display all items for ease of selection
                        mycursor.execute("select * from stock")
                        print("LIST OF PRODUCTS")
                        print("pcode||pname||price")
                        for i in mycursor:
                            t_code,t_name,t_price=i
                            print(t_code,"||",t_name,"||",t_price)
                        pcode=int(input("enter code of product you want to delete:"))
                        mycursor.execute("delete from stock where pcode='"+str(pcode)+"'")
                        mydb.commit()
                        loop=input("Do you want to delete another item in this table?(y/n):")
                    loop2=input("Do you want to continue functioning as an admin?(y/n):")  
                elif(ch1==4):
                    mycursor.execute("select * from stock")
                    print("LIST OF PRODUCTS")
                    print("pcode||pname||price")
                    for i in mycursor:
                        t_code,t_name,t_price=i
                        print(t_code,"||",t_name,"||",t_price)
                    print()
                elif(ch1==5):
                    old_password=input("Enter old password:")
                    mycursor.execute("select * from login")
                    for j in mycursor:
                        username1,password=j
                    if(old_password==password):
                        print("\nSuccessfully verified")
                        new_password=input("enter new password:")
                        mycursor.execute("update login set password='"+new_password+"'")
                        print("Updated successfully")
                        mydb.commit()
                    else:
                        print("wrong password")
                        print()
                        
                       
                elif(ch1==6):
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
                mycursor.execute("select * from stock")
                print("LIST OF PRODUCTS")
                print("pcode||product name||price")
                for i in mycursor:
                    t_code,t_name,t_price=i
                    print(t_code,"||",t_name,"||",t_price)
                pcode=int(input("Enter product code of item you wish to purchase:"))
                quantity=int(input("Enter quantity of item you wish to purchase:"))
                mycursor.execute("select * from stock where pcode='"+str(pcode)+"'")
                for i in mycursor:#for calculating total amount
                    t_code,t_name,t_price=i
                amount=t_price*quantity
                mycursor.execute("insert into purchase values('"+name+"','"+str(amount)+"')")
                mydb.commit()
                loop2=input("Do you want to continue functioning as a customer?(y/n):")  
                
        elif(ch2==2):#payment
            name=input("\nEnter your name")#database is not case sensitive
            mycursor.execute("select * from purchase where name='"+name+"'")
            for i in mycursor:
                n,a=i
            print("\nHello",n,"!!Amount needed to be paid by you=₹",a,"\n")
            
        elif(ch2==3):
            mycursor.execute("select * from stock")
            print("LIST OF PRODUCTS")
            print("pcode||product name||price")
            for i in mycursor:
                t_code,t_name,t_price=i
                print(t_code,"||",t_name,"||",t_price)
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
        break
    else:
        print("Invalid choice! Please try again")
        
            
        



