#!/bin/bash

ref=$1
targ=$2

for ref_file in $(find ${ref} -type f | fgrep -v .rda |fgrep -v pyc |fgrep -v .svn | fgrep -v .git | fgrep -v CVS|fgrep -v "\~" |fgrep -v "cmake-build-" |fgrep -v "node_modules" |fgrep -v .idea ); do
  if [ -f stop ]; then
    echo "Stop file found, so not continuing."
    exit -1;
  fi
  targ_file=$(echo ${ref_file} |sed "s#${ref}#${targ}#g" )
  if [ -f ${targ_file} ]; then
    diff -b ${ref_file}  ${targ_file}
    status=$?
    if [ $status -ne 0 ] && [ ! -f stop ]; then
      echo "${ref_file} --> ${targ_file}"
#      vimdiff ${ref_file} ${targ_file}
      vimdiff -c 'set diffopt+=iwhite' ${ref_file} ${targ_file}
    fi
  else
    echo "File not found: ${targ_file}."
    echo "Try:  cp ${ref_file} ${targ_file}"
  fi
done
