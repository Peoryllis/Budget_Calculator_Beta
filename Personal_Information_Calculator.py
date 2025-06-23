import sys
sys.path.append("/Users/anayaahanotu/Documents/Coding/GitHub/Special_tkinter_objects/")
from tkinterPlus2 import *
from datetime import date

from tkinter import *

class BillsCalculator(Frame):
    '''BillsCalculator'''

    def __init__(self, master):
        '''BillsCalculator(master)
        master: Tkinter.Tk or Frame
        Converts weekly bills or yearly bills to monthly bills
        returns None'''
        
        self.master = master

        Frame.__init__(self, master, bg='White', borderwidth=2, relief=RIDGE)

        self.weeklyBillsLabel = Label(self, bg='white', text='Weekly Bills ($)', font = self.master.fonttype)
        self.weeklyBillsLabel.place(relx=0, rely=0, relwidth=1/3, relheight=1/2)
        
        self.weeklyBillsInput = Mutable_Label(self, {'bg':self.master.maincolor, 'font':self.master.fonttype[:2], 'borderwidth':1, 'relief':GROOVE, 'text':0.00}, True, self.master.focuscolor)
        self.weeklyBillsInput.place(relx=0, rely=1/2, relwidth=1/3, relheight=1/2)
        self.weeklyBillsInput.bind('<Return>', lambda e: self.calculate('weekly'))

        self.yearlyBillsLabel = Label(self, bg='white', text='Yearly Bills ($)', font = self.master.fonttype)
        self.yearlyBillsLabel.place(relx=1/3, rely=0, relwidth=1/3, relheight=1/2)
        
        self.yearlyBillsInput = Mutable_Label(self, {'bg':self.master.maincolor, 'font':self.master.fonttype[:2], 'borderwidth':1, 'relief':GROOVE}, True, self.master.focuscolor)
        self.yearlyBillsInput.place(relx=1/3, rely=1/2, relwidth=1/3, relheight=1/2)
        self.yearlyBillsInput.bind('<Return>', lambda e: self.calculate('yearly'))

        self.ResutLabel = Label(self, bg='white', text='Result', font = self.master.fonttype)
        self.ResutLabel.place(relx=2/3, rely=0, relwidth=1/3, relheight=1/2)
        self.output = Label(self, bg=self.master.resultcolor, text='', font = self.master.fonttype[:2])
        self.output.place(relx=2/3, rely=1/2, relwidth=1/3, relheight=1/2)


    def calculate(self, interval):
        '''BillsCalulator.calculate(interval)
        interval: 'weekly' or 'yearly'
        converts weekly or yearly payments to monthly payments
        outputed in the output label
        return None'''

        if interval == 'weekly':
            self.output['text'] = '$' + '{:.2f}'.format(float(self.weeklyBillsInput['text']) * 4)
        elif interval == 'yearly':
            self.output['text'] = '$' + '{:.2f}'.format(round(float(self.yearlyBillsInput['text']) / 12, 2))
