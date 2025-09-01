import tkinter as tk
import pymysql
from tkinter import messagebox

class bill():
    def __init__(self, root):
        self.root = root
        self.root.title("Super Market") 
        scrn_width = self.root.winfo_screenwidth() 
        scrn_height = self.root.winfo_screenheight()
          
        self.root.geometry(f"{scrn_width}x{scrn_height}+0+0")


        mainTitle = tk.Label(self.root, text = "Super Market Billing System", bg = "black", fg = "#FFD700", bd = 5, relief = "groove", font = ("Arial", 40, "bold") )
        mainTitle.pack(side = "top", fill = "x")

        # variable

        self.item_name = tk.StringVar()
        self.item_price = tk.IntVar()
        self.item_quant = tk.IntVar()
        self.total = tk.IntVar()

              # -------input frame
        self.inputFrame = tk.Frame(self.root,bg = "sky blue", bd = 5, relief = "groove")
        self.inputFrame.place(x = 10, y = 90, width = 400, height = 700) 

        item = tk.Label(self.inputFrame, text = "Item Name:", bg = "sky blue",fg = "black",font = ("Aria",20,"bold") )
        item.grid(row = 0, column = 0, padx = 10, pady = 30) 
        self.itemIn = tk.Entry(self.inputFrame, width = 15, bd = 2, font = ("Arial", 15)) 
        self.itemIn.grid( pady = 30, row = 0, column = 1)
                 
        quant = tk.Label(self.inputFrame, text = "Item Quantity:", bg = "sky blue",fg = "black",font = ("Aria",20,"bold") ) 
        quant.grid(row = 1, column = 0, padx = 10, pady = 30)
        self.quantIn = tk.Entry(self.inputFrame, width = 15, bd = 2, font = ("Arial", 15)) 
        self.quantIn.grid( pady = 30, row = 1, column = 1) 
        
        buyBtn = tk.Button(self.inputFrame,  text = "Buy",command = self.purchase, width = 8, bd = 2, relief = "raised", bg = "orange", font = ("Arial", 15, "bold")) 
        buyBtn.grid(row = 2, column = 0, padx = 40, pady = 70) 

        printBillBtn = tk.Button(self.inputFrame, text = "Print Bill",command = self.print_bill, width = 8, bd = 2, relief = "raised", bg = "orange", font = ("Arial", 15, "bold")) 
        printBillBtn.grid(row = 2, column = 1, padx = 30, pady = 70) 

        addBtn = tk.Button(self.inputFrame, text = "Add Item", command = self.add_fun, width = 15, bd = 2, relief = "raised", bg = "orange", font = ("Arial", 15, "bold"))
        addBtn.grid(row = 3, column = 0, padx = 40, columnspan = 2, pady = 30)

        updateBtn = tk.Button(self.inputFrame, text="Update Item", command=self.open_update_window, width=15, bd=2, relief="raised", bg="orange", font=("Arial", 15, "bold"))
        updateBtn.grid(row=4, column=0, columnspan=2, pady=20)


        # detail frame

        self.detailFrame = tk.Frame(self.root, bg="dark gray", bd=5, relief="groove") 
        self.detailFrame.place(x=420, y=90, width=1100, height=700)

        self.list = tk.Listbox(self.detailFrame, bg = "sky blue", font = ("Arial", 15), bd = 3, relief = "sunken", width = 95, height = 27 )
        self.list.grid(row=0, column=0, padx = 10, pady=10)

        
        



    def add_fun(self):
        self.addFrame = tk.Frame(self.root, bg = "light gray" , bd = 5, relief = "groove")
        self.addFrame.place(x = 439, y = 107, width = 460, height = 651)

        itemName = tk.Label(self.addFrame, text = "Item Name:", bg = "light gray",fg = "black",font = ("Aria",20,"bold") )
        itemName.grid(row = 0, column = 0, padx = 10, pady = 30) 
        self.itemNameIn = tk.Entry(self.addFrame, textvariable = self.item_name, width = 15, bd = 2, font = ("Arial", 15)) 
        self.itemNameIn.grid( pady = 30, row = 0, column = 1)

        itemQuant = tk.Label(self.addFrame, text = "Item Quantity:", bg = "light gray",fg = "black",font = ("Aria",20,"bold") )
        itemQuant.grid(row = 1, column = 0, padx = 10, pady = 30) 
        self.itemQuantIn = tk.Entry(self.addFrame, textvariable = self.item_quant, width = 15, bd = 2, font = ("Arial", 15)) 
        self.itemQuantIn.grid( pady = 30, row = 1, column = 1)

        itemPrice = tk.Label(self.addFrame, text = "Item Price:", bg = "light gray",fg = "black",font = ("Aria",20,"bold") )
        itemPrice.grid(row = 2, column = 0, padx = 10, pady = 30) 
        self.itemPriceIn = tk.Entry(self.addFrame, textvariable = self.item_price, width = 15, bd = 2, font = ("Arial", 15)) 
        self.itemPriceIn.grid( pady = 30, row =2, column = 1)

        okayBtn = tk.Button(self.addFrame, command = self.insert_fun, text = "Okay", width = 15, bd = 2, relief = "raised", bg = "sky blue", font = ("Arial", 15, "bold"))
        okayBtn.grid(row = 3, column = 0, padx = 20,  pady = 30)

        closeBtn = tk.Button(self.addFrame, command = self.close, text = "Close", width = 15, bd = 2, relief = "raised", bg = "sky blue", font = ("Arial", 15, "bold"))
        closeBtn.grid(row = 3, column = 1, padx = 20,  pady = 30)

    def insert_fun(self):
        con = pymysql.connect(host = "localhost",  user = "root", passwd = "Dheerajrawat", database = "billdb")
        cur = con.cursor()
        cur.execute("Insert into item values(%s, %s, %s)", (self.item_name.get(), self.item_price.get(), self.item_quant.get()))
        con.commit()
        messagebox.showinfo("Success", "Item Added Successfully")
        con.close()
        self.clear()

    def clear(self):
        self.item_name.set("")
        self.item_price.set("")
        self.item_quant.set("")



    def close(self):
        self.addFrame.destroy()

    def purchase(self):
        item = self.itemIn.get()
        quant = int(self.quantIn.get())

        con = pymysql.connect(host = "localhost",  user = "root", passwd = "Dheerajrawat", database = "billdb")
        cur = con.cursor()
        cur.execute("select item_price, item_quant from item where item_name = %s", item)
        data = cur.fetchone()
        # means if data consists
        if data:
            if data[1] >= quant:
                amount = data[0] * quant
                self.total.set(self.total.get() + amount)

                singleItem = f"Price of {quant} {item} is: {amount}"
                self.list.insert(tk.END, singleItem)
                self.clear_inputframe()
                update = data[1] - quant

                cur.execute("update item set item_quant = %s where item_name = %s", (update, item))
                con.commit()
                con.close()

             

            
            else:
                messagebox.showerror("Error", "Item Quantity does not met the requirement ")
                self.clear_inputframe()



        else:
            messagebox.showerror("Error", "Invalid Item Name!")
            self.clear_inputframe()


    def clear_inputframe(self):
        self.itemIn.delete(0, tk.END)
        self.quantIn.delete(0, tk.END)


    def print_bill(self):
        line = "---------------------------------------"
        self.list.insert(tk.END, line)
        print_bill = f"Your Bill : {self.total.get()}"
        self.list.insert(tk.END, print_bill)

    def update_item(self):
        name = self.updName.get().strip()
        new_price = self.updPrice.get().strip()
        new_quant = self.updQuant.get().strip()

        if name == "" or new_price == "" or new_quant == "":
          messagebox.showerror("Error", "All fields are required")
          return

        try:
          con = pymysql.connect(host="localhost", user="root", passwd="Dheerajrawat", database="billdb")
          cur = con.cursor()

        # First check if item exists
          cur.execute("SELECT * FROM item WHERE item_name = %s", (name,))
          result = cur.fetchone()

          if result is None:
              messagebox.showwarning("Not Found", f"Item '{name}' does not exist in the database")
          else:
              cur.execute("UPDATE item SET item_price=%s, item_quant=%s WHERE item_name=%s", 
                        (new_price, new_quant, name))
              con.commit()
              messagebox.showinfo("Success", f"Item '{name}' updated successfully!")
              
          con.close()

        # Clear input fields
          self.updName.delete(0, tk.END)
          self.updPrice.delete(0, tk.END)
          self.updQuant.delete(0, tk.END)

          self.updateWin.destroy()  # Close popup


        except Exception as e:
          messagebox.showerror("Error", str(e))

    def open_update_window(self):
         # Create new popup window
        self.updateWin = tk.Toplevel(self.root)
        self.updateWin.title("Update Item")
        self.updateWin.geometry("400x300")
        self.updateWin.config(bg="lightyellow")

        # Labels & Entry boxes
        tk.Label(self.updateWin, text="Item Name:", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
        self.updName = tk.Entry(self.updateWin, font=("Arial", 12))
        self.updName.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.updateWin, text="New Price:", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10)
        self.updPrice = tk.Entry(self.updateWin, font=("Arial", 12))
        self.updPrice.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.updateWin, text="New Quantity:", bg="lightyellow", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=10)
        self.updQuant = tk.Entry(self.updateWin, font=("Arial", 12))
        self.updQuant.grid(row=2, column=1, padx=10, pady=10)

        # Update button
        tk.Button(self.updateWin, text="Update", command=self.update_item, width=12, bg="orange", font=("Arial", 12, "bold")).grid(row=3, columnspan=2, pady=20)
        






root = tk.Tk()
obj = bill(root)
root.mainloop()
