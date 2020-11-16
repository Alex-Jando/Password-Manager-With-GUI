from tkinter import *

from cryptography.fernet import Fernet

import sqlite3

import random

passwordLabels = list()


#Dealing with Databases

def connectToDatabase():
	global conn
	global c

	try:
		with open("passwords.db", "rb") as f:
			temp = f.read()
			conn = sqlite3.connect("passwords.db")
			print("Connected To Database")

	except:

		print("Creating Database ...")
		conn = sqlite3.connect("passwords.db")
		print("Connected To Database")

	c = conn.cursor()

	try:
		c.execute("CREATE TABLE passwords (account, password)")

		conn.commit()

	except:
		pass

def getPasswords():

	passwords = list()
	accounts = list()

	c.execute("SELECT * FROM passwords")

	stuff = c.fetchall()

	for x in stuff:

		accounts.append(x[0])
		passwords.append(key.decrypt(eval(x[1])).decode())

	return accounts, passwords

#Encryption

#Getting Key
with open("key.txt", "rb") as i:

	key = Fernet(i.read())

	with open("password.txt", "rb") as j:

		masterPassword = key.decrypt(j.read()).decode()

#Encryption


class passMainMasterPasswordEntry:

	def __init__(self, root):
		self.root = root
		self.root.title("Enter The Master Password")
		self.root.configure(bg="white")
		self.root.geometry("450x225")
		self.root.resizable(width="false", height="false")
		self.root.bind("<Return>", lambda event: self.mainPassSubmit())
		print("The window has opened successfully")

	def defVisualsStartScreen(self):
		self.text = Label(self.root, text="Enter The Master Password Please:", fg="green", bg="White", font=("Microsoft Sans Serif", 20))
		self.mainPassEntry = Entry(self.root, fg="green", bg="white", border=3, font=("Microsoft Sans Serif", 15))
		self.mainPassEntryButton = Button(self.root, fg="green", bg="white", border=3, text="Enter", font=("Microsoft Sans Serif", 15), command = self.mainPassSubmit)
		print("Visuals have been created")

	def createVisualsStartScreen(self):
		self.text.grid(row=0, column=0, pady=15)
		self.mainPassEntry.grid(row=1, column=0, pady=15)
		self.mainPassEntryButton.grid(row=2, column=0, pady=15)
		print("Visuals have been displayed")

	def mainPassSubmit(self):

		self.submittedPassword = self.mainPassEntry.get()

		self.mainPassEntry.delete(0, END)

		if self.submittedPassword == masterPassword:

			self.items = [self.text, self.mainPassEntry, self.mainPassEntryButton]

			for x in self.items:
				x.grid_forget()

			passMainPasswordsScreen(self.root)

