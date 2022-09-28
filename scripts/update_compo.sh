#!/bin/sh
echo "Which component do you want to update"
read component
function git_update_component()
{
    echo "Updating component $1"
    git add ./components/$1.py ./Tests/components/$1
    echo "Updates of component $1 and its tests are ready to be commited"
    git commit -m "New Updates of component $1 and tests on its classes"
    git push
    
}
git_update_component $component