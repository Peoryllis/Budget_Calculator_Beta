import sys

sys.path.insert(0, "GitHub/Special_tkinter_objects")

from Special_tkinter_objects import tkinterPlus2 as tk2

from tkinter import *
import time

class Financial_Information(Frame):
    '''Financial Information, the user inputs their financial information + bills'''

    def __init__(self, master):
        '''Financial Information(self)
        master: tkinter.Tk()
        initiantes the calculator'''

        Frame.__init__(self, master, bg='white')

        self.master = master

        self.title = Label(self, text='Banking info', bg='white', font=('Ariel', 12, 'bold'), anchor='e')
        self.title.place(relx=0, rely=0, relheight=0.2)

        self.addBankButton = Button(self, text='Add Bank', bg='white', relief=GROOVE, borderwidth=3, font=('Ariel', 8), command=self.add_bank_info)
        self.addBankButton.place(relx=0.6, rely=0, relwidth=0.2, relheight=0.2)

        self.removeBankButton = Button(self, text='Remove Bank', bg='white', relief=GROOVE, borderwidth=3, font=('Ariel', 8), command=self.remove_bank)
        self.removeBankButton.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.2)

        self.banklist = tk2.ScrollingBar(self, '#CCDCEC', scroll='x')
        self.banklist.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

        self.banklist.item(Label, kwargs={'bg':'white', 'text':'Cash', 'width':14, 'height':2, 'font':('Ariel', 12)}, row=0, column=0) #keep visual tracks of all the banks

        self.cashInput = self.banklist.item(tk2.Mutable_Label,({'bg':'#E4F6F8', 'width':14, 'height':2, 'font':('Ariel', 12), 'borderwidth':1, 'relief':GROOVE}, True, '#cee5ed'), row=1, column=0)
        
        self.cashInput.bind('<Key>', lambda e: self.edit_values('CASH'), '+')

        self.bankinginfo = {} #keep track of all the banks
        self.values = {'CASH':0} #keep track of how much money is in each bank
        self.numbanks = 0

    def add_bank_info(self):
        '''Financial_information.add_bank_info()
        makes a pop-up for someone to add their bank info'''

        def add_bank(bank):
            '''add_bank
            bank: str: bank name
            Adds bank to system
            returns None'''

            if bank in self.bankinginfo.keys(): #check if the bank already exists
                warningLabel = Label(popup, bg='red', text='This bank already exists')
                warningLabel.grid(row=4, column=0)
                self.update()
                time.sleep(1.5)
                warningLabel.destroy()
                return None
