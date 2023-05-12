class Job():
    joblist = ["Trashman", "Police", "Firefighter", "Criminal", "Officeworker", "Programmer"]

    trashman = {
        "min_pay": 500,
        "max_pay": 1000,
        "success_chance": 90,
        "fail_message": "You spilled the trash!"
    }

    police = {
        "min_pay": 750,
        "max_pay": 1250,
        "success_chance": 80,
        "fail_message": "You didn't catch the thief!"
    }

    firefighter = {
        "min_pay": 1500,
        "max_pay": 2000,
        "success_chance": 55,
        "fail_message": "The building burnt down!"
    }

    criminal = {
        "min_pay": 75,
        "max_pay": 10000,
        "success_chance": 20,
        "fail_message": "You were caught!"
    }

    officeworker = {
        "min_pay": 450,
        "max_pay": 950,
        "success_chance": 100,
        "fail_message": ""
    }

    programmer = {
        "min_pay": 2000,
        "max_pay": 4000,
        "success_chance": 45,
        "fail_message": "StackOverflow!"
    }

    def __init__(self, name):
        self.work = {}
        match name.lower():
            case "trashman":
                self.work = self.trashman
            case "Police":
                self.work = self.police
            case "firefighter":
                self.work = self.firefighter
            case "criminal":
                self.work = self.criminal
            case "officeworker":
                self.work = self.officeworker
            case "programmer":
                self.work = self.programmer

        self.min_pay = self.work["min_pay"]
        self.max_pay = self.work["max_pay"]
        self.success_chance = self.work["success_chance"]
        self.fail_message = self.work["fail_message"]

    def autocomplete(self, ctx):
        jobs = Job.joblist
        autocomplete = []
        for job in jobs:
            if job.lower().startswith(ctx.value.lower()):
                autocomplete.append(job)
        return autocomplete if autocomplete else jobs
