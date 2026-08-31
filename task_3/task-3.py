from enum import Enum
from abc import ABC, abstractmethod


class Item_status(Enum):
    AVAILABLE = "AVAILABLE"
    CHECKED_OUT = "CHECKED_OUT"
    LOST = "LOST"


class Library_Item(ABC):
    def __init__(self, title: str, status: Item_status = Item_status.AVAILABLE):
        self.title = title
        self._status = status  # the '_' its a private attribute

    @classmethod
    def from_dict(cls, data: dict):
        cleanData = data.copy()
        cleanData.pop("type", None)  # to remove the type from the data entered
        return cls(**cleanData)     # unpack dict to populate instance attributes

    @property
    def status(self) -> Item_status:  # getter so read only
        return self._status

    @abstractmethod
    def get_loanPeriod(self) -> int:
        pass

    def checkout(self) -> None:
        if self._status == Item_status.CHECKED_OUT:
            raise ValueError(f"{self.title} is already checked out.")
        if self._status == Item_status.LOST:
            raise ValueError(f"{self.title} is lost and can't be checked out.")
        self._status = Item_status.CHECKED_OUT

    def return_item(self) -> None:
        self._status = Item_status.AVAILABLE

    def mark_lost(self) -> None:
        self._status = Item_status.LOST

    # implement __lt__ to sort by title
    def __lt__(self, other: "Library_Item") -> bool:
        if not isinstance(other, Library_Item):
            return NotImplemented
        return self.title.lower() < other.title.lower()  # lower to decrease error probability

    # __repr__
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title!r}, status={self._status.name!r})"

    # __str__
    def __str__(self) -> str:
        return f"{self.title} ({self.__class__.__name__}) - {self._status.value}"


class Book(Library_Item):
    def __init__(self, title: str, auther: str, isbn: str, status: Item_status = Item_status.AVAILABLE):
        super().__init__(title, status)
        self.auther = auther
        self.isbn = isbn

    def get_loanPeriod(self) -> int:
        return 21

    @staticmethod
    def validate_Isbn(isbn: str) -> bool:
        clean_isbn = isbn.replace("-", "").replace(" ", "")
        if len(clean_isbn) != 13 or not clean_isbn.isdigit():
            return False
        # the checksum algorithm for isbn-13
        total = sum(int(num) * (1 if idx % 2 == 0 else 3) for idx, num in enumerate(clean_isbn))
        return total % 10 == 0


class Dvd(Library_Item):
    def __init__(self, title: str, director: str, status: Item_status = Item_status.AVAILABLE):
        super().__init__(title, status)
        self.director = director

    def get_loanPeriod(self) -> int:
        return 5


class Magazine(Library_Item):
    def __init__(self, title: str, issue: str, status: Item_status = Item_status.AVAILABLE):
        super().__init__(title, status)
        self.issue = issue

    def get_loanPeriod(self) -> int:
        return 14


# item registry [used to map the dict to the classes using unique keys]
ItEM_REGISTIRY = {
    "Book": Book,
    "DVD": Dvd,
    "Dvd": Dvd,
    "Magazine": Magazine
}


def createItem(parsed_dict: dict) -> Library_Item:
    data = parsed_dict.copy()
    item_Type = data.get("type")

    if item_Type not in ItEM_REGISTIRY:
        raise ValueError(f"Unknown Item type: {item_Type}")
    item_class = ItEM_REGISTIRY[item_Type]
    return item_class.from_dict(data)


class Database:
    # file load from or save from
    def __init__(self, filePath: str = "database.txt"):
        self.filePath = filePath

    # '_' private method for the database class only
    def _parse_line(self, line: str) -> dict:
        data = {}
        parts = line.strip().split('|')
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                key = key.strip()
                value = value.strip()
                # support both 'auther' and 'author' keys
                if key == "author":
                    key = "auther"
                if key == "status":
                    value = Item_status[value]  # to out the status of the item
                data[key] = value  # dict
        return data

    def load_from_file(self) -> list[Library_Item]:
        items = []  # empty list to be filled
        try:
            with open(self.filePath, "r") as file:
                for line in file:
                    if line.strip():  # to remove newline
                        parsed_dict = self._parse_line(line)
                        item = createItem(parsed_dict)
                        items.append(item)
        except FileNotFoundError:
            return []
        return items

    def save_to_file(self, items: list[Library_Item]) -> None:
        with open(self.filePath, "w") as file:
            for item in items:
                fields = [f"type={item.__class__.__name__}", f"title={item.title}"]

                if isinstance(item, Book):
                    fields.extend([f"auther={item.auther}", f"isbn={item.isbn}"])
                elif isinstance(item, Dvd):
                    fields.append(f"director={item.director}")
                elif isinstance(item, Magazine):
                    fields.append(f"issue={item.issue}")

                fields.append(f"status={item.status.name}")
                file.write("|".join(fields) + "\n")


class Library:
    def __init__(self, dataBase: Database = None):
        self.dataBase = dataBase
        self.items: list[Library_Item] = self.dataBase.load_from_file() if self.dataBase else []

    def add_item(self, item: Library_Item) -> None:
        self.items.append(item)

    def find_by_title(self, title: str) -> Library_Item | None:
        for item in self.items:
            if item.title.lower() == title.lower():
                return item
        return None

    def checkout(self, title: str) -> bool:
        item = self.find_by_title(title)
        if item:
            item.checkout()
            return True
        return False

    def return_item(self, title: str) -> bool:
        item = self.find_by_title(title)
        if item:
            item.return_item()
            return True
        return False

    def list_available(self) -> list[Library_Item]:
        return [item for item in self.items if item.status == Item_status.AVAILABLE]

    def save(self) -> None:
        if self.dataBase:
            self.dataBase.save_to_file(self.items)


if __name__ == "__main__":
    db = Database("database.txt")
    library = Library(db)

    print("---- Loaded Items ----")
    for item in library.items:
        print(f"Loaded: {item}")

    # Test adding items
    new_book = Book("The Hobbit", "J.R.R. Tolkien", "9780261102217")
    new_dvd = Dvd("Interstellar", "Christopher Nolan")
    new_mag = Magazine("National Geographic", "August 2026")

    library.add_item(new_book)
    library.add_item(new_dvd)
    library.add_item(new_mag)

    print("\n---- Sorted Collection ----")
    for item in sorted(library.items):
        print(f"{item} | Loan Period: {item.get_loanPeriod()} days")

    # Save updates back to database.txt
    library.save()
    print("\nSaved successfully to database.txt!")