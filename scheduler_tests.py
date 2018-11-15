from scheduler import ScheduleParser

physics_classes = ScheduleParser('physics.json')
physics_classes.read_contents()
physics_classes.reorder() == ['Calculus', 'Scientific Thinking','Differential Equations','Intro to Physics','Relativity']

math_classes = ScheduleParser('math.json')
math_classes.read_contents()
math_classes.reorder() == ['Algebra 1', 'Geometry', 'Algebra 2', 'Pre Calculus']
