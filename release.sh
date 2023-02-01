#!/bin/bash

set -e
NC='\033[0m' RED='\033[0;31m' GREEN='\033[0;32m' BLUE='\033[0;34m' YELLOW='\033[0;33m'

echo -e "${BLUE}----------------- checking project settings -----------------${NC}"
version=$(grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3)
tags=($(git tag -l))
remotes=($(git remote -v | grep fetch | grep -Eo  'https://[^ >]+'))

if [[ " ${tags[*]} " =~ " ${version} " ]]; then
    echo -e "${RED}release '${version}' already exists${NC}"
    exit 1
fi

echo -e "${BLUE}--------------- running tests, lint, coverage ---------------${NC}"
{ fails=$(tox --colored=yes | tee >(grep "exit 1") >&3); } 3>&1
if [ -n "$fails" ]; then
    echo -e "${RED}some of the tests failed, check output${NC}"
    exit 1
fi

echo -e "${BLUE}------------------ building documentation -------------------${NC}"
rm -f ./docs/source/eodhdc.*
make -C ./docs clean
sphinx-apidoc -o ./docs/source/ eodhdc
make -C ./docs html

echo -e "${BLUE}---------------- publishing project, package ----------------${NC}"
git add -- docs reports
git commit -m "update docs, reports" -- docs reports || true
git checkout main
git merge develop -m "update main"
git tag -a "${version}" -m "release ${version}"
git push origin --all
git push origin --tags
git checkout develop
poetry publish --build
