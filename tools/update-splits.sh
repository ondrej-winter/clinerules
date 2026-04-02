#!/bin/bash

git subtree split --prefix=python/hexagonal/agents -b split-python-hexagonal-agents
git push --force origin split-python-hexagonal-agents

git subtree split --prefix=python/hexagonal/clinerules -b split-python-hexagonal-clinerules
git push --force origin split-python-hexagonal-clinerules
