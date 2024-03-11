class Book:
    def __init__(self, title, author, release_year, unique_ISBN):
        self.title = title
        self.author = author
        self.release_year = release_year
        self.unique_ISBN = unique_ISBN
        self.available = True
        self.reserved = None


    def is_available(self):
        return self.available

    def reserve_book(self, user_id):
        if self.available:
            self.available = False
            self.reserved_by = user_id
            return True
        else:
            return False
        
    
    def loan_book(self, user_id):
        if self.available:
            self.available = True
            self.reserved_by = user_id
            return True
        else:
            return False
        
    def return_book(self):
        self.available = True
        self.reserved_by = None
        return True
