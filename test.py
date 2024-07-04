class test():
    def __init__(self , id):
        self.id = id
    
    def __repr__(self):
        return f'my id is : {self.id}'

obj = test(1)

print(obj)