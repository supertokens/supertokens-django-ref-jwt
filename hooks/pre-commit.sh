#!/bin/bash

# checks if locally staged changes are
# formatted properly. Ignores non-staged
# changes.
# Intended as git pre-commit hook

#COLOR CODES:
#tput setaf 3 = yellow -> Info
#tput setaf 1 = red -> warning/not allowed commit
#tput setaf 2 = green -> all good!/allowed commit

echo ""
echo "$(tput setaf 3)Running pre-commit hook ... (you can omit this with --no-verify, but don't)$(tput sgr 0)"

no_of_files_to_stash=`git ls-files . --exclude-standard --others -m | wc -l`
if [ $no_of_files_to_stash -ne 0 ]
then
   echo "$(tput setaf 3)* Stashing non-staged changes"
   files_to_stash=`git ls-files . --exclude-standard --others -m | xargs`
   git stash push -k -u -- $files_to_stash >/dev/null 2>/dev/null
fi

cd scripts && ./check-lint.sh >/dev/null 2>/dev/null
compiles=$?

echo "$(tput setaf 3)* Compiles?$(tput sgr 0)"

if [ $compiles -eq 0 ]
then
   echo "$(tput setaf 2)* Yes$(tput sgr 0)"
else
   echo "$(tput setaf 1)* No$(tput sgr 0)"
fi

if [ $no_of_files_to_stash -ne 0 ]
then
   echo "$(tput setaf 3)* Undoing stashing$(tput sgr 0)"
   git stash apply >/dev/null 2>/dev/null
   if [ $? -ne 0 ]
   then
      git checkout --theirs . >/dev/null 2>/dev/null
   fi
   git stash drop >/dev/null 2>/dev/null
fi

if [ $compiles -eq 0 ]
then
   echo "$(tput setaf 2)... done. Proceeding with commit.$(tput sgr 0)"
   echo ""
   exit 0
else
   echo "$(tput setaf 1)... done.$(tput sgr 0)"
   echo "$(tput setaf 1)CANCELLING commit due to COMPILE ERROR.$(tput sgr 0)"
   echo ""
   exit 2
fi