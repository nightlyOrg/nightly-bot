class Job():
    trashman = {
        "min_pay": 500,
        "max_pay": 1000
    }

    def __init__(self, name):
        self.work = {}
        match name.lower():
            case "trashman":
                self.work = self.trashman
        self.min_pay = self.work["min_pay"]
        self.max_pay = self.work["max_pay"]
