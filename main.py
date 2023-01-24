# https://www.optaplanner.org/blog/2016/10/26/DomainModelingGuide.html
# https://docs.optaplanner.org/7.11.0.Final/optaplanner-docs/html_single/index.html#designPatterns
# https://yed-uml.readthedocs.io/en/latest/class-diagram.html
# https://github.com/optapy/optapy


from optapy import problem_fact
from optapy import planning_entity, planning_id, planning_variable

from optapy import planning_solution, problem_fact_collection_property, value_range_provider, planning_entity_collection_property, planning_score
from optapy.types import HardSoftScore
from optapy.types import Joiners, HardSoftScore
from optapy import constraint_provider

def format_list(a_list):
    return ',\n'.join(map(str, a_list))
@problem_fact
class Month:
    def __init__(self, id, number,name):
        self.id = id
        self.number = number
        self.name = name

@planning_entity()
class KW:
    def __init__(self,id,person,discipline,month=None):
        self.id=id
        self.person=person
        self.discipline=discipline
        self.month=month

    @planning_id
    def get_id(self):
        return self.id

    @planning_variable(Month, value_range_provider_refs=["monthRange"])
    def get_month(self):
        return self.month

    def set_month(self, new_month):
        self.month = new_month

@planning_solution
class Plan:
    def __init__(self, month_list, kw_list, score=None):
        self.month_list = month_list
        self.kw_list = kw_list
        self.score = score

    @problem_fact_collection_property(Month)
    @value_range_provider(range_id = "monthRange")
    def get_month_list(self):
        return self.month_list

    @planning_entity_collection_property(KW)
    def get_kw_list(self):
        return self.kw_list

    @planning_score(HardSoftScore)
    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def __str__(self):
        return (
            f"Plan("
            f"month_list={format_list(self.month_list)},\n"
            f"kw_list={format_list(self.kw_list)},\n"
            f"score={str(self.score.toString()) if self.score is not None else 'None'}"
            f")"
        )

@constraint_provider
def define_constraints(constraint_factory):
    return [
        # Hard constraints
        room_conflict(constraint_factory),
        # Other constraints here...
    ]

def room_conflict(constraint_factory):
    # A room can accommodate at most one lesson at the same time.
    return constraint_factory.for_each_unique_pair(KW,
                # ... in the same timeslot ...
                Joiners.equal(lambda kw: kw.person),
                # ... in the same room ...
                Joiners.equal(lambda kw: kw.month)) \
        .penalize("Two kw in month", HardSoftScore.ONE_HARD)


def generate_problem():
    month_list=[
        Month(1,1,'JAN'),
        Month(2, 2, 'FEB'),
        Month(3, 3, 'MARCH'),
        Month(4, 4, 'APRIL'),
        Month(5, 5, 'MAY'),
        Month(6, 6, 'JUN'),
        Month(7, 7, 'JULY'),
    ]

    kw_list=[
        KW(1,"Amb",'D1'),
        KW(2, "Bug", 'D1'),
        KW(3, "Fod", 'D3'),
        KW(4, "Wn", 'D4'),
        KW(5, "Bug", 'D3'),
        KW(6, "Amb", 'D3'),
        KW(7, "Fod", 'D4'),
        KW(8, "Wn", 'D7'),
        KW(9, "Amb", 'D4'),
        KW(10, "Fod", 'D5'),
    ]
    kw=kw_list[0]
    kw.set_month(month_list[0])
    return Plan(month_list, kw_list)

if __name__ == "__main__":
    from optapy import solver_factory_create
    from optapy.types import SolverConfig, Duration


    solver_config = SolverConfig().withEntityClasses(KW) \
        .withSolutionClass(Plan) \
        .withConstraintProviderClass(define_constraints) \
        .withTerminationSpentLimit(Duration.ofSeconds(30))

    solver = solver_factory_create(solver_config).buildSolver()
    solution = solver.solve(generate_problem())
    print(solution.month_list[0])
    #print(dir(solution.kw_list))
    #print(format_list(solution.kw_list))