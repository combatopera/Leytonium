#!/bin/bash

#HALP Show list of branches and outgoing changes.

set -e

clear

git branch -vv

git status -v
