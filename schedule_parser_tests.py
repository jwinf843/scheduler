import pytest
from .schedule_parser import ScheduleParser
import random


def _setup_math_parser():
    math = ScheduleParser('math.json')
    math.load_contents()
    return math

def _setup_physics_parser():
    physics = ScheduleParser('physics.json')
    physics.load_contents()
    return physics

def test_error_loading_contents():
    """File not found"""
    with pytest.raises(FileNotFoundError):
        ScheduleParser('physics.jso').load_contents()


def test_load_contents():
    """Test loading the given file"""
    physics_classes = _setup_physics_parser()
    assert(physics_classes.class_list == [{'name': 'Calculus', 'prerequisites': []},
        {'name': 'Scientific Thinking', 'prerequisites': []},
        {'name': 'Differential Equations', 'prerequisites': ['Calculus']},
        {'name': 'Intro to Physics', 'prerequisites': ['Scientific Thinking']},
        {'name': 'Relativity', 'prerequisites': ['Differential Equations', 'Intro to Physics']}
    ]) is True

    math_classes = _setup_math_parser()
    assert(math_classes.class_list == [
        {'name': 'Algebra 1', 'prerequisites': []},
        {'name': 'Geometry', 'prerequisites': []},
        {'name': 'Algebra 2', 'prerequisites': ['Algebra 1', 'Geometry']},
        {'name': 'Pre Calculus', 'prerequisites': ['Algebra 2']}
    ]) is True

def test_reorder_of_classes():
    """Test ordering of the classes after loading the file"""
    physics_classes = _setup_physics_parser()
    assert(physics_classes.reorder() == [
        'Calculus',
        'Scientific Thinking',
        'Differential Equations',
        'Intro to Physics',
        'Relativity']
    ) is True

    assert(physics_classes.insert_after_index_map == {
        'Calculus': 0,
        'Scientific Thinking': 1,
        'Differential Equations': 1,
        'Intro to Physics': 2,
        'Relativity': 3}
    ) is True

    math_classes = _setup_math_parser()
    assert(math_classes.reorder() == ['Algebra 1', 'Geometry', 'Algebra 2', 'Pre Calculus']) is True
    assert(math_classes.insert_after_index_map == {
        'Algebra 1': 0,
        'Geometry': 1,
        'Algebra 2': 2,
        'Pre Calculus': 3}
    ) is True

def test_reorder_of_classes_after_shuffle():
    """Test ordering of the classes after shuffling the classes.
    `insert_after_index_map` informs where in the list the class was added at the time of reorder.
    Testing the index map is sufficient to let us know that advanced classes are added after their prerequisites."""

    physics_classes = _setup_physics_parser()
    random.shuffle(physics_classes.class_list)
    physics_classes.reorder()
    assert(physics_classes.insert_after_index_map.get('Calculus') < physics_classes.insert_after_index_map.get('Differential Equations')) is True
    assert(physics_classes.insert_after_index_map.get('Differential Equations') < physics_classes.insert_after_index_map.get('Relativity')) is True
    assert(physics_classes.insert_after_index_map.get('Intro to Physics') < physics_classes.insert_after_index_map.get('Relativity')) is True

    math_classes = _setup_math_parser()
    random.shuffle(math_classes.class_list)
    math_classes.reorder()
    assert(math_classes.insert_after_index_map.get('Algebra 2') < math_classes.insert_after_index_map.get('Pre Calculus')) is True
    assert(math_classes.insert_after_index_map.get('Algebra 1') < math_classes.insert_after_index_map.get('Algebra 2')) is True
    assert(math_classes.insert_after_index_map.get('Geometry') < math_classes.insert_after_index_map.get('Algebra 2')) is True
