# Copyright (c) 2023 Ho Kim (ho.kim@ulagbulag.io). All rights reserved.
# Use of this source code is governed by a license
# that can be found in the LICENSE file.

clean:
    # Clean up all iPython outputs
    find . -name '*.ipynb' -exec jupyter nbconvert --clear-output --inplace {} \;

lint:
    pylint $(git ls-files '*.py')

release:
    python -m build . --sdist
    twine upload "dist/kubegraph-$(cat pyproject.toml | grep -Po '^version *\= *\"\K[0-9.]+').tar.gz"
