from dataclasses import dataclass

@dataclass #add a category/ from database and not input by user (Insert Into) Action
class Category:
    id: int = 0
    name:str = ""
    
@dataclass # add more to the movie desc, price, discount
class Movie:
    id:int = 0
    name:str = ""
    year: int= 0
    minutes:int =0
    desc: str = ""
    category:Category = None
    



