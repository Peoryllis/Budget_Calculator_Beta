from DataListBeta import *
import random

class BillsCounter(Frame):
    '''BillsCounter obj
    Keeps a data list of your Bills with total cost (monthly) at the top'''

    def __init__(self, master, kwargs={}):
        '''BillsCounter.__init__(master, kwargs)
        master: tkinter.Budget_Calculator()
        kwargs: dict: any valid parameter for tkinter.Frame
        creates BillsCounter'''
        
        self.master = master
        Frame.__init__(self, master, **kwargs)

        self.costWidget = Label(
            master = self,
            bg = self['bg'],
            fg = 'grey',
            text = 'Total amount: $0.00',
            justify = 'left',
            )       
        self.costWidget.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        self.update=()

        self.dataList = DataRecord(
            master = self,
            kwargs = kwargs,
            height = self.winfo_height(),
            title = 'Bills',
            numColumns = 2,
            columnLabels = ['Item', 'Cost per month']
            )
        self.dataList.place(relx=0, rely=0.05, relwidth=1, relheight=(0.95))

        self.dataList.dataList.bind_all('<Control-u>', lambda e: self.master.shoppingList.update())

        self.dataList.bind_all('<Key>', lambda e: [self.find_total_cost(), self.master.update_option_menu()], '+')

        self.totalCost = 0
            
        
            

    def find_total_cost(self):
        '''BillsCounter.find_total_cost()
        upadates the total cost of all the bills'''

        data2 = self.get_data()

        if data2 != None:
            self.costWidget['text'] = 'Total Cost: $' + '{:.2f}'.format(sum(data2[1]))
            self.totalCost = sum(data2[1])
            self.master.create_budget()
        else:
            self.costWidget['text'] = 'Error'

    def get_data(self):
        '''BillsCounter.get_data()
        returns nested lists: Bills and their cost
        returns None if there are any non numeric values for the cost'''

        data = []

        column1Data = self.dataList.get_data(rows = list(range(1, self.dataList.numRows + 1)), columns = [1])
        column2Data = self.dataList.get_numeric_data(rows = list(range(1, self.dataList.numRows + 1)), columns = [2])

        if type(column2Data) is not dict:
            return None

        data.append(column1Data['Item'])

        for key in column2Data:
            data.append(list(float(value) for value in column2Data[key]))

        return data

class DesiresList(BillsCounter):
    '''Makes a list of your desires'''
    def __init__(self, master, kwargs):
        '''DesiresList.__init__(master, kwargs)
        master: tkinter.Budget_Calculator()
        kwargs: dict: any valid parameter for tkinter.frame()'''

        BillsCounter.__init__(self, master, kwargs)

        self.dataList = DataRecord(
            master = self,
            kwargs = kwargs,
            height = self.winfo_height(),
            title = 'Things I want',
            numColumns = 2,
            columnLabels = ['Item', 'Price']
            )
        self.dataList.place(relx=0, rely=0.05, relwidth=1, relheight=(0.95))

class BudgetList(Frame):
    '''Makes a list of the things you want you can afford'''

    def __init__(self, master, kwargs):
        '''BudgetList.__init__(master, kwargs)
        master: tkinter.Budget_Calculator()
        kwargs: dict: any valid parameter for tkinter.frame()'''

        Frame.__init__(self, master, **kwargs)

        self.title = Label(
            self,
            bg = 'white',
            font = (self.master.fonttype[0], 24, 'bold'),
            text = 'In my budget',
            )

        self.title.pack(side = TOP)


        self.goodsList = ScrollingBar(
            master = self,
            color = self['bg'],
            scroll = 'Y',
            )
        self.goodsList.place(relx = 0, rely = 0.1, relwidth=1, relheight=0.9)

        self.itemsLabel = self.goodsList.item(
            Label,
            kwargs = {
                'bg': 'white',
                'font': self.master.fonttype,
                'text': 'Item',
                'width': 14,
                'height': 2,
                'borderwidth':2,
                'relief':RIDGE,
                },
            row = 0,
            column = 0
        )

        self.priceLabel = self.goodsList.item(
            Label,
            kwargs = {
                'bg': 'white',
                'font': self.master.fonttype,
                'text': 'Price',
                'width': 14,
                'height': 2,
                'borderwidth': 2,
                'relief':RIDGE,
                },
            row = 0,
            column = 1
        )

        self.numrows = 1
        self.affordableGoods = {}

    def update(self):
        '''BudgetList.update()
        updates the budgetList on what you can afford'''
        
        data = self.master.wishList.get_data()
        budget = self.master.budget
        reasonableItems = {}
        unreasonableItems = []

        
        for key in self.affordableGoods:
            if float(self.affordableGoods[key][1]['text']) > budget or self.affordableGoods[key][0] not in data[0]:
                for item in self.affordableGoods[key]:
                    item.destroy()
                unreasonableItems.append(key)

        for value in unreasonableItems:
            del self.affordableGoods[value]

        remainingRows = list(self.affordableGoods[value] for value in self.affordableGoods)
        self.affordableGoods = {}
        index = 1

        for value in remainingRows:
            for obj in value:
                obj.grid(row = index)
            self.affordableGoods[data[0][index-1]] = value
            index += 1

        self.numRows = len(self.affordableGoods.keys())


        for index in range(len(data[1])):
            if data[1][index] <= budget:
                item = str(data[0][index])
                number = 1
                
                while item in reasonableItems.keys():
                    number += 1
                    item = str(data[0][index]) + str(number)

                reasonableItems[item] = data[1][index]

        
        for element in reasonableItems:
            if element not in self.affordableGoods.keys():
                self.affordableGoods[element] = [
                    self.goodsList.item(Label, kwargs = {'bg': 'white', 'font': self.master.fonttype, 'text': element,'width':14, 'height':2}, row = self.numrows, column = 0),
                    self.goodsList.item(Label, kwargs = {'bg': 'white', 'font': self.master.fonttype, 'text': reasonableItems[element], 'width':14, 'height':2}, row = self.numrows, column = 1),
                    ]
               
            self.numrows += 1

        succession = 1

        for key in self.affordableGoods:
            for bauble in self.affordableGoods[key]:
                bauble.grid(row = succession)
                
            succession += 1
                
                    
                    
        
