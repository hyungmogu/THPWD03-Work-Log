'''
    WORK LOG

    REQUIREMENTS

        1. [x] As a user of the script, I should be prompted with a menu to choose whether to add a new entry or lookup previous entries.

        2. [x] As a user of the script, if I choose to enter a new work log, I should be able to provide a task name, a number of minutes spent working on it, and any additional notes I want to record.

        3. [x] As a user of the script, if I choose to find a previous entry, I should be presented with four options:

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
import sys
import csv
import datetime

from model_service import ModelService
from view_service import ViewService

# TODO: Generalize is_response_valid_main_page
# TODO: Move prompt to object [maybe]

class Program: # this is controller (from MVC architecture.)
    def __init__(self, model_service=ModelService, view_service=ViewService):
        self.quit_program = False

        self.view_service = ViewService()
        self.model_service = ModelService()

    def clear_screen(self):
        os.system('cls')  # For Windows
        os.system('clear')  # For Linux/OS X

    def quit(self):
        print("Thank You and Take Care")
        self.quit_program = True

    def get_error_message_main_page(self, response, menu):
        # 1. if menu is empty, then set menu is empty error
        if len(menu) == 0:
            error_message = "Sorry. There are no items in menu. Please exit program (Ctrl + c) and try again."

        # 2. if menu has value other than what's available, set value error
        if not len(response) == 1 or not (ord(response) >= 97 and ord(response) < 97 + len(menu)):
            error_message = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(menu) - 1))

        return error_message

    def is_response_valid_main_page(self, response, menu):
        # 1. if response contains characters other than letters, return false
        if len(re.findall(r"[^a-zA-Z]", response)) > 0:
            return False

        # 2. if response contains characters of length greater than 1, then return false
        if len(response) > 1 or len(response) == 0:
            return False

        # 3. if response contains character of value less than ASCII value of 97 and greater than or equal to 97 + len(main_items), then return false
        if ord(response) < 97 or ord(response) >= 97 + len(menu):
            return False

        # 4. otherwise, return true
        return True

    def run_main_page(self):
        self.view_service.page_title = 'Main Page'
        menu = self.model_service.get_menu('main')

        while not self.quit_program:
            self.clear_screen()
            self.view_service.get_main_page(menu)

            if sys.version_info < (3, 0):
                response = raw_input("> ").strip().lower()
            else:
                response = input("> ").strip().lower()

            if not self.is_response_valid_main_page(response, menu):
                self.view_service.error_message = self.get_error_message_main_page(response, menu)
                continue

            if response == 'a':
                self.run_add_page()

            elif response == 'b':
                self.run_search_page()

            else:
                self.clear_screen()
                self.quit()

    def is_response_valid_add_page(self, response, prompt):
        if prompt != 'Additional Notes' and response.strip() == '':
            return False

        if prompt == '# of Minutes' and re.search(r'[^0-9]', response) != None:
            return False

        return True

    def get_error_message_add_page(self, response, prompt):
        if prompt != 'Additional Notes' and response.strip() == '':
            return 'Please enter non-empty value'

        if prompt == '# of Minutes':
            return 'Please enter integer value between 0-60'

    def _file_is_empty(self, file):
        if file.tell() == 0:
            return True
        return False

    def run_add_page(self):
        self.view_service.page_title = 'Add Entry Page'
        prompts = ["Task Name", "# of Minutes", "Additional Notes"]
        output = {}

        # 1. Walk through each prompt and store value in output
        for prompt in prompts:
            correct = False
            while not correct:
                self.clear_screen()
                self.view_service.get_add_page(prompt)

                if sys.version_info < (3, 0):
                    response = raw_input("> ").strip().lower()
                else:
                    response = input("> ").strip().lower()

                if not self.is_response_valid_add_page(response, prompt):
                    self.view_service.error_message = self.get_error_message_add_page(response, prompt)
                    continue

                output[prompt] = response
                correct = True

        output['Date'] = datetime.datetime.now().strftime('%B %d, %Y')

        # 2. Store / append output in csv
        with open("work_log.csv", "a" ) as csvFile:
            csvHeaders = ['Date'] + prompts
            csvWriter = csv.DictWriter(csvFile, fieldnames=csvHeaders)

            if self._file_is_empty(csvFile):
                csvWriter.writeheader()
            csvWriter.writerow(output)

        self.run_display_page('add_page', [output])

    def is_response_valid_search_page(self, response, menu):
        # 1. if response contains characters other than letters, return false
        if len(re.findall(r"[^a-zA-Z]", response)) > 0:
            return False

        # 2. if response contains characters of length greater than 1 or 0, then return false
        if len(response) > 1 or len(response) == 0:
            return False

        # 3. if response contains character of value less than ASCII value of 97 and greater than or equal to 97 + len(main_items), then return false
        if ord(response) < 97 or ord(response) >= 97 + len(menu):
            return False

        # 4. otherwise, return true
        return True

    def get_error_message_search_page(self, response, menu):
        # 1. if menu is empty, then set menu is empty error
        if len(menu) == 0:
            error_message = "Sorry. There are no items in menu. Please exit program (Ctrl + c) and try again."

        # 2. if menu has value other than what's available, set value error
        if not len(response) == 1 or not (ord(response) >= 97 and ord(response) < 97 + len(menu)):
            error_message = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(menu) - 1))

        return error_message

    def run_search_page(self):
        self.view_service.page_title = 'Search Page'

        exit_page = False
        menu = self.model_service.get_menu('search_page')

        while not exit_page:
            self.clear_screen()
            self.view_service.get_search_page(menu)

            if sys.version_info < (3, 0):
                response = raw_input("> ").strip().lower()
            else:
                response = input("> ").strip().lower()

            if not self.is_response_valid_search_page(response, menu):
                self.view_service.error_message = self.get_error_message_search_page(response, menu)
                continue

            if response == 'a':
                self.run_search_page_by_date()

            elif response == 'b':
                self.run_search_page_by_time_spent()

            elif response == 'c':
                self.run_search_page_by_exact_search()

            elif response == 'd':
                self.run_find_by_the_pattern()

            elif response == 'e':
                exit_page = True
                self.clear_screen()

        self.run_main_page()

    def is_response_valid_display_page(self, response, path):
        if path == 'search_page':
            choices = ['N','P','R']
        else:
            choices = ['R']

        # if the response is empty, warn user to type the correct value
        if response not in choices:
            return False
        return True

    def get_error_message_display_page(self, response, path):
        if path == 'search_page':
            choices = ['N','P','R']
        else:
            choices = ['R']

        # if the response is empty, warn user to type the correct value
        if response not in choices:
            return "Please choose correct value(s) ({})".format(",".join(choices))

    def run_display_page(self, path, items):
        exit_page = False
        self.view_service.page_title = 'Display Page'
        index = 0

        while not exit_page:

            # while quit page is not registered, allow users to navigate through items
            self.clear_screen()
            self.view_service.get_display_page(path, items, index)

            if sys.version_info < (3, 0):
                response = raw_input("> ").strip()
            else:
                response = input("> ").strip()

            if not self.is_response_valid_display_page(response, path):
                self.view_service.error_message = self.get_error_message_display_page(response, path)
                continue

            if response == 'N':
                index = index + 1 if (index+1) < len(items) else index

            elif response == 'P':
                index = index - 1 if (index - 1) >= 0 else index

            elif response == 'R':
                exit_page = True
                self.clear_screen()


        self.run_search_page() if path == 'search_page' else self.run_main_page()

if __name__ == "__main__":
    program = Program()
    program.run_main_page()