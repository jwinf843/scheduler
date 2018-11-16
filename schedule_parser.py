import json
from pathlib import Path

class ScheduleParser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.contents = None
        self.class_list = None
        self.ordering = []
        self.insert_after_index_map = {}

    def load_contents(self):
        """Loads the contents of a json file in the /data directory"""
        if self.file_name:
            try:
                root_path = Path.cwd()
                with open(root_path / 'data' / self.file_name) as json_data:
                    self.class_list = json.load(json_data)
            except FileNotFoundError as e:
                print('File cannot be found. Make sure it is available in the \\data folder.')
                raise e

    def reorder(self):
        """Reorders the class list whereby prerequisite classes come before advanced classes"""
        current_min_prereq_ind = 0 #track the last index of classes without prereqs
        index = 0
        classes_copy = sorted(self.class_list, key=lambda cls: len(cls['prerequisites']))

        while index < len(classes_copy):
            subject = classes_copy[index]
            current_class = subject["name"]
            prereqs_for_current_class = subject["prerequisites"]

            if (not len(prereqs_for_current_class) or not len(self.ordering)):
                #if no prereqs required or no classes ordered yet then insert at the position before classes requiring prereqs
                self.insert_after_index_map[current_class] = current_min_prereq_ind
                current_min_prereq_ind+=1
                self.ordering.insert(current_min_prereq_ind, current_class)
                classes_copy.pop(index)
            else:
                #for classes with prereqs required, track the prereq with the greatest index
                current_max_prereq_ind = None

                for prereq in prereqs_for_current_class:
                    if self.insert_after_index_map.get(prereq) is not None:
                        if current_max_prereq_ind is None:
                            current_max_prereq_ind = self.insert_after_index_map[prereq]
                        current_max_prereq_ind = max(current_max_prereq_ind, self.insert_after_index_map[prereq] + 1)

                if current_max_prereq_ind is not None:
                    #if max prereq index has been determined then insert class in the position after the last prereq
                    self.insert_after_index_map[current_class] = current_max_prereq_ind
                    self.ordering.insert(current_max_prereq_ind+1, current_class)
                    classes_copy.pop(index)
                else:
                    #we haven't seen the prereqs required, shuffle the current_class to the end of the list and restart the while loop
                    classes_copy.append(classes_copy.pop(index))

        return self.ordering

    def print_class_order(self):
        """Prints the class order after reordering operation"""
        try:
            for ordered_class in self.ordering:
                print(ordered_class)
        except:
            pass
