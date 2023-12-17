
Export the current duplicated elastic pre-built rules 
Put the current rules file in rules-file/current_rules.ndjson

In a different space download/upgrade and duplicate the elastic rules
Export the updated elastic rules
Put the new rules file in rules-file/new_rules.ndjson

python3 run.py

Select rules with the "elastic" tag and do a bulk delete
Import the output_new_rules.ndjson back into the Kibana space