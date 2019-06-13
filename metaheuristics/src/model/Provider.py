class Provider:
    def __init__(self, _id, cost_worker, available_workers, cost_contract, country):
        self.id = _id
        self.cost_worker = cost_worker
        self.available_workers = available_workers
        self.cost_contract = cost_contract
        self.country = country

        self.all_hired = False
        self.none_hired = True
        self.half_hired = False

        self.first_bracket = 0
        self.second_bracket = 0
        self.third_bracket = 0

        self.incompatibilities = 0

    def get_id(self):
        return self.id

    def get_incompatibilities():
        return self.incompatibilities

    def get_cost_worker(self):
        return self.cost_worker

    def get_available_workers(self):
        return self.available_workers

    def get_cost_contract(self):
        return self.cost_contract

    def get_country(self):
        return self.country

    def is_all_hired(self):
        return self.all_hired

    def is_none_hired(self):
        return self.none_hired

    def is_half_hired(self):
        return self.half_hired

    def hire_all(self):
        self.hired_all = True
        self.hired_half = False
        self.hired_none = False

    def hire_half(self):
        self.hired_all = False
        self.hired_half = True
        self.hired_none = False

    def hire_none(self):
        self.hired_all = False
        self.hired_half = False
        self.hired_none = True

    def set_brackets(self, workers):
        self.set_first_bracket(min(5, workers))

        self.set_second_bracket(
            0 if (self.first_bracket < 5) else min(5, workers - 5))

        self.set_third_bracket(
            0 if (self.second_bracket < 5) else workers - 10)

    def get_first_bracket(self):
        return self.first_bracket

    def set_first_bracket(self, workers):
        self.first_bracket = workers

    def get_second_bracket(self):
        return self.second_bracket

    def set_second_bracket(self, workers):
        self.second_bracket = workers

    def get_third_bracket(self):
        return self.third_bracket

    def set_third_bracket(self, workers):
        self.third_bracket = workers

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __hash__(self):
        return self.get_id()

    def __str__(self):
        return 'Provider: %d \t Num_workers: %d' % (self.id, self.available_workers)
