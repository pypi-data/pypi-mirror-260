class mather:
    def __init__(self):
        self.showProgress = False

    def add(self, x, y):
        if self.showProgress:
            print("Adding Please Wait")
        return x + y

    def sub(self, x, y):
        if self.showProgress:
            print("Subtractiong Please Wait")
        return x - y
