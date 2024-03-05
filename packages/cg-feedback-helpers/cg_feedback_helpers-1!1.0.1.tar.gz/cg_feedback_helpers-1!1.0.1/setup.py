# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cg_feedback_helpers', 'cg_feedback_helpers._impl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cg-feedback-helpers',
    'version': '1!1.0.1',
    'description': '',
    'long_description': '# cg_feedback_helpers\n\nThis package provides functionality to provide feedback messages. It\nmainly provides the class `Asserter`. The `Asserter` has a number of\nmethods that are documented on [the official\ndocs](http://feedback-helpers.atv2.codegrade.com/index.html), which allow \nto run assertions. Each assertion can provide either positive or negative\nfeedback. A few helpers are also provided to aid with input and output\ncoupled when running assertions. At the end of a run, call\n`Asserter::emit_success` to guarantee the user receives some feedback\nif everything was correct.\n\nThe package outputs feedback in the following format:\n\n```json\n{\n    "tag": "feedback",\n    "contents": [\n        {\n            "value": <your feedback message>,\n            "sentiment": <"positive" | "negative">\n        },\n    ]\n}\n```\n\n## Usage:\n\nThe following example shows how the asserter can be used to check that\nthe function `greet_user` responds with the correct output to a user\ninput.\n\n```py\nfrom cg_feedback_helpers import asserter, helpers\n\ndef greet_user():\n    name = input()\n    print(f"Hi {name}")\n\n\nwith helpers.capture_output() as buffer, helpers.as_stdin("John"):\n    greet_user()\n\noutput = helpers.get_lines_from_buffer(buffer)\nasserter.has_length(output, 1)\nasserter.equals(output[0], "John")\nasserter.emit_success()\n```\n\nThe output of which will be:\n\n```\n{"tag":"feedback","contents":[{"value":"Got expected length 1","sentiment":"positive"}]}\n{"tag":"feedback","contents":[{"value":"Got expected value Hi John","sentiment":"positive"}]}\n{"tag":"feedback","contents":[{"value":"Everything was correct! Good job!","sentiment":"positive"}]}\n```\n\n## Module contains:\n\n- `Asserter` class, of which the default messages produced can be\n  configured, as well as its failure behavior (either using exceptions\n  or `sys.exit`);\n- `helpers` to make it easier to work with input/output tests.\n\n# Limitation:\n\nThe module currently does not support markdown feedback, nor the\n`neutral` sentiment.\n',
    'author': 'CodeGrade',
    'author_email': 'info@codegrade.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
