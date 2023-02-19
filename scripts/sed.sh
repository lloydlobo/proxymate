# !/bin/bash

# To remove a term from a file using bash, you can use the sed command. 
# The basic syntax for the command is:

# Delete a line which has this term: 
cat txt/spock.txt | sed '/- Spock/d'

# cat scripts/spock.txt | sed 's/- Spock/d' | tee txt/spock_sed.txt
# sed -i 's/"- Spock"//g' example.txt

# where:
 # -i flag specifies that the file should be edited in-place #
 # 's/term_to_remove//g' is a sed command to replace all instances of
 # `term_to_remove` with nothing (`''`) 
 # `file.txt` is the name of the file you want to remove the term from.

# So to remove a term from a file called example.txt, you can run the
# following command:

# sed -i 's/term_to_remove//g' example.txt

# Replace term_to_remove with the term you want to remove. Note that
# this command will modify the file in-place, so it's a good idea to make
# a backup copy of the file before running the command.

