class ViewService:
    def __init__(self):
        self.error_message = ''
        self.page_title = ''

    def _get_header(self):
        print("Work Log ({})\n".format(self.page_title))

    def _get_error_message(self):
        if self.error_message:
            print("Error: {}".format(self.error_message))
            print("Please try again:")

    def get_main(self, menu_items):
        self._get_header()

        print("Please select an item from menu\n")

        for index,item in enumerate(menu_items):
            if index != len(menu_items) - 1:
                print("{0}. {1}".format(chr(index+97), item))
            else:
                print("{0}. {1}\n".format(chr(index+97), item))

        self._get_error_message()


    def get_add(self, prompt):
        self._get_header()

        print("Please enter value to the following\n")

        print ("{}:\n".format(prompt))

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

