import sys
sys.path.insert(1, 'E:/')
from tkinterPlus import *
import time


class DataRecord(Frame):
    '''Organize the user's data'''

    def __init__(self, master, kwargs={}, height=300, title='Data', numColumns=1, columnLabels=[]):
        '''DataRecord(self, master, kwargs)
        master: tkinter.Tk or tkinter.Frame
        kwargs: dict: any valid parameter for tkinter.Frame
        height: int: the height you want the frame to be
        title: title for this datalist
        numColumns: int: how many columns will this Data Record have
        columnLabels: have a label for each column
        makes a Data Record:
        user keeps a record of their own data'''

        self.master = master

        width = 140 + (150 * int(numColumns))
        
        Frame.__init__(self, master, **kwargs)

        self.pack()

        self.update()

        self.numColumns = numColumns

        self.titleLabel = Label(self, bg='white', text=title, font=('Calibri', 24, 'bold'))
        self.titleLabel.place(relx=0.5, rely=0.005, anchor='n')

        self.xAddedInput = Mutable_Label(self,\
                                         kwargs={'bg':'white', 'font':('Calibri', 18), 'width':14, 'height':1, 'relief':GROOVE},\
                                         make_numeric=True)
        self.xAddedInput.place(relx=0.5, rely=0.13, anchor='n')
        self.update_idletasks()

        self.addRowButton = Button(
            self, bg='white',\
            text='Add rows',\
            font=('Calibri', 8, 'bold'),\
            command=lambda: [self.add_rows(self.xAddedInput['text']), self.xAddedInput.configure(text='')]
            )
        
        self.addRowButton.place(relx=0, rely=0.13, relwidth=0.2, height=self.xAddedInput.winfo_height(),)

        self.removeRowButton = Button(self, bg='white', text='Strip rows', font=('Calibri', 8, 'bold'), command=lambda: self.remove_rows())
        self.removeRowButton.place(relx=0.8, relwidth=0.2, rely=0.13, height=self.xAddedInput.winfo_height())

        if numColumns > len(columnLabels):
            for add in rDataange(numColumns - len(columnLabels)) :
                columnLabels.append('')

        self.columnLabels = columnLabels

        self.columnLabelObj = {}
                        
        self.dataLog = {}
        self.numColumns=numColumns

        self.dataList = ScrollingBar(self, color=self['bg'], scroll='XY')
        self.dataList.place(rely=0.25, x=0, relwidth=1, relheight = 0.75)

        self.placeholderLabel = self.dataList.item(
            Label,
            kwargs = {
                'bg':'white',
                'text':'X',
                'font':('Calibri', 12, 'bold'),
                'borderwidth':2,
                'relief':RIDGE,
                'width':5,
                'height':1,
                },
            row=0,
            column=0
            )

        self.update()

        Cgrid = 1

        for label in self.columnLabels:
            dictKey = label
            
            if label in self.columnLabelObj.keys():
                num = 1

                while f'label{num}' in self.columnLabelObj.keys():
                    num += 1

                dictKey = f'label{num}'

            self.columnLabelObj[dictKey] = self.dataList.item(
                Label,
                kwargs = {
                    'bg':'white',
                    'text':label,
                    'font':('Calibri', 12),
                    'borderwidth':2,
                    'relief':RIDGE,
                    'width':13,
                    'height':1
                    },
                row = 0,
                column = Cgrid
                )
            
            Cgrid += 1
            
        self.bind_all(
            '<Control-BackSpace>',
            lambda e: self.erase(), '+')

        self.numRows = 0
        self.add_rows(numrows=1)
        self.bind('<Button>', lambda e: self.focus_set())


    def add_rows(self, numrows):
        '''DataRecord.add_rows(self, numrows)
        numrows: int: how many rows should be added at once
        adds x number of rows to the datalist'''

        if numrows == '':
            numrows = 1
        else:
            numrows = int(numrows)

        for row in range(numrows):

            if len(self.dataLog.keys()) == 0:
                entryNum = 1
                self.dataLog[1] = []
            else:
                entryNum = max(self.dataLog.keys()) + 1
                self.dataLog[entryNum] = []

            self.dataLog[entryNum].append(
                self.dataList.item(
                    obj=Label,
                    kwargs={
                        'bg':'white',
                        'font':('Calibri', 12),
                        'height':1,
                        'width':5,
                        'borderwidth':2,
                        'relief': GROOVE,
                        'text':entryNum},
                    row=self.numRows + 1, column=0)
                )

            for item in range(self.numColumns):
                self.dataLog[entryNum].append(
                    self.dataList.item(
                        obj=Mutable_Label,
                        kwargs={
                            'kwargs':{
                                'bg':'white',
                                'font':('Calibri', 12),
                                'width':13,
                                'height':1,
                                'borderwidth':2,
                                'relief': GROOVE}
                            },\
                        row=self.numRows + 1,\
                        column=item + 1)
                    )
                
            self.numRows += 1

    def remove_rows(self):
        '''DataRecord.remove_rows(self)
        creates prompt to remove certain rows and removes them according to the user's wishes'''

        def remove_rows(entryText, root):
            selectedRows = []

            currentValue = ''

            for index in range(len(entryText) + 1):
                if index < len(entryText):
                    character = entryText[index]
                
                if not any((character.isdigit(), character == ',', character == '-', character == ' ')):
                    print(f'ERROR: Operation can not be done. Invalid character in input: "{character}".')
                    
                    warningLabel = Label(
                        master = root,
                        bg = 'red',
                        font = ('Ariel', 16, 'bold'),
                        text = f'ERROR: Operation can not be done. Invalid character in input: "{character}".',
                        wraplength=250
                        )
                    warningLabel.place(
                        relx=0.5,
                        rely=0.5,
                        anchor = 'center'
                        )

                    root.update()
                    time.sleep(3.5)
                    warningLabel.destroy()
                    
                    return ['OPERATION CANNOT BE DONE', character]
                elif character == ',' or index == len(entryText):
                    if '-' in currentValue:
                        currentValue = currentValue.replace('-', ' ', 1)
                        selectedRows.extend(range(*list(int(value) for value in currentValue.split())))
                        selectedRows.append(selectedRows[-1] + 1)
                    else:
                        selectedRows.append(int(currentValue))
                        
                    currentValue = ''
                elif character != ' ':
                    currentValue += character

            selectedRows = tuple(value for value in selectedRows if all((value <= len(self.dataLog.keys()), value > 0)))

            for value in selectedRows:
                for obj in self.dataLog[value]:
                    obj.destroy()
                    self.numRows -= 1

            for value in selectedRows:
                del self.dataLog[value]

            remainingRows = list(self.dataLog[value] for value in self.dataLog)
            self.dataLog = {}
            index = 1

            for value in remainingRows:
                value[0].configure(text=index)
                for obj in value:
                    obj.grid(row=index)
                self.dataLog[index] = value

                index += 1

            self.numRows = len(self.dataLog.keys())

            root.destroy()
    


        rowSelectWidget = Frame(
            master = self.master.master,
            bg = 'white',
            borderwidth = 2,
            width = 500,
            height = 500,
            relief = SUNKEN
            )
        rowSelectWidget.place(
            relx=0.5,
            rely=0.5,
            anchor = 'center',
            )

        titleLabel = Label(
            master = rowSelectWidget,
            bg = 'white',
            font = ('Calibri', 18, 'bold'),
            text = f'''Remove Rows for "{self.titleLabel['text']}"'''
            )
        titleLabel.place(
            relx = 0,
            rely = 0,
            relwidth = 1,
            relheight = 0.2
            )

        descriptionLabel = Label(
            master = rowSelectWidget,
            bg = 'white',
            font = ('Calibri', 10),
            text = 'Put in the row numbers and/or row ranges you want deleted. Seperate by comma.\nTo add a range, input: <number1> + "-" + <number2>. Ex: "5-7".',
            wraplength = 250,
            justify = LEFT
            )
        descriptionLabel.place(
            relx = 0,
            rely = 0.2,
            relwidth = 1,
            relheight = 0.3
            )

        entryBox = Entry(
            master = rowSelectWidget,
            bg = 'light gray'
            )
        entryBox.place(
            relx=0,
            rely=0.5,
            relwidth=1
            )

        doneButton = Button(
            master = rowSelectWidget,
            bg = '#74B72E',
            font = ('Calibri', 10, 'bold'),
            text = 'Done',
            command = lambda: remove_rows(entryBox.get(), rowSelectWidget),
            )
        doneButton.place(
            relx = 0.8,
            rely = 0.9,
            relwidth = 0.2,
            relheight = 0.1
            )

        cancelButton = Button(
            master = rowSelectWidget,
            bg = '#d3d3d3',
            font = doneButton['font'],
            text = 'Cancel',
            command = rowSelectWidget.destroy
            )        
        cancelButton.place(
            relx = 0,
            rely = 0.9,
            relwidth = 0.2,
            relheight = 0.1)
        

    def get_data(self, rows, columns):
        '''DataRecord.get_data(self, rows, columns)
        rows: seq: row number(s) that should get data extracted
        columns: seq: column numbers that should get data extracted
        returns dict: {column number: row data...} in order'''

        output = {}

        for row in rows:

            if row in self.dataLog.keys():
                objs = tuple(self.dataLog[row])

                for column in columns:

                    if column in range(1, len(objs) + 1):
                        if self.columnLabels[column - 1] in output:
                            output[self.columnLabels[column - 1]].append(objs[column]['text'])
                        else:
                            output[self.columnLabels[column - 1]] = [objs[column]['text']] 

        return(output)

    def get_numeric_data(self, rows, columns):
        '''DataRecord.get_numeric_data(self, rows, columns)
        rows: int: row number(s) that should get data extracted
        columns: int: column numbers that should get data extracted
        returns dict: {column number: row data...} in order
        returns str: 'non numeric value found' if non numeric values are present in the dataset'''

        output = {}

        for row in rows:

            if row in self.dataLog.keys():
                objs = tuple(self.dataLog[row])

            for column in columns:

                if column in range(1, len(objs) + 1):
                    if self.columnLabels[column - 1] in output:
                        if objs[column]['text'].replace('.', '', 1).replace('-', '', 1).isnumeric():
                            output[self.columnLabels[column - 1]].append(objs[column]['text'])
                            
                        elif objs[column]['text'] == '':
                            output[self.columnLabels[column - 1]].append(0)
                            
                        else:
                            return 'Non numeric value found'
                    else:
                        if objs[column]['text'].replace('.', '', 1).replace('-', '', 1).isnumeric():
                            output[self.columnLabels[column - 1]] = [objs[column]['text']]
                        elif objs[column]['text'] == '':
                            output[self.columnLabels[column - 1]] = [0]
                        else:
                            return 'Non numeric value found'
                            

        return(output)

    def erase(self):
        '''DataRecord.erase()
        erases all data in the data list.
        Activated by Control-BackSpace when DataRecord is in focus'''

        for key in self.dataLog:
           for value in self.dataLog[key]:
               if self.dataLog[key].index(value) != 0:
                   value['text'] = ''

