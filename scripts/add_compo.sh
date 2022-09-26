#!/bin/sh
echo "Which component do you want to add?"
read component
function git_add_component()
{
    echo "Updating component $1"
    git add ~/projects/PokerParser/components/$1.py ~/projects/PokerParser/Tests/components/$1
    git status
    echo "Updates of component $1 and its tests are ready to be commited"
}
git_add_component $component