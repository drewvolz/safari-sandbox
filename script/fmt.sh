#!/bin/sh

root_dir="$(dirname $0)/.."

set -x

yapf -r $root_dir/*.py $root_dir/safarisandbox -vv --in-place
