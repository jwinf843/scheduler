import sys
import json

class ScheduleParser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.contents = None
        self.class_list = None
        self.ordering = []

    def read_contents(self):
        if self.file_name:
            with open(self.file_name) as json_data:
                self.class_list = json.load(json_data)

    def reorder(self):
        seen = {}
        current_min_prereq_ind = 0 #track the last index of classes without prereqs
        index = 0
        classes_copy = self.class_list[:]

        while index < len(classes_copy):
            subject = classes_copy[index]
            current_class = subject["name"]
            prereqs_for_current_class = subject["prerequisites"]

            if (not len(prereqs_for_current_class) or not len(self.ordering)):
                #if no prereqs required or no classes ordered yet then insert at the position before classes requiring prereqs
                seen[current_class] = current_min_prereq_ind
                current_min_prereq_ind+=1
                self.ordering.insert(current_min_prereq_ind, current_class)
                classes_copy.pop(index)
            else:
                #for classes with prereqs required, track the prereq with the greatest index
                current_max_prereq_ind = None

                for prereq in prereqs_for_current_class:
                    if seen.get(prereq) is not None:
                        if current_max_prereq_ind is None:
                            current_max_prereq_ind = seen[prereq]
                        current_max_prereq_ind = max(current_max_prereq_ind, seen[prereq] + 1)

                if current_max_prereq_ind is not None:
                    #if max prereq index has been determined then insert class in the position after the last prereq
                    seen[current_class] = current_max_prereq_ind
                    self.ordering.insert(current_max_prereq_ind+1, current_class)
                    classes_copy.pop(index)
                else:
                    #we haven't seen the prereqs required, shuffle the current_class to the end of the list and restart the while loop
                    classes_copy.append(classes_copy.pop(index))

        return self.ordering

    def print_class_order(self):
        try:
            for ordered_class in self.ordering:
                print(ordered_class)
        except:
            pass

if __name__ == '__main__':
    json_file = None
    if len(sys.argv) >= 2:
        json_file = sys.argv[1]

    parser = ScheduleParser(json_file)
    parser.read_contents()
    parser.reorder()
    parser.print_class_order()