#add the bank to the system

            
            self.bankinginfo[bank] = [self.banklist.item(Label,\
                                                         kwargs={'bg':'white', 'text':bank, 'width':14, 'height':2, 'font':('Ariel', 12)},
                                                         row=0, column=len(self.bankinginfo.keys()) + 1),\
                                      self.banklist.item(tk2.Mutable_Label,\
                                                         ({'bg':'#E4F6F8', 'width':14, 'height':2, 'font':('Ariel', 12), 'borderwidth':1, 'relief':GROOVE, 'text':0}, True, '#cee5ed'),\
                                                         row=1, column=len(self.bankinginfo.keys()) + 1)] #add the banks to the scrolling bar so users can input the amount of money in their bank account
            self.numbanks += 1

            print(len(self.bankinginfo.keys()))
            
            self.bankinginfo[bank][1].bind('<Key>', lambda e, b=bank: self.edit_values(b), '+') #store the cash value of the bank in the system
            self.edit_values(bank)
            
        popup = Frame(self.master, bg='#79a5c6', relief=RIDGE, borderwidth=3) #allows people to add a bank
        popup.place(relx=0.5, rely=0.5, anchor=CENTER)

        title = Label(popup, bg=popup['bg'], text='Add Bank', font=('Ariel', 12, 'bold'))
        title.grid(row=0, column=0, padx=2)

        label = Label (popup, bg=popup['bg'], text='Bank name') #Tells people what to input
        label.grid(row=1, column=0, pady=2, padx=2)

        bankLabel = tk2.Mutable_Label(popup,{'bg':'#749cbc', 'width':20, 'height':1}) #allows people to input a bank
        bankLabel.bind('<Return>',lambda e:[add_bank(bankLabel['text']), bankLabel.configure(text='')])
        bankLabel.grid(row=2, column=0, pady=2, padx=2)

        doneButton = Button(popup, bg=popup['bg'], text='Done', relief=GROOVE, borderwidth=4, font=('Ariel', 10, 'bold'),\
                            command=lambda:[add_bank(bankLabel['text']), bankLabel.configure(text='')])
        doneButton.grid(row=3, column=0, pady=2, padx=2, sticky='w')

        exitButton = Button(popup, bg=popup['bg'], text='Exit', relief=GROOVE, borderwidth=2, command=lambda:popup.destroy())
        exitButton.grid(row=3, column=0, pady=2, sticky='e')

    def remove_bank(self):
        '''remove_bank
        removes banks of the user's choosing
        returns none'''

        def selected_bank(index, ref):
            '''selected_bank
            bank: str: bank
            selects or unselects the bank
            return None'''

            entry = ref[list(ref.keys())[index]]
            
            if entry[1] == True: #highlight the selected banks
                entry[0]['relief'] = RAISED
                entry[1] = False
            else:
                entry[0]['relief'] = SUNKEN
                entry[1] = True

        def remove_banks(banks):
            '''remove_banks
            removes all selected banks
            selects or unselects the bank
            return None'''
            for bank in selectlabels: #remove all selected banks from the scrollingbar AND system
                if selectlabels[bank][1] == True:
                    self.bankinginfo[bank][0].destroy()
                    self.bankinginfo[bank][1].destroy()
                    del self.bankinginfo[bank]
                    del self.values[bank]
                    self.master.update_total_cash_values()
                    self.numbanks -=1


            for key in self.bankinginfo:
                index = list(self.bankinginfo.keys()).index(key)

                for item in self.bankinginfo[key]:
                    item.grid(column=index + 1)
                

        selectlabels = {}

        popup = Frame(self.master, bg='#79a5c6', relief=RIDGE, borderwidth=3) #allows people to remove a bank
        popup.place(relx=0.5, rely=0.5, anchor=CENTER)

        title = Label(popup, bg=popup['bg'], text='Remove Banks', font=('Ariel', 12, 'bold'))
        title.grid(row=0, column=0, padx=2)

        label = Label (popup, bg=popup['bg'], text='Select Banks') #Tells people what to input
        label.grid(row=1, column=0, pady=2, padx=2)

        labelselect = tk2.ScrollingBar(popup, '#749cbc', width=150, height=1200/9) #homes the selectable banks
        labelselect.grid(row=2, column=0, pady=2, padx=2)

        rownum = 0 #for placing the banks using grid()

        for key in self.bankinginfo:

            obj = labelselect.item(Label, kwargs={'bg':'#9dd9f3', 'text':key, 'width':int(labelselect.get_width()), 'anchor':'w', 'relief':RAISED, 'borderwidth':2}, row=rownum, column=0) #put the label on the scrollingbar           
            selectlabels[key] =  [obj, False] #keep track of the object and whether or not it has to be selected
            rownum += 1 #keep the labels in the grid

        for index in range(len(list(selectlabels.keys()))): #bind the labels as a button so the user can select it
            key = list(selectlabels.keys())[index] #for a cleaner line
            selectlabels[key][0].bind('<Button>', lambda e, i=index: selected_bank(i,selectlabels))
            
        doneButton = Button(popup, bg=popup['bg'], text='Done', relief=GROOVE, borderwidth=4, font=('Ariel', 10, 'bold'), command=lambda:[remove_banks(selectlabels), popup.destroy()])
        doneButton.grid(row=3, column=0, pady=2, padx=2, sticky='w')

        cancelButton = Button(popup, bg=popup['bg'], text='Cancel', relief=GROOVE, borderwidth=2, command=lambda:popup.destroy())
        cancelButton.grid(row=3, column=0, pady=2, sticky='e')
            

        

    def edit_values(self, bank):
        '''self.edit_values(bank)
        bank: any key in self.values
        edits the amount of money stored in the bank'''

        if bank == 'CASH': #update how much cash the user has
            if self.cashInput['text'] == '':
                self.values[bank] = 0
                self.master.update_total_cash_values()
                return None
            
            self.values[bank] = float(self.cashInput['text'])
            self.master.update_total_cash_values()
            return None

        if self.bankinginfo[bank][1]['text'] == '': #update the value of the bank in the system
            self.values[bank] = 0
            self.master.update_total_cash_values()
            return None

        self.values[bank] = float(self.bankinginfo[bank][1]['text'])

        self.master.update_total_cash_values()

    def return_sum_values(self):
        '''self.return_sum_values()
        returns the total amount of money the user has
        returns int or float'''
        return sum(list(self.values[bank] for bank in self.values))

    def return_individual_bank_values(self):
        '''self.return_sum_values()
        returns the amount of money in each bank
        returns dict'''
        return self.values


