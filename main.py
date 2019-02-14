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
            a) [x] When finding by date, I should be presented with a list of dates with entries and be able to choose one to see entries from.
            b) [x] When finding by time spent, I should be allowed to enter the number of minutes a task took and be able to choose one to see entries from.
            c) [] When finding by an exact string, I should be allowed to enter a string and then be presented with entries containing that string in the task name or notes.
            d) [] When finding by a pattern, I should be allowed to enter a regular expression and then be presented with entries matching that pattern in their task name or notes.
            e) [x] When displaying the entries, the entries should be displayed in a readable format with the date, task name, time spent, and notes information.

'''

import os
import re
import sys
import csv
import datetime

from model_service import ModelService
from view_service import ViewService

# TODO: Generalize is_response_valid method
# TODO: Move prompt to object [maybe]

class Program: # this is controller (from MVC architecture.)
    def __init__(self, model_service=ModelService, view_service=ViewService):
        self.quit_program = False

        self.view_service = ViewService()
        self.model_service = ModelService()

    def _clear_screen(self):
        os.system('cls')  # For Windows
        os.system('clear')  # For Linux/OS X

    def _quit(self):
        print("Thank You and Take Care")
        self.quit_program = True

    def _get_error_message_main_page(self, response, menu):
        # 1. if menu is empty, then set menu is empty error
        if len(menu) == 0:
            error_message = "Sorry. There are no items in menu. Please exit program (Ctrl + c) and try again."

        # 2. if menu has value other than what's available, set value error
        if not len(response) == 1 or not (ord(response) >= 97 and ord(response) < 97 + len(menu)):
            error_message = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(menu) - 1))

        return error_message

    def _is_response_valid_main_page(self, response, menu):
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
        exit_page = False

        while not exit_page:
            self._clear_screen()
            self.view_service.get_main_page(menu)

            if sys.version_info < (3, 0):
                response = raw_input("> ").strip().lower()
            else:
                response = input("> ").strip().lower()

            if not self._is_response_valid_main_page(response, menu):
                self.view_service.error_message = self._get_error_message_main_page(response, menu)
                continue

            exit_page = True



        if response == 'a':
            self.run_add_page()

        elif response == 'b':
            self.run_search_page()

        else:
            self._clear_screen()
            self._quit()

    def _is_response_valid_add_page(self, response, prompt):
        if prompt != 'Additional Notes' and response.strip() == '':
            return False

        if prompt == '# of Minutes' and re.search(r'[^0-9]', response) != None:
            return False

        return True

    def _get_error_message_add_page(self, response, prompt):
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
        prompts = [{'label': "Task Name", 'model': 'task_name'}, {'label': "# of Minutes", 'model': 'time_amt'}, {'label':"Additional Notes", 'model': 'notes'}]
        output = {}

        # 1. Walk through each prompt and store value in output
        for prompt in prompts:
            correct = False
            while not correct:
                self._clear_screen()
                self.view_service.get_add_page(prompt['label'])

                if sys.version_info < (3, 0):
                    response = raw_input("> ").strip().lower()
                else:
                    response = input("> ").strip().lower()

                if not self._is_response_valid_add_page(response, prompt['label']):
                    self.view_service.error_message = self._get_error_message_add_page(response, prompt['label'])
                    continue

                output[prompt['model']] = response
                correct = True

        output['date'] = datetime.datetime.now().strftime('%d-%m-%Y')

        # 2. Store / append output in csv
        with open("work_log.csv", "a" ) as csvFile:
            csvHeaders = ['date'] + [x['model'] for x in prompts]
            csvWriter = csv.DictWriter(csvFile, fieldnames=csvHeaders)

            if self._file_is_empty(csvFile):
                csvWriter.writeheader()
            csvWriter.writerow(output)

        self.run_display_page('add_page', [output])

    def _is_response_valid_search_page(self, response, menu):
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

    def _get_error_message_search_page(self, response, menu):
        # 1. if menu is empty, then set menu is empty error
        if len(menu) == 0:
            error_message = "Sorry. There are no items in menu. Please exit program (Ctrl + c) and try again."

        # 2. if menu has value other than what's available, set value error
        if not len(response) == 1 or not (ord(response) >= 97 and ord(response) < 97 + len(menu)):
            error_message = "Please enter correct value ({}-{})".format(chr(97), chr(97 + len(menu) - 1))

        return error_message

    def _get_csv_data(self):
        return self.model_service.get_csv_data()

    def _get_error_message_search_by_date_page(self, response, message_type):
        output = ''

        if message_type == 'empty_data':
            output = 'CSV data is empty. Please return to main (R), and add an item.'

        elif message_type == 'not_valid_response':
            # 1. check if correct format has been registered
            if not response or len(response) == 0 or re.match(r'\d{2}\-\d{2}\-\d{4}', response.strip()) is None:
                output = 'Please enter item in correct format (dd-mm-yyyy) or value (R)'
            else:
                day,month,year = response.split('-')
                try:
                    datetime.datetime(int(year),int(month),int(day))
                except ValueError as e:
                    output = str(e).capitalize()

        elif message_type == 'empty_results':
            output = 'Retrieved result is empty.'

        return output

    def _is_response_valid_search_by_date_page(self, response):
        #1. check if response is non-empty
        if not response or len(response) == 0:
            return False

        #2. if response is a single letter, then check to see if it has entered correct value corresponding menu
        if len(response) == 1:
            if response != 'R':
                return False
            return True
        #3. if response is in date format, then check to see if it has a correct value
        elif re.match(r'\d{2}\-\d{2}\-\d{4}', response) is not None:
            day,month,year = response.split('-')
            try:
                datetime.datetime(int(year),int(month),int(day))
            except ValueError:
                return False

            return True
        #4. for other cases, return False
        else:
            return False

    def run_search_by_date_page(self):
        self.view_service.page_title = 'Search Page'
        data = self._get_csv_data()
        exit_page = False
        items = []

        if len(data.strip()) == 0:
            self.view_service.error_message = self._get_error_message_search_by_date_page('', 'empty_data')

        while not exit_page:
            # 1. Clear screen
            self._clear_screen()

            #2. Load page
            self.view_service.get_search_by_date_page()

            #3. Load prompt
            if sys.version_info < (3, 0):
                response = raw_input("> ").strip()
            else:
                response = input("> ").strip()

            #4. if data not empty and response typed, check and see if typed value is correct
            if not self._is_response_valid_search_by_date_page(response):
                self.view_service.error_message = self._get_error_message_search_by_date_page(response, 'not_valid_response')
                continue

            # By this point, the response should be in the format of dd-mm-yyyy or R
            # 5. if response is 'R', then return to search page
            if response == 'R':
                exit_page = True
                continue

            #6. If data is empty, then raise error saying data is empty, so try again once it has been added
            if len(data.strip()) == 0:
                self.view_service.error_message = self._get_error_message_search_by_date_page('', 'empty_data')
                continue

            # 7. If not r and date in correct format, then grab all items by the date
            results = re.finditer(r'''
                ^(?P<date>{})\,
                (?P<task_name>.*)\,
                (?P<time_amt>\d+)\,
                (?P<notes>.*)\r$
            '''.format(response), data, re.X|re.M)

            items = [x.groupdict() for x in results]

            # 8. Once grabbed, check and see if it has length equal to zero. If so, then raise error saying nothing found
            if len(items) == 0:
                self.view_service.error_message = self._get_error_message_search_by_date_page(response, 'empty_results')
                continue

            exit_page = True

        #8. bring data to display page
        if response == 'R':
            self.run_search_page()
        else:
            self.run_display_page('search_page', items)

    def _sanitize_response(self, response):
        # for each reserved character, replace it with \Character or \s if it's a space
        reserved_chrs = ['.','^',' ', '$', '*', '+', '?', '|']

        for character in reserved_chrs:
            if character in response:
                response = re.sub('', '\{}'.format(character) if character != ' ' else '\s', response)
        return response

    def run_search_by_exact_search_page(self):
        self.view_service.page_title = 'Search Page'
        data = self._get_csv_data()
        exit_page = False
        items = []

        if len(data.strip()) == 0:
            self.view_service.error_message = self._get_error_message_search_by_exact_search_page('', 'empty_data')

        while not exit_page:
            # 1. Clear screen
            self._clear_screen()

            #2. Load page
            self.view_service.get_search_by_exact_search_page()

            #3. Load prompt
            if sys.version_info < (3, 0):
                response = raw_input("> ").strip()
            else:
                response = input("> ").strip()

            #4. if data not empty and response typed, check and see if typed value is correct
            if not self._is_response_valid_search_by_exact_search_page(response):
                self.view_service.error_message = self._get_error_message_search_by_exact_search_page(response, 'not_valid_response')
                continue

            # 5. if response is 'R', then return to search page
            if response == 'R':
                exit_page = True
                continue

            #6. If data is empty, then raise error saying data is empty, so try again once it has been added
            if len(data.strip()) == 0:
                self.view_service.error_message = self._get_error_message_search_by_exact_search_page('', 'empty_data')
                continue

            # 8. Sanitize response if it has regex reserved characters
            response = self._sanitize_response(response)

            # 7. Grab all results by exact string in task name or notes
            # results = re.finditer(r'''
            #     ^(?P<date>\d{{2}}\-\d{{2}}\-\d{{4}})\,
            #     (?P<task_name>.*)\,
            #     (?P<time_amt>{})\,
            #     (?P<notes>.*)\r$
            # '''.format(response), data, re.X|re.M)

            # items = [x.groupdict() for x in results]

            # 8. Once grabbed, check and see if it has length equal to zero. If so, then raise error saying nothing found
            if len(items) == 0:
                self.view_service.error_message = self._get_error_message_search_by_exact_search_page(response, 'empty_results')
                continue

            exit_page = True

        #8. bring data to display page
        if response == 'R':
            self.run_search_page()
        else:
            self.run_display_page('search_page', items)


    def _is_response_valid_search_by_time_page(self, response):

        #1. check if response is non-empty
        if not response or len(response) == 0:
            return False

        #2. if response is a single letter, then check to see if it has entered correct value corresponding menu
        if len(response) == 1 and response.strip() == 'R':
            return True

        #3. if response is in time spent, then check to see if it has a correct value
        if len(response) > 0 and response.strip() != 'R':
            try:
                int(response)
                return True
            except ValueError:
                return False

        #4. for other cases, return False
        return False


    def _get_error_message_search_by_time_spent_page(self, response, message_type):
        output = ''

        if message_type == 'empty_data':
            output = 'CSV data is empty. Please return to main (R), and add an item.'

        if message_type == 'not_valid_response':
            output = 'Please enter item in correct format (non-negative integer) or value (R)'

        if message_type == 'empty_results':
            output = 'Retrieved result is empty.'

        return output

    def run_search_by_time_spent_page(self):
        self.view_service.page_title = 'Search Page'
        data = self._get_csv_data()
        exit_page = False
        items = []

        if len(data.strip()) == 0:
            self.view_service.error_message = self._get_error_message_search_by_time_spent_page('', 'empty_data')

        while not exit_page:
            # 1. Clear screen
            self._clear_screen()

            #2. Load page
            self.view_service.get_search_by_time_spent_page()

            #3. Load prompt
            if sys.version_info < (3, 0):
                response = raw_input("> ").strip()
            else:
                response = input("> ").strip()

            #4. if data not empty and response typed, check and see if typed value is correct
            if not self._is_response_valid_search_by_time_page(response):
                self.view_service.error_message = self._get_error_message_search_by_time_spent_page(response, 'not_valid_response')
                continue

            # 5. if response is 'R', then return to search page
            if response == 'R':
                exit_page = True
                continue

            #6. If data is empty, then raise error saying data is empty, so try again once it has been added
            if len(data.strip()) == 0:
                self.view_service.error_message = self._get_error_message_search_by_time_spent_page('', 'empty_data')
                continue

            # 7. If not r and date in correct format, then grab all items by the date
            results = re.finditer(r'''
                ^(?P<date>\d{{2}}\-\d{{2}}\-\d{{4}})\,
                (?P<task_name>.*)\,
                (?P<time_amt>{})\,
                (?P<notes>.*)\r$
            '''.format(response), data, re.X|re.M)

            items = [x.groupdict() for x in results]

            # 8. Once grabbed, check and see if it has length equal to zero. If so, then raise error saying nothing found
            if len(items) == 0:
                self.view_service.error_message = self._get_error_message_search_by_time_spent_page(response, 'empty_results')
                continue

            exit_page = True

        #8. bring data to display page
        if response == 'R':
            self.run_search_page()
        else:
            self.run_display_page('search_page', items)

    def run_search_by_date_page(self):
        self.view_service.page_title = 'Search Page'
        data = self._get_csv_data()
        exit_page = False
        items = []

        if len(data.strip()) == 0:
            self.view_service.error_message = self._get_error_message_search_by_date_page('', 'empty_data')

        while not exit_page:
            # 1. Clear screen
            self._clear_screen()

            #2. Load page
            self.view_service.get_search_by_date_page()

            #3. Load prompt
            if sys.version_info < (3, 0):
                response = raw_input("> ").strip()
            else:
                response = input("> ").strip()

            #4. if data not empty and response typed, check and see if typed value is correct
            if not self._is_response_valid_search_by_date_page(response):
                self.view_service.error_message = self._get_error_message_search_by_date_page(response, 'not_valid_response')
                continue

            # By this point, the response should be in the format of dd-mm-yyyy or R
            # 5. if response is 'R', then return to search page
            if response == 'R':
                exit_page = True
                continue

            #6. If data is empty, then raise error saying data is empty, so try again once it has been added
            if len(data.strip()) == 0:
                self.view_service.error_message = self._get_error_message_search_by_date_page('', 'empty_data')
                continue

            # 7. If not r and date in correct format, then grab all items by the date
            results = re.finditer(r'''
                ^(?P<date>{})\,
                (?P<task_name>.*)\,
                (?P<time_amt>\d+)\,
                (?P<notes>.*)\r$
            '''.format(response), data, re.X|re.M)

            items = [x.groupdict() for x in results]

            # 8. Once grabbed, check and see if it has length equal to zero. If so, then raise error saying nothing found
            if len(items) == 0:
                self.view_service.error_message = self._get_error_message_search_by_date_page(response, 'empty_results')
                continue

            exit_page = True

        #8. bring data to display page
        if response == 'R':
            self.run_search_page()
        else:
            self.run_display_page('search_page', items)

    def run_search_page(self):
        self.view_service.page_title = 'Search Page'

        exit_page = False
        menu = self.model_service.get_menu('search_page')

        while not exit_page:
            self._clear_screen()
            self.view_service.get_search_page(menu)

            if sys.version_info < (3, 0):
                response = raw_input("> ").strip().lower()
            else:
                response = input("> ").strip().lower()

            if not self._is_response_valid_search_page(response, menu):
                self.view_service.error_message = self._get_error_message_search_page(response, menu)
                continue

            exit_page = True

        if response == 'a':
            self.run_search_by_date_page()

        elif response == 'b':
            self.run_search_by_time_spent_page()

        elif response == 'c':
            self.run_search_by_exact_search_page()

        elif response == 'd':
            self.run_find_by_the_pattern_page()

        elif response == 'e':
            self._clear_screen()
            self.run_main_page()


    def _is_response_valid_display_page(self, response, path):
        if path == 'search_page':
            choices = ['N','P','R']
        else:
            choices = ['R']

        # if the response is empty, warn user to type the correct value
        if response not in choices:
            return False
        return True

    def _get_error_message_display_page(self, response, path):
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
            self._clear_screen()
            self.view_service.get_display_page(path, items, index)

            if sys.version_info < (3, 0):
                response = raw_input("> ").strip()
            else:
                response = input("> ").strip()

            if not self._is_response_valid_display_page(response, path):
                self.view_service.error_message = self._get_error_message_display_page(response, path)
                continue

            if response == 'N':
                if len(items) == 0 or index == len(items) - 1:
                    continue
                else:
                    index = index + 1 if (index+1) < len(items) else index

            elif response == 'P':
                if len(items) == 0 or index == 0:
                    continue
                else:
                    index = index - 1 if (index - 1) >= 0 else index

            elif response == 'R':
                exit_page = True

        if response == 'R':
            self._clear_screen()
            self.run_search_page() if path == 'search_page' else self.run_main_page()

if __name__ == "__main__":
    program = Program()
    program.run_main_page()