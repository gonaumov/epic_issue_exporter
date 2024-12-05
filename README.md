# Epic issue exporter 

I needed to have a report which the hours of original estimates and other informations 
for a Jira Epic. I ended with imlmenetation of a Python script using Jira API 
which I am sharing here in case someone has a similar problem in the future. 

I order main.py to work properly there is need JIRA_SERVER, TOKEN_AUTH and EPIC_KEY
environment variables to be specified. You can build the report by running main.py