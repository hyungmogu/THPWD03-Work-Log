class ModelService:
    menu_main = ["Add Entry", "Search Existing Entry", "Quit"]
    def get_menu(self, name):
        output = []

        if hasattr(self, 'menu_{}'.format(name)):
            output = getattr(self, 'menu_{}'.format(name))

        return output
