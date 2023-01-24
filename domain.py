from optapy import problem_fact, planning_id, planning_entity, planning_variable, \
    planning_solution, planning_entity_collection_property, \
    problem_fact_collection_property, \
    value_range_provider, planning_score

from optapy.types import HardSoftScore
from collections import OrderedDict
from math import ceil
################################################
wall_len = OrderedDict()
wall_len['a'] = 150.0
wall_len['b'] = 100.0
wall_len['c'] = 30.0
wall_len['d'] = 40.0
wall_len['e'] = 120.0
wall_len['f'] = 60.0

min_len = 20.0
board_len = 140.0

# wylicz maksynalną bazową liczbę listew
N = ceil((sum(wall_len.values()) + len(wall_len) * min_len) / board_len)
print(N)

###########################################
@problem_fact
class BaseboardMolding: #indeksy listew
    id: int
    name: str

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"BaseboardMolding(id={self.id}, name={self.name})"

@problem_fact
class SegmentLength: # długości listew
    id: int
    seg_length: int

    def __init__(self, id, seg_length):
        self.id = id
        self.seg_length = seg_length

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"SegmentLength(id={self.id}, seg_length={self.seg_length})"

@problem_fact
class WallSegmentLength: # długości ścian
    id: int
    wall_name:str
    wall_length: float

    def __init__(self, id,wall_name, wall_length):
        self.id = id
        self.wall_name=wall_name
        self.wall_length = wall_length

    @planning_id
    def get_id(self):
        return self.id

    def __str__(self):
        return f"WallSegmentLength(id={self.id},wall_name={self.wall_name} wall_length={self.wall_length})"

@planning_entity
class Selection:
    id: int
    baseboard_molding: BaseboardMolding
    segment_length: SegmentLength
    wall_segment_length:WallSegmentLength


    def __init__(self, id, baseboard_molding=None, segment_length=None, wall_segment_length=None):
        self.id = id
        self.baseboard_molding = baseboard_molding
        self.segment_length = segment_length
        self.wall_segment_length = wall_segment_length

    @planning_id
    def get_id(self):
        return self.id

    @planning_variable(BaseboardMolding, ["BaseboardMoldingRange"])
    def get_baseboard_molding(self):
        return self.baseboard_molding

    def set_baseboard_molding(self, new_baseboard_molding):
        self.baseboard_molding = new_baseboard_molding

    @planning_variable(SegmentLength, ["SegmentLengthRange"])
    def get_segment_length(self):
        return self.segment_length

    def set_segment_length(self, new_segment_length):
        self.room = new_segment_length


    @planning_variable(WallSegmentLength, ["WallSegmentLengthRange"])
    def get_wall_segment_length(self):
        return self.wall_segment_length

    def set_wall_segment_length(self, new_wall_segment_length):
        self.wall_segment_length = new_wall_segment_length

# Generate the problem
def generate_problem():
    # lista indexów listw
    BaseboardMoldingRange_list=[]
    for  i in range(N):
        print(i)
        BaseboardMoldingRange_list.append(BaseboardMolding(i+1,str(i+1)))
    print(BaseboardMoldingRange_list)

    #lista  dlugosci segmentow do przyciecia
    SegmentLengthRange_list=[]
    for i in range(int(board_len)+1):
        SegmentLengthRange_list.append(SegmentLength(i+1,i))
        print(i)

    # lista długości ścian
    WallSegmentLength_list=[]
    for  i, (key,value) in enumerate(wall_len.items()):
        print(i,key,value)
        WallSegmentLength_list.append(WallSegmentLength(i+1,key,value))
    #print(dir(WallSegmentLength_list))





generate_problem()