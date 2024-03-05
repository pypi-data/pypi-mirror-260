# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cg_flake8_reporter']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=6.0.0,<7.0.0']

entry_points = \
{'flake8.report': ['cg-flake8-reporter = cg_flake8_reporter:CustomFormatter']}

setup_kwargs = {
    'name': 'cg-flake8-reporter',
    'version': '1!1.0.1',
    'description': '',
    'long_description': "# cg-flake8-reporter\n\nA Flae8 reporter plugin for CodeGrade AutoTest v2.\n\nThis plugin writes messages to CodeGrade AutoTest v2's structured output channel.\nFor each violation Flake8 reports, a `comments` message is written as described\nin CodeGrade's documentation. When Flake8 finishes its analysis, a final message\nis written with the amount of points that were achieved in the code quality run.\n\n## Configuration\n\nIn order to use the custom reporter, make sure you have installed both Flake8\nand this package:\n\n```bash\npython3 -m pip install flake8==6.0.0\npython3 -m pip install cg-flake8-reporter\n```\n\nThis reporter is registered with Flake8 as `cg-flake8-reporter`, to use it run\nflake with the option `--format=cg-flake8-reporter`.\n\nThe custom reporter adds a few new options to Flake8: `cg-points-deducted`,\n`cg-flake8-fd` and `cg-base-path`.\n\n### cg-points-deducted\n\nThe `cg-points-deducted` option makes it possible to configure the amount of\npoints (in percentage) that each violation deducts from the total points.\n\nThe `cg-points-deducted` expectes a string in the following format as input:\n\n```bash\n'info:<percentage>,warning:<percentage>,error:<percentage>'\n```\n\nEach of the violation levels must be present in the provided string. The\npercentage provided should be an integer number **without** the `%` symbol.\n\nIf you wish for a violation level to not deduct points, simply set it to `0`.\n\n### cg-flake8-fd\n\nThe `cg-flake8-fd` option makes it possible to configure where the reporter\nwill write its output. By default, the value is `1`, which means the reporter\nwill write to `stdout`. Within AutoTest v2 it is recommended to use file\ndescriptor `3` so that the comments will be visible in CodeGrade's UI. The\n_Flake8_ step will already set this up for you.\n\n### cg-base-path\n\nThe `cg-base-path` allows you to restrict which files the reporter will report.\nFor example, if you only want files to be reported within the `server` directory\nof the student, you may want to set `--cg-base-path=~/student/server/`. Beware,\nthe _Flake8_ step always sets `cg-base-path` to the root of the student's\nworkspace. If you want to customize this, you should use a _Custom Test_ step\ninstead.\n\n### cg-code-prefix-mapping\n\nThe `cg-code-prefix-mapping` options allows you to create a custom mapping\nbetween error code prefixes and severities. The code prefixes are groups of errors.\nThe option expects a string in the following format:\n```bash\n'_prefix_:_severity_,_prefix_2_:_severity_2_,...'\n```\n\nThe normal mapping can be represented as follows:\n```bash\n'F:error,E:error,W:warning:C:info,N8:info'\n```\n\nThe standard mapping will always be set, however you can overwrite existing\nkeys with new values should you want this.\n\nThis mapping also allows you to use libraries that introduce new error types,\nwhich will use a different, unknown code prefix.\n\n### cg-default-severity\n\nThe `cg-default-severity` option will set provide a fallback severity, when we\nhave checked the default mapping, (plus your supplied mapping,) and could not\nfind any set severity for the code prefix.\n\nFor example, when we install a library that adds error codes in the form of\n`D...`, where the dots are the actual error code numbers. We will search for\nan entry in the severity mapping, and fallback to the default if we cannot find\nanything.\n\nThe default value for this option is: 'unset', which means that there can be\nno deduction for this type of code, and will not get flagged as categorised\nerrors.\n\n\n## Usage\n\nTo run Flake8 with the custom reporter:\n\n```bash\npython3 -m flake8 \\\n    --format=cg-flake8-reporter \\\n    --cg-points-deducted='info:1,warning:3,error:5,unknown:0' \\\n    --cg-flake8-fd=1 \\\n    ./\n```\n\nTo run flake8 when having a library installed that adds error codes with prefix `D`\nand assign the `info` severity to each error starting with a `D`:\n\n```bash\npython3 -m flake8 \\\n    --format=cg-flake8-reporter \\\n    --cg-points-deducted='info:1,warning:3,error:5,unknown:0' \\\n    --cg-code-prefix-mapping='D:info' \\\n    --cg-flake8-fd=1 \\\n    ./\n```\n",
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
