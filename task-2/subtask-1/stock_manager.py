
import sys
def printContent(stockDict):
    for id,(items , quantity) in enumerate(stockDict.items(),start=1):   #enumerate to give us the key-value in pairs 
        print(f"{id}.{items}:{quantity}")

def addStock():
    printContent(stockDict) 
    takeInput=input("Enter the name or the ID for exicting stock [to change it] or to add new one:")

    keys=list(stockDict.keys())   #list of keys only 
    if takeInput.isdigit():
        id = int(takeInput)-1
        if 0<=id <len(keys):
           stockName=keys[id]
        else:
            print("INVALID ID SELECTION")
            return
    else:
        stockName= takeInput.lower()
    try:
        stockQuant=int(input("Enter how much you want to add to the Stock:"))
    except ValueError:
        print("Invalid quantity")
        return

    if stockName in stockDict:
        stockDict[stockName]+=stockQuant
    else:
        stockDict[stockName]=stockQuant

   # printContent(stockDict)

def removeStock():
    printContent(stockDict)
    
    takeInput=input("Enter the name or the ID for exicting stock [to remove it]:")
    
    key=list(stockDict.keys())  
    if takeInput.isdigit():
        id = int(takeInput)-1
        if 0<=id <len(key):
           stockName=key[id]
        else:
            print("INVALID ID SELECTION")
            return
    else:
        stockName= takeInput.lower()
   
    if stockName not in stockDict:
        print(f"{stockName} not found in stock")
        return
    
    try:
        stockQuant=int(input("Enter how much you want to remove from the Stock:"))
    except ValueError:
        print("Invalid quantity")
        return


    if stockQuant>stockDict[stockName]:   # check is <0 
      print("Error:Quantity can't be less than zero ")
      return
    else:
       stockDict[stockName]-=stockQuant 
     
    printContent(stockDict)


stockDict={}
try:
    with open("stock.txt","r") as file:
        content=file.read().split()   #like tokenization in c
        for item in content:
            if ',' in item:    
             items,quantity=item.split(',')
             stockDict[items]=int(quantity)
    
except FileNotFoundError:
    print("File Not Found")

while True:
    choise=input("Enter 1 to add stock\nEnter 2 to remove stock\nEnter 3 to show stock's contents\nEnter 4 to exit program\n")

    if choise=='1':
        addStock()
    elif choise=='2':
        removeStock()
    elif choise =='3':
       printContent(stockDict)
    elif choise =='4':
        with open("stock.txt", "w") as file:  #update stock file 
         for item, quantity in stockDict.items():
            file.write(f"{item},{quantity}\n")
        sys.exit()  
    else :
        print("INVALID INPUT")