class passMainPasswordsScreen:

	def __init__(self, root):

		self.root = root
		self.root.title("LogMeIn")
		self.root.configure(bg="white")
		self.root.geometry("240x450")
		self.root.resizable(width="true", height="true")

		self.menubar = Menu(self.root)
		self.passwordCommands = Menu(self.menubar, tearoff=0)
		self.passwordCommands.add_command(label="Add Password", command=self.makeAddPasswordWindow)
		self.passwordCommands.add_command(label="Delete Password", command=self.makeDeletePasswordWindow)
		self.passwordCommands.add_command(label="Change Master Password Password", command=self.makeChangeMasterPasswordWindow)

		self.menubar.add_cascade(menu=self.passwordCommands, label="Commands")
		self.menubar.add_command(label="Generate Password", command=self.copyAPasswordToClipboard)
		self.menubar.add_command(label="Exit", command=self.root.destroy)
		
		self.root.config(menu=self.menubar)

		print("The password window has opened successfully")
		self.defineVisualsMaster()
		self.createVisualsMaster()
		connectToDatabase()
		self.listPasswords()

	def copyAPasswordToClipboard(self):

		self.root.clipboard_clear()

		self.chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '$', '%', '&', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

		random.shuffle(self.chars)

		for i in range(11):
			self.root.clipboard_append(self.chars[i])

	def listPasswords(self):

		for widget in self.masterFrame.winfo_children():
			widget.destroy()

		self.accounts, self.passwords = getPasswords()

		for x in range(len(self.accounts)):
			self.accountLabel = Label(self.masterFrame, text=f"{str(self.accounts[x])}", fg="green", bg="white", font=("Microsoft Sans Serif", 15), pady=5, padx=5).grid(row=x, column=0)
			self.passwordLabel = Label(self.masterFrame, text=f"{str(self.passwords[x])}", fg="green", bg="white", font=("Microsoft Sans Serif", 15), pady=5, padx=5).grid(row=x, column=1)

	def addAccountPassword(self, account, password):

		stuff = (f'{account}', f'{key.encrypt(password.encode())}', )

		self.addPasswordEntry.delete(0, END)
		self.addAccountEntry.delete(0, END)		

		c.execute("INSERT INTO passwords VALUES (?, ?)", stuff)

		conn.commit()

		self.listPasswords()

	def makeChangeMasterPasswordWindow(self):

		self.changeMasterPasswordWindow = Toplevel()

		self.newMasterPasswordEntry = Entry(self.changeMasterPasswordWindow, fg="green", bg="white", border=3, font=("Microsoft Sans Serif", 15))
		self.changeMasterPasswordButton = Button(self.changeMasterPasswordWindow, text="Change Master Password", fg="green", bg="white", border=3, font=("Microsoft Sans Serif", 15), command=self.changeMasterPassword)

		self.newMasterPasswordEntry.grid(row=0, column=0)
		self.changeMasterPasswordButton.grid(row=1, column=0)

	def changeMasterPassword(self):

		self.newMasterPassword = self.newMasterPasswordEntry.get()
		self.newMasterPasswordEntry.delete(0, END)

		self.newMasterPasswordEncrypted = key.encrypt(self.newMasterPassword.encode())
		with open("password.txt", "wb") as f:
			f.write(self.newMasterPasswordEncrypted)

	def deleteAccountPassword(self, accountName):

		account = (f'{accountName}', )

		self.deleteAccountPasswordEntry.delete(0, END)
		
		c.execute("DELETE FROM passwords WHERE account=?", account)

		conn.commit()

		self.listPasswords()

	def defineVisualsMaster(self):

		self.masterFrame = Frame(self.root, bg="white", border=3)

	def makeAddPasswordWindow(self):

		self.addPasswordWindow = Toplevel()

		self.addPasswordWindow.configure(bg="white")
		self.addPasswordWindow.title("Add A Password")
		self.icon = PhotoImage(file = 'LogMeIn.png')
		self.addPasswordWindow.iconphoto(False, self.icon)

		self.addAccountEntry = Entry(self.addPasswordWindow, fg="green", bg="white", border=3, font=("Microsoft Sans Serif", 15))
		self.addPasswordEntry = Entry(self.addPasswordWindow, fg="green", bg="white", border=3, font=("Microsoft Sans Serif", 15))
		self.addAccountPasswordButton = Button(self.addPasswordWindow, text="Add New Account And Password", fg="green", bg="white", border=3, font=("Microsoft Sans Serif", 15), command = lambda: self.addAccountPassword(self.addAccountEntry.get(), self.addPasswordEntry.get()))

		self.addAccountEntry.grid(row=0, column=0, padx=5)
		self.addPasswordEntry.grid(row=0, column=1, padx=5)
		self.addAccountPasswordButton.grid(columnspan=2, row=1, column=0, pady=10)

	def makeDeletePasswordWindow(self):

		self.deletePasswordWindow = Toplevel()

		self.deletePasswordWindow.configure(bg="white")
		self.deletePasswordWindow.title("Delete A Password")
		self.icon = PhotoImage(file = 'LogMeIn.png')
		self.deletePasswordWindow.iconphoto(False, self.icon)

		self.deleteAccountPasswordEntry = Entry(self.deletePasswordWindow, fg="green", bg="white", border=3, font=("Microsoft Sans Serif", 15))
		self.deleteAccountPasswordButton = Button(self.deletePasswordWindow, text="Delete Account", fg="green", bg="white", border=3, font=("Microsoft Sans Serif", 15), command = lambda: self.deleteAccountPassword(self.deleteAccountPasswordEntry.get()))

		self.deleteAccountPasswordEntry.grid(row=0, column=0, pady=5)
		self.deleteAccountPasswordButton.grid(row=1, column=0)

	def createVisualsMaster(self):

		self.masterFrame.grid(row=0, column=0)







root = Tk()
root.iconphoto(False, PhotoImage(file = 'LogMeIn.png'))
passMainStartScreen = passMainMasterPasswordEntry(root)
passMainStartScreen.defVisualsStartScreen()
passMainStartScreen.createVisualsStartScreen()

root.mainloop()