# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cg_atv2_python_insert']

package_data = \
{'': ['*']}

install_requires = \
['libcst>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['cg_atv2_python_insert = '
                     'cg_atv2_python_insert.substitution:main']}

setup_kwargs = {
    'name': 'cg-atv2-python-insert',
    'version': '1!1.0.1',
    'description': '',
    'long_description': '# cg_atv2_python_insert\n\nThis package provides functionality to parse a Python script, identify specific\n\'magic comments\', and substitute these comments with code from other files.\nIt\'s designed to be used in environments where code templates and supplementary\nfiles are involved, such as automated grading or code templating systems.\n\nThe script supports command-line interaction, allowing users to specify the\nfile to be processed. It then reads through the specified Python script, looks\nfor magic comments in the format `# CG_INSERT filename`, and replaces these\ncomments with the contents of the referenced file, executing it as part of the\nscript.\n\nThe file to be processed cannot contain any call to `sys.exit()`, `quit()`,\n`exit()`, `os._exit()` or any method that raises the `SystemExit` error.\nThis will raise a `ValueError` if the filled in template is then run.\n\n## Usage:\n\nRun the script from the command line with the filename as an argument.\n\n-   `./example.py`\n\n```python\nfoo = 4\n\n# CG_INSERT other.py\n\nprint (foo+bar)\n\n```\n\n-   `./other.py`\n\n```python\nbar = 3\n```\n\nRunning `python -m cg_atv2_python_insert example.py` results in the following file being generated\n\n-   `./filled_example.py`\n\n```\nfoo = 4\n\ntry:\n    exec(compile(open(\'other.py\').read(), \'other.py\', \'exec\'), globals())\nexcept SystemExit as e:\n    raise ValueError("Call not allowed") from e\n\nprint (foo+bar)\n\n```\n\nIf the filled template is then run, the result printed on screen will be `7`\n\n## Module contains:\n\n-   CLI To generate a python file where each magic comment is substituted by the correct exec call.\n\n# Limitation:\n\nThis module is not intended to handle complex substitutions or manage\ndependencies between inserted scripts. The magic comment needs to be placed at the top level,\noutside of any function or class.\n',
    'author': 'CodeGrade',
    'author_email': 'info@codegrade.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
