# catalog-plugin
This repository contains Catalog plugin for the Pearson OpenEdX platform.

## Installation

#### Using Devstack

* Clone this repository in the src folder of your devstack.
* Open a new LMS shell.
* Install the plugin as follows: pip install -e /path/to/your/src/folder/catalog-plugin
* Restart LMS service.

#### Using Tutor

```bash
git clone git@github.com:Pearson-Advance/catalog-plugin.git "$(tutor config printroot)/env/build/openedx/requirements/catalog-plugin"
echo "-e ./catalog-plugin" >> "$(tutor config printroot)/env/build/openedx/requirements/private.txt"
```

Then run `tutor config save`, `tutor images build openedx` and `tutor local launch`.

### How to run tests

- Run the command `make test && make quality`  # Or run make validate to run both.

#### Update Version

- Run ``bump-my-version bump [type of change: e.g: minor]``
- Verify the version in `catalog_plugin/__init__.py` and `pyproject.toml`
- Update the `CHANGELOG.md`

### License

The code in this repository is licensed under version 2.0 of the Apache unless otherwise noted.
