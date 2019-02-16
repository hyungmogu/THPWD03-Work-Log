class ViewService:
    def __init__(self):
        self.error_message = ''
        self.page_title = ''

    def _get_header(self):
        print("Work Log ({})\n".format(self.page_title))

    def _get_error_message(self):
        if self.error_message:
            print("Error: {}".format(self.error_message))
            print("Please try again:\n")

    def clear_error_message(self):
        self.error_message = ''

    def get_main_page(self, menu_items):
        self._get_header()

        print("Please select an item from menu\n")

        for index,item in enumerate(menu_items):
            if index != len(menu_items) - 1:
                print("{0}. {1}".format(chr(index+97), item))
            else:
                print("{0}. {1}\n".format(chr(index+97), item))

        self._get_error_message()


    def get_add_page(self, prompt_phrase):
        self._get_header()

        print("Please enter value to the following\n")

        print ("{}:\n".format(prompt_phrase))

        self._get_error_message()

    def get_search_page(self, menu_items):
        self._get_header()

        print ("Please select one of the following options\n")

        for index,item in enumerate(menu_items):
            if index != len(menu_items) - 1:
                print("{0}. {1}".format(chr(index+97), item))
            else:
                print("{0}. {1}\n".format(chr(index+97), item)) # this is to add extra space for prompt

        self._get_error_message()

    def get_search_by_date_page(self):
        self._get_header()

        print("Please enter full date (dd-mm-yyyy):\n")

        print("[R] Return to Search Page\n")

        self._get_error_message()

    def get_search_by_time_spent_page(self):
        self._get_header()

        print("Please enter amount of time (Non-negative integer):\n")

        print("[R] Return to Search Page\n")

        self._get_error_message()

    def get_search_by_exact_search_page(self):
        self._get_header()

        print("Please enter exact string:\n")

        print("[R] Return to Search Page\n")

        self._get_error_message()

    def get_display_page(self, path, items, index):
        self._get_header()
        item = items[index]

        print("Task Name: {}".format(item['task_name']))
        print("Created Date: {}".format(item['date']))
        print("Time Spent: {}".format(item['time_amt']))
        print("Notes: {}\n".format(item['notes']))

        if path == 'search_page':
            print("Displaying Item ({} of {})\n".format(index+1, len(items)))

            if len(items) == 1:
                print("[R] Return to Search Page\n")
            elif index == 0:
                print("[N] Next Item [R] Return to Search Page\n")
            elif index > 0 and index < len(items) - 1:
                print("[N] Next Item [P] Previous Item [R] Return to Search Page\n")
            else:
                print("[P] Previous Item [R] Return to Search Page\n")
        else:
            print("[R] Return to Main Page\n")

        self._get_error_message()

