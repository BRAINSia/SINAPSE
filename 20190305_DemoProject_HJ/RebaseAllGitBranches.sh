#!/bin/bash
# \author Hans J. Johnson

for i in $(git for-each-ref --format='%(refname:short)' refs/heads/); do  
    git branch --set-upstream-to=origin/master --track  $i; 
    git checkout $i; 
    git fetch; 
    git rebase origin/master  || git rebase --abort;
done


git checkout master

git branch -v
