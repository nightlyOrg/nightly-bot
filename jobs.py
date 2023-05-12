class Job():
    trashman = {
        "min_pay": 500,
        "max_pay": 1000
    }

    def __init__(self, name):
        self.work = {}
        for job in Job():
            if job.__getattribute__(name):
                self.work = job
        self.min_pay = self.work["min_pay"]
        self.max_pay = self.work["max_pay"]
