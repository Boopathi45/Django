class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

rect = Rectangle(10, 5) # --- Example usage ---

# iterate over an instance of the Rectangle class
for dimension in rect:
    print(dimension)


# Expected output as follows:

{'length': 10}
{'width': 5}