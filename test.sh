#!/bin/sh
set -ex
export PATH="$(dirname $(realpath $0))/bin:$PATH"
xd --version
nosetests
