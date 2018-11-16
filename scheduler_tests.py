import pytest
from scheduler import ScheduleParser

def setup_math_parser():
    math = ScheduleParser('math.json')
    math.read_contents()
    return math

def setup_physics_parser():
    physics = ScheduleParser('physics.json')
    physics.read_contents()
    return physics


def test_read_contents():
    physics_classes = setup_physics_parser()
    assert(physics_classes.class_list == [{'name': 'Calculus', 'prerequisites': []},
        {'name': 'Scientific Thinking', 'prerequisites': []},
        {'name': 'Differential Equations', 'prerequisites': ['Calculus']},
        {'name': 'Intro to Physics', 'prerequisites': ['Scientific Thinking']},
        {'name': 'Relativity', 'prerequisites': ['Differential Equations', 'Intro to Physics']}
    ]) is True

    math_classes = setup_math_parser()
    assert(math_classes.class_list == [
        {'name': 'Algebra 1', 'prerequisites': []},
        {'name': 'Geometry', 'prerequisites': []},
        {'name': 'Algebra 2', 'prerequisites': ['Algebra 1', 'Geometry']},
        {'name': 'Pre Calculus', 'prerequisites': ['Algebra 2']}
    ]) is True

def test_reorder_of_classes():
    physics_classes = setup_physics_parser()
    assert(physics_classes.reorder() == ['Calculus', 'Scientific Thinking','Differential Equations','Intro to Physics','Relativity']) is True

    math_classes = setup_math_parser()
    assert(math_classes.reorder() == ['Algebra 1', 'Geometry', 'Algebra 2', 'Pre Calculus']) is True
