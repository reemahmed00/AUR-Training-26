from enum import Enum
from abc import ABC,abstractmethod

class Item_status(Enum):
    AVAILABLE =  "AVAILABLE"
    CHECK_OUT = "CHECK_OUT"
    LOST="LOST"

class Library_Item(ABC):
    def __init__(self,title:str,status:Item_status=Item_status.AVAILABLE):
        self.title=title
        self._status=status # the '_' its a private attribute 
        #super().__init__()

    @classmethod
    def from_dict(cls,data:dict):
        return cls(**data)   #unpack dict to populate the instance attribute of the class
    
    @property
    def status(self)->Item_status: #getter so read only 
        return self._status
    
    @abstractmethod
    def get_loanPeriod(self)->int:
        pass

    def checkout(self)->None:
        if self._status==Item_status.CHECK_OUT:
            raise ValueError(f"{self.title} is already checked out.")
        if self._status==Item_status.LOST:
            raise ValueError(f"{self.title} is lost and can't be checked out.")
        self._status=Item_status.CHECK_OUT

    def return_item(self)->None:
        self._status=Item_status.AVAILABLE

    def mark_lost(self)->None:
        self._status=Item_status.LOST

    #implement __lt__ to sort by title
    def __lt__(self, other:"Library_Item")->bool:
        if not isinstance(other,Library_Item):
            return NotImplemented
        return self.title.lower<other.title.lower  #lower to decrease error probability
    #__repr__
    def __repr__(self)->str:
        return f"{self.__class__.__name__}(title={self.title},status={self._status})"
    #__str__
    def __str__(self)->str:
        return f"{self.title} ({self.__class__.__name__}) - {self._status.value}"


class Book(Library_Item):
    def __init__(self, title,auther:str,isbn:str, status = Item_status.AVAILABLE):
        super().__init__(title, status)
        self.auther=auther
        self.isbn=isbn
    def get_loanPeriod(self):
        return 21
    
    @staticmethod
    def validate_Isbn(isbn:str)->bool:
     clean_isbn = isbn.replace("-", "").replace(" ", "")
     if len(clean_isbn) != 13 or not clean_isbn.isdigit():
        return False
     #the checksum algorithm for isbn-13
     total = sum(int(num) * (1 if idx % 2 == 0 else 3) for idx, num in enumerate(clean_isbn))
     return total%10==0
    

class Dvd(Library_Item):
    def __init__(self, title,director:str, status = Item_status.AVAILABLE):
        super().__init__(title, status)
        self.director=director

    def get_loanPeriod(self):
        return 5
    

class Magazine(Library_Item):
    def __init__(self, title,issue:str, status = Item_status.AVAILABLE):
        super().__init__(title, status)
        self.issue=issue

    def get_loanPeriod(self):
        return 14
    
#b=BOOK("Dune","frank Herbert","")
#print(b.__dict__)  keeps track of instance variable
class Database:
    # file load from or save from
    def __init__(self,filePath:str = "database.txt"):
        self.filePath=filePath
    # '_' private method for the database class only 
    def _parse_line(self,line:str)->dict:
       data={}
       parts=line.strip().split('|')
       for part in parts:
           key,value=part.split('=',1)
           if key =="status":
               value=Item_status[value]  #to out the status of the item 
           data[key]=value   # dict 
       return data       
    
    def load_from_file(self)->list[Library_Item]:
        items=[]  #empty list to be filled 
        try:
            with open(self.filePath,"r") as file:
                for line in file:
                    if line.strip() : # to remove newline 
                        pass # will be continuted 
                     
        except FileExistsError:
            return []   
        return items
    def save_to_file(self):
        pass
    
     
