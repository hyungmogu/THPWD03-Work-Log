'''
    WORK LOG

    REQUIREMENTS

        1. [x] As a user of the script, I should be prompted with a menu to choose whether to add a new entry or lookup previous entries.

        2. [] As a user of the script, if I choose to enter a new work log, I should be able to provide a task name, a number of minutes spent working on it, and any additional notes I want to record.

        3. [] As a user of the script, if I choose to find a previous entry, I should be presented with four options:

            a. find by date
            b. find by time spent
            c. find by exact search
            d. find by pattern

            NOTE:
            a) [] When finding by date, I should be presented with a list of dates with entries and be able to choose one to see entries from.
            b) [] When finding by time spent, I should be allowed to enter the number of minutes a task took and be able to choose one to see entries from.
            c) [] When finding by an exact string, I should be allowed to enter a string and then be presented with entries containing that string in the task name or notes.
            d) [] When finding by a pattern, I should be allowed to enter a regular expression and then be presented with entries matching that pattern in their task name or notes.
            e) [] When displaying the entries, the entries should be displayed in a readable format with the date, task name, time spent, and notes information.

'''

import os
import re

from model_service import ModelService
from view_service import ViewService

# TODO: Generalize is_response_valid_main
# TODO: Move menu items (i.e. ["Add Entry", "Search Existing Entry", "Quit"]) to ModelService

class Program: # this is controller (from MVC architecture.)
    def __init__(self, model_service=ModelService, view_service=ViewService):
        self.quit_program = False

        self.view_service = ViewService()
        self.model_service = ModelService()

    def is_response_valid_main(self, response):
        if len(re.findall(r"[^a-zA-Z]", response)) > 0:
            return False

        if len(response) != 1:
            return False

        if ord(response) < 97 or ord(response) >= 97 + len(["Add Entry", "Search Existing Entry", "Quit"]):
            return False

        return True

    def clear_screen(self):
        os.system('cls')  # For Windows
        os.system('clear')  # For Linux/OS X

    def quit(self):
        print("Thank you and take care")
        self.quit_program = True

    def run_main(self):
        self.view_service.page_title = 'Main Page'

        while not self.quit_program:
            self.clear_screen()
            self.view_service.get_main(["Add Entry", "Search Existing Entry", "Quit"])

            response = input("> ").strip().lower()

            if not self.is_response_valid_main(response):
                self.view_service.error_message = self.get_error_message(response)
                continue

            if response == 'a':
                self.run_add()

            elif response == 'b':
                self.run_search()

            else:
                self.clear_screen()
                self.quit()


    def run_add(self):
        pass

    def run_search(self):
        pass

    def run_display(self):
        pass


if __name__ == "__main__":
    program = Program()
    program.run_main()