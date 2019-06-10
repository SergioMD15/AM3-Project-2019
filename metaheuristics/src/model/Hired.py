class Hired:
    def __init__(self, provider, workers):
        available = provider.get_available_workers()
        if(2 * available >= workers):
            if(workers <= available):
                if(not (workers == 0 or workers == available or workers == available / 2)):
                    raise Exception('Unsupported assignment of workers: Not valid amount')
        else:
            raise Exception('Unsupported assignment of workers: Cannot assign more workers than available ones')

        self.provider = provider
        self.workers = workers

        self.calculate_hired()

    def calculate_hired(self):
        self.hired_base = self.calculate_base()
        self.hired_extra = self.calculate_extra()

    def calculate_base(self):
        workers = self.workers
        available = self.provider.get_available_workers()

        base = workers if workers < available else available

        if(base == 0):
            self.provider.hire_none()
        elif(base == available / 2):
            self.provider.hire_half()
        else:
            self.provider.hire_all()

        # We assume only valid results (0, half, all) will be received

        return base

    def calculate_extra(self):
        workers = self.workers
        available = self.provider.get_available_workers()

        extra = 0 if workers < available else workers - available
        self.provider.set_extra(extra)

        return extra

    def get_provider(self):
        return self.provider
    
    def get_workers(self):
        return self.workers

    def calculate_cost(self, cost_1, cost_2, cost_3):
        available = self.provider.get_available_workers()
        contract = 0 if self.provider.none_hired else self.provider.get_cost_contract()

        base = self.hired_base * self.provider.get_cost_worker()
        extra = self.provider.get_first_bracket() * cost_1 \
            + self.provider.get_second_bracket() * cost_2 \
            + self.provider.get_third_bracket() * cost_3
        workers = base + extra

        return contract + workers

    def __str__(self):
        return "[Provider: %d, Workers Hired: %d]" % (self.get_provider().get_id(), self.workers())
