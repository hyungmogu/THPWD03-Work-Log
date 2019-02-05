class ModelService:
    menu_main = ["Add Entry", "Search Existing Entry", "Quit"]
    menu_search_page = ["Find By Date", "Find by Time Spent", "Find by Exact Search", "Find by Pattern", "Return to Main"]

    def get_menu(self, name):
        output = []

        if hasattr(self, 'menu_{}'.format(name)):
            output = getattr(self, 'menu_{}'.format(name))

        return output

    def get_csv_data(self):
        try:
            with open('work_log.csv','r') as csvFile:
                output = csvFile.read()
        except IOError:
            output = ''

        return output
