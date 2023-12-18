import json


class Upgrade():

    def __init__(self):
        self.current_rules_filepath = None
        self.new_rules_filepath = None
        self.output_new_rules_filepath = None
        self.current_rules = []
        self.new_rules = []
        self.output_new_rules = []
        self.rule_keys = [] # Store a unique list of keys from the new rules.
        self.DEBUG = True

    def set_current_rules_filepath(self, filepath=None):
        try:
            self.current_rules_filepath = filepath
            self.current_rules = self.load_rules_file(filepath=filepath)
        except Exception as e:
            print(e)

    def set_new_rules_filepath(self, filepath=None):
        try:
            self.new_rules_filepath = filepath
            self.new_rules = self.load_rules_file(filepath=filepath)
        except Exception as e:
            print(e)

    def load_rules_file(self, filepath=None):
        try:
            rules = []
            print(filepath)
            with open(filepath) as f:
                for line in f.readlines():
                    rules.append(json.loads(line))
            return rules
        except Exception as e:
            print(e)

    def output_rules_file(self, filepath=None):
        try:
            print(filepath)
            f = open(filepath, "w")
            for line in self.output_new_rules:
                f.write("{0}\n".format(json.dumps(line)))
            f.close()
            # with open(filepath) as f:
            #     for line in self.output_new_rules:
            #         f.write(json.dumps(line))
        except Exception as e:
            print(e)

    def get_current_rule(self, new_rule=None):
        try:
            # Use the rule name to get the current/previous version of the rule.
            for current_rule in self.current_rules:
                if "name" in current_rule and "name" in new_rule and self.sanitise_rule_name(current_rule["name"]) == self.sanitise_rule_name(new_rule["name"]):
                    return current_rule
        except Exception as e:
            print(e)

    def search_rules_file(self, rules=None):
        try:
            for new_rule in self.new_rules:
                new_rule = self.set_timesamp_override(rule=new_rule)
                if "name" in new_rule:

                    for key in new_rule.keys():
                        if key not in self.rule_keys:
                            self.rule_keys.append(key)

                    if self.DEBUG:
                        if "alert_suppression" in new_rule:
                            print(new_rule["alert_suppression"])

                    # Remove [Duplicate] from rule name.
                    new_rule_name = self.sanitise_rule_name(name=new_rule["name"])

                    new_rule["name"] = new_rule_name
                    current_rule = self.get_current_rule(new_rule=new_rule)
                    if current_rule is not None:

                        # Transfer the index settings.
                        if "index" in new_rule and "index" in current_rule:
                            new_rule["index"] = current_rule["index"]

                        # Transfer the actions
                        if "actions" in new_rule and "actions" in current_rule:
                            new_rule["actions"] = current_rule["actions"]

                        # Transfer the rule exceptions.
                        if "exceptions_list" in new_rule and "exceptions_list" in current_rule:
                            new_rule["exceptions_list"] = current_rule["exceptions_list"]

                        # If it's an ML rule, transfer the settings specific to ML rules.
                        if "anomaly_threshold" in new_rule and "anomaly_threshold" in current_rule:
                            new_rule["anomaly_threshold"] = current_rule["anomaly_threshold"]

                        if "machine_learning_job_id" in new_rule and "machine_learning_job_id" in current_rule:
                            new_rule["machine_learning_job_id"] = current_rule["machine_learning_job_id"]

                        # Unique append tags from current rule to new rule.
                        # Custom tags set by the user will get transferred to the new rule.
                        if "tags" in new_rule and "tags" in current_rule:
                            for tag in current_rule["tags"]:
                                if tag not in new_rule["tags"]:
                                    new_rule["tags"].append(tag)

                        # Transfer false positive settings
                        if "false_positives" in new_rule and "false_positives" in current_rule:
                            new_rule["false_positives"] = current_rule["false_positives"]

                        # Transfer the description if the new rule description is empty
                        # and the user set a custom description in the current rule.
                        if "description" in new_rule and "description" in current_rule:
                            if new_rule["description"].strip() == "" and current_rule["description"].strip() != "":
                                new_rule["description"] = current_rule["description"]

                        # Transfer the description if the new rule description is empty
                        # and the user set a custom description in the current rule.
                        if "description" in new_rule and "description" in current_rule:
                            if new_rule["description"].strip() == "" and current_rule["description"].strip() != "":
                                new_rule["description"] = current_rule["description"]

                        # Transfer the investigation guide from the current rule to the new rule.
                        # Do this when the investigation guide in the new rule is empty
                        # and the user set a custom investigation guide in the current/previous rule.
                        if "note" in new_rule and "note" in current_rule:
                            if new_rule["note"].strip() == "" and current_rule["note"].strip() != "":
                                new_rule["note"] = current_rule["note"]

                        # Add references set by the user to the new rule.
                        # This is done by transferring references from the current rule to the new rule.
                        if "references" in new_rule and "references" in current_rule:
                            for reference in current_rule["references"]:
                                if reference not in new_rule["references"]:
                                    new_rule["references"].append(reference)

                        # Transfer timeline settings.
                        if "timeline_id" in new_rule and "timeline_id" in current_rule:
                            new_rule["timeline_id"] = current_rule["timeline_id"]

                        if "timeline_title" in new_rule and "timeline_title" in current_rule:
                            new_rule["timeline_title"] = current_rule["timeline_title"]

                        # Transfer the custom highlighted fields.
                        if "investigation_fields" in new_rule and "investigation_fields" in current_rule:
                            new_rule["investigation_fields"] = current_rule["investigation_fields"]

                        # Transfer the alert suppression fields.
                        if "alert_suppression" in new_rule and "alert_suppression" in current_rule:
                            new_rule["alert_suppression"] = current_rule["alert_suppression"]

                        # timestamp override fallback setting.
                        if "timestamp_override_fallback_disabled" in new_rule and "timestamp_override_fallback_disabled" in current_rule:
                            new_rule["timestamp_override_fallback_disabled"] = current_rule["timestamp_override_fallback_disabled"]

                        if "rule_name_override" in new_rule and "rule_name_override" in current_rule:
                            new_rule["rule_name_override"] = current_rule["rule_name_override"]

                        if "event_category_override" in new_rule and "event_category_override" in current_rule:
                            new_rule["event_category_override"] = current_rule["event_category_override"]

                        # Transfer enabled setting
                        if "enabled" in new_rule and "enabled" in current_rule:
                            new_rule["enabled"] = current_rule["enabled"]

                        # Only output rules in the current_rules file, not all elastic pre-built rules.
                        self.output_new_rules.append(new_rule)

            if self.DEBUG:
                print(self.rule_keys)

        except Exception as e:
            print(e)

    def sanitise_rule_name(self, name=None):
        try:
            if isinstance(name, str):
                return name.replace("[Duplicate]", "").strip()
            return name
        except Exception as e:
            print(e)

    def set_timesamp_override(self, rule):
        try:
            if isinstance(rule, dict) and "timestamp_override" in rule:
                rule["timestamp_override"] = "event.ingested"
            return rule
        except Exception as e:
            print(e)






