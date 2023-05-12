class Job():
    joblist = ["trashman", "police"]

    trashman = {
        "min_pay": 500,
        "max_pay": 1000,
        "success_chance": 90,
        "fail_message": "You spilled the trash!"
    }

    def __init__(self, name):
        self.work = {}
        match name.lower():
            case "trashman":
                self.work = self.trashman
        self.min_pay = self.work["min_pay"]
        self.max_pay = self.work["max_pay"]
        self.success_chance = self.work["success_chance"]
        self.fail_message = self.work["fail_message"]

    def autocomplete(ctx):
        jobs = Job.joblist
        autocomplete = []
        for job in jobs:
            if job.startswith(ctx.value.lower()):
                autocomplete.append(job)
        return autocomplete if autocomplete else jobs
