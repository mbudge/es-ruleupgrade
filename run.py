import os
from upgrade import Upgrade

class Run():

    def __init__(self):
        pass

    def run(self):
        upgrade = Upgrade()

        # Get the current directory
        current_directory = os.getcwd()

        # Create new rule file paths
        current_rules_path = os.path.join(current_directory, "rules-files/current_rules.ndjson")
        new_rules_path = os.path.join(current_directory, "rules-files/new_rules.ndjson")

        upgrade.set_current_rules_filepath(current_rules_path)
        upgrade.set_new_rules_filepath(new_rules_path)

        upgrade.current_rules = upgrade.search_rules_file(rules=upgrade.current_rules)

        upgrade.output_rules_file(os.path.join(current_directory, "output_new_rules.ndjson"))

if __name__ == '__main__':
    run = Run()
    run.run()

