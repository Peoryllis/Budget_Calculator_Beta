from Financial_Information import *
from Personal_Information_Calculator import *
from DataListBeta import *
from ShoppingList import *
import tkinter
from tkinter import ttk


root = tkinter.Tk() #initiate the window
root.configure(bg='#89CFF0')
root.title('Budget calculator')
root.geometry('1600x900')

class Budget_Calculator(Frame):
    '''Budget Calculator... calculates your funds'''

    def __init__(self, master):
        '''Budget_Calculator(self, master)
        master: Tkinter.Tk()
        Creates a budget calculator'''
        
        Frame.__init__(self, master, bg='#89CFF0')
        self.pack(fill=BOTH, expand=1)
        self.root = master

        self.maincolor = '#E4F6F8'
        self.focuscolor = '#cee5ed'
        self.resultcolor = '#b5c7d3'
        self.fonttype = ['Candara', 12, 'bold']
        
        self.financialInformation = Financial_Information(self) #have users input the financial information
        self.financialInformation.place(relx=0, rely=0, relwidth=3/12, relheight=1/6)

        self.taxLabel = Label(self, bg='white', text='Sales Tax (%)', font=('Ariel', 10, 'bold')) #have users input the sales tax
        self.taxLabel.place(relx=3/12, rely=0, relwidth=1/12, relheight=1/24)
        self.taxInput = Mutable_Label(self, {'bg':'#E4F6F8', 'text':0, 'font':('Ariel', 10)}, True, '#cee5ed')
        self.taxInput.place(relx=3/12, rely=1/24, relwidth=1/12, relheight=1/24)
        self.taxInput.bind('<Key>', lambda e: self.create_budget(), '+')

        billsCalculator = BillsCalculator(self) #allow users to convert yearly and weekly bills to monthly bills
        billsCalculator.place(relx=4/12, rely=0, relwidth=3/12, relheight=1/12)

        #haave users input their imcome

        self.incomeLabel = Label(self, bg='white', text='Income per month ($)', font=('Ariel', 8, 'bold')) #have users input the sales tax
        self.incomeLabel.place(relx=7/12, rely=0, relwidth=1/12, relheight=1/24)
        self.incomeInput = Mutable_Label(self, {'bg':'#E4F6F8', 'text':0, 'font':('Ariel', 10)}, True, '#cee5ed')
        self.incomeInput.place(relx=7/12, rely=1/24, relwidth=1/12, relheight=1/24)
        self.incomeInput.bind('<Key>', lambda e: self.create_budget(), '+')

        self.portionSetterLabel = Label(
            master = self,
            font = self.fonttype,
            bg = 'white',
            text = '% of savings to spend',
            )
        self.portionSetterLabel.place(relx=8/12, rely=0, relwidth=2/12, relheight=1/24)

        self.portionSet = Mutable_Label(
            master = self,
            kwargs = {
                'bg':self.maincolor,
                'text': 100,
                'font': self.fonttype,
                },
            make_numeric = True,
            focusColor = self.focuscolor
            )
        self.portionSet.place(relx=8/12, rely=1/24, relwidth=2/12, relheight=1/24)
        self.portionSet.bind('<Key>', lambda e: self.create_budget(), '+')

        self.totalCash = Label(self, bg=self.resultcolor, font=self.fonttype, text='Total Cash: $0.00')
        self.totalCash.place(relx=0, rely=1/6, relwidth=3/12, relheight=1/24)

        self.budgetLabel = Label(
            self,
            bg = self.resultcolor,
            font = self.fonttype,
            text = '$0.00 budget'
            )
        self.budgetLabel.place(relx=0, rely=5/24, relheight=1/24, relwidth=3/12)

        self.donationsLabel = Label(
            self,
            bg = self.resultcolor,
            font = self.fonttype,
            text = 'At least a dollar would do for donations'
            )
        self.donationsLabel.place(relx=0, rely=6/24, relheight=1/24, relwidth=3/12)

        self.update()

        self.visual = LabelImage(
            master = self,
            imageURL = 'https://i.pinimg.com/236x/b4/bf/49/b4bf495ba0b4dbde2a9e4ebcc602248b.jpg',
            width = int(self.winfo_width() * (3/12)),
            height = int(self.winfo_height() / 2),
            background = 'green',
            )
        self.visual.place(relx=0, rely=7/24, relwidth=3/12, relheight=1/2)

        visualDescription = Label(
            self,
            bg = 'white',
            font = ['Candara', 12, 'italic', 'bold'],
            text = 'Better smart spending now than later'
            )
        visualDescription.place(relx=0, rely=19/24, relwidth=3/12, relheight=1/24)

        self.billsList = BillsCounter(
            master = self,
            kwargs = {
                'bg': '#ebcfc3',
                'borderwidth': 2,
                'relief': GROOVE,
                },
            )
        self.billsList.place(relx=3/12, rely=2/24, relwidth=9/36, relheight=22/24)

        self.wishList = DesiresList(
            master = self,
            kwargs = {
                'bg': '#ebcfc3',
                'borderwidth': 2,
                'relief': GROOVE,
                },
            )
        self.wishList.place(relx=18/36, rely=2/24, relwidth=9/36, relheight=22/24)

        self.shoppingList = BudgetList(
            master = self,
            kwargs = {
                'bg': '#ebcfc3',
                'borderwidth': 2,
                'relief': GROOVE,
                },
            )
        self.shoppingList.place(relx=27/36, rely=2/24, relwidth=9/36, relheight=22/24)

        self.goalLabel = Label(
            master = self,
            font = ('Candara', 12, 'bold'),
            text = 'How much money I need in the bank to get: ',
            bg = 'white',
            borderwidth=2,
            relief=GROOVE,
            )
        self.goalLabel.place(relx=0, rely=20/24, relwidth = 3/12, relheight = 1/24)

        self.goalVar = StringVar(self)
        self.goalVar.set(self.wishList.get_data()[0][0])
        self.goalVar.trace('w', self.update_wanted_item)

        self.goalSet = ttk.OptionMenu(
            self,
            self.goalVar,
            *self.wishList.get_data()[0],
            )
        self.goalSet.place(relx=0, rely=21/24, relwidth=3/12, relheight=1/24)

        self.goal_input = self.wishList.get_data()[0][0]

        self.currentSelection = self.goalVar.get()

        self.savingsLeft = Label(
            master = self,
            bg = self.resultcolor,
            font = ['Candara', 8],
            text='Select an option from the dropdown above to get started',
            )
        self.savingsLeft.place(relx=0, rely=22/24, relwidth=3/12, relheight=1/24)

        self.incomeLeft = Label(
            master = self,
            bg = self.resultcolor,
            font = ['Candara', 8],
            text='Select an option from the dropdown above to get started'
            )
        self.incomeLeft.place(relx=0, rely=23/24, relwidth=3/12, relheight=1/24,)

                               
        self.totalCurrency = 0

    def update_wanted_item(self, *args):
        self.currentSelection = self.goalVar.get()

        self.update_remaining_value_labels()

    def update_remaining_value_labels(self):
        '''Budget_Calculator.update_remaining_value_labels(self)
        updates the values of how much money you need left to get an item'''

        item = self.currentSelection
        print(item)

        if item in self.wishList.get_data()[0]:
            print(1)
        
            if self.taxInput['text'] == '':
                tax = 0
            elif self.taxInput['text'] == '0':
                tax = 0
            else:
                tax = float(self.taxInput['text']) / 100

            if self.incomeInput['text'] == '':
                income = 0
            else:
                income = float(self.incomeInput['text'])

            if self.portionSet['text'] == '':
                portion = 0
            else:
                portion = float(self.portionSet['text']) / 100
                
            cost = self.wishList.get_data()[1][self.wishList.get_data()[0].index(item)]

            print(tax)


            if self.totalCurrency >= (cost/(1-tax)/portion) - income + sum(self.billsList.get_data()[1]):
                self.incomeLeft['text'] = f'You make enough money each month to get {item}'
                self.savingsLeft['text'] = f'You have enough money to get {item}'
            else:
                self.incomeLeft['text'] = 'You need to make $' + '{:.2f}'.format((cost/(1-tax)/portion) - self.totalCurrency + sum(self.billsList.get_data()[1])) + f' per month to get {item}'
                self.savingsLeft['text'] = 'You need $' + '{:.2f}'.format((cost/(1-tax)/portion) - income + sum(self.billsList.get_data()[1])) + f' to get {item} OR'


    def create_budget(self):
        '''Budget_Calculator.create_budget(self)
        creates your budget'''

        if self.taxInput['text'] == '':
            tax = 0
        else:
            tax = float(self.taxInput['text']) / 100

        if self.incomeInput['text'] == '':
            income = 0
        else:
            income = float(self.incomeInput['text'])

        if self.portionSet['text'] == '':
            portion = 0
        else:
            portion = float(self.portionSet['text']) / 100

        baseCashValue = ((self.totalCurrency + income - sum(self.billsList.get_data()[1])) * portion) * (1 - tax)

        self.budget = round(baseCashValue * (1 - tax), 2)

        if self.budget < 0:
            self.budget == 0
            
        self.budgetLabel['text'] = '${:.2f}'.format(self.budget) + ' budget'
        self.create_donations_budget()
        self.update_remaining_value_labels()

    def update_option_menu(self):
        '''Budget_Calculator.update_option_menu():
        updates the options for the option menu'''

        menu = self.goalSet['menu']
        menu.delete(0, 'end')
        print(menu)
        for entry in self.wishList.get_data()[0]:
            menu.add_command(
                label = entry,
                command = lambda value=entry: self.goalVar.set(value)
                )

    def create_donations_budget(self):
        '''Budget_Calculator.create_donations_budget()
        Creates a specialized budget for donations'''

        if self.budget > 500:
            self.donationsBudget = 0.3 * self.budget
            self.donationsLabel['text'] = 'You should donate at least S' + '{:.2f}'.format(self.donationsBudget)
        else:
            self.donationsBudget = 0
            self.donationsLabel['text'] = 'Try to donate what you have <3'

    def update_total_cash_values(self):
        '''self.update_total_values()
        update the totalCash meter in the calculator'''
        self.totalCash['text'] = 'Total cash: $' + '{:.2f}'.format(self.financialInformation.return_sum_values())
        self.totalCurrency = self.financialInformation.return_sum_values()
        self.create_budget()
    
finalCalc = Budget_Calculator(root)

root.mainloop()
