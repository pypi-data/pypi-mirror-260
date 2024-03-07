# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['g29py']

package_data = \
{'': ['*']}

install_requires = \
['hid==1.0.4']

setup_kwargs = {
    'name': 'g29py',
    'version': '0.0.8',
    'description': 'python driver for g29 wheel/pedals',
    'long_description': '# g29py\n> python driver for logitech g29 wheel/pedals\n\n> :warning: **Warning**: g29py is alpha software. This repository is under heavy development and subject to breaking changes. :warning:\n\n![](etc/g29py.jpg)\n\n## Install\n```bash\npip install g29py\n```\n\n## Use\n\n```python\nfrom g29py import G29\ng29 = G29()\n```\n\n```python\n# write \ng29.set_range(500)\ng29.set_friction(0.5)\n```\n\n```python\n# read\ng29.start_pumping() # thread\nwhile 1:\n    state = g29.get_state()\n    print("steering:", state["steering"])\n    print("brake:", state["brake"])\n    print("accelerator", state["accelerator"])\n```\n\n## Read\n\n### Pedals/Steering\n\n| Pedal         | Value Range      | Neutral Position |\n|---------------|------------------|------------------|\n| `steering`    | Float: -1 to 1   | 0 (Centered)     |\n| `accelerator` | Float: -1 to 1   | -1 (Not pressed) |\n| `clutch`      | Float: -1 to 1   | -1 (Not pressed) |\n| `brake`       | Float: -1 to 1   | -1 (Not pressed) |\n\n### Buttons\n\n| Button  | Value |\n|---------|-------|\n| `up`    | 0/1   |\n| `down`  | 0/1   |\n| `left`  | 0/1   |\n| `right` | 0/1   |\n| `X`     | 0/1   |\n| `O`     | 0/1   |\n| `S`     | 0/1   |\n| `T`     | 0/1   |\n| `R2`    | 0/1   |\n| `R3`    | 0/1   |\n| `L2`    | 0/1   |\n| `L3`    | 0/1   |\n| `Share` | 0/1   |\n| `Options` | 0/1 |\n| `+`     | 0/1   |\n| `-`     | 0/1   |\n| `track` | -1/1  |\n| `back`  | 0/1   |\n| `PS`    | 0/1   |\n\n## Write\n\n| Method Name       | Default Parameters                         | Parameter Types                  |\n|-------------------|--------------------------------------------|----------------------------------|\n| `force_constant`  | `val=0.5`                                  | `val`: float                     |\n| `set_friction`    | `val=0.5`                                  | `val`: float                     |\n| `set_range`       | `val=400`                                  | `val`: int                       |\n| `set_autocenter`  | `strength=0.5, rate=0.05`                  | `strength`: float, `rate`: float |\n| `set_anticenter`  | `angle1=180, angle2=180, strength=0.5, reverse=0x0, force=0.5` | `angle1`: int, `angle2`: int, `strength`: float, `reverse`: hexadecimal, `force`: float |\n| `autocenter_off`  | None                                       | None                             |\n| `force_off`       | `slot=0xf3`                                | `slot`: hexadecimal              |\n\n## Sources\n\n- Commands based on nightmode\'s [logitech-g29](https://github.com/nightmode/logitech-g29) node.js driver.\n- Interface uses libhidapi ctype bindings from apmorton\'s [pyhidapi](https://github.com/apmorton/pyhidapi).\n- Reference [wiki-brew](https://wiibrew.org/wiki/Logitech_USB_steering_wheel) for effects API.\n\n## Support\n\nOnly Logitech G29 Driving Force Racing Wheels & Pedals kit supported on linux in ps3 mode.\n\nOn linux, remove sudo requirements by adding udev rule.\n\n```bash\necho \'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"\' \\\n    | sudo tee /etc/udev/rules.d/99-hidraw-permissions.rules\nsudo udevadm control --reload-rules\n```\n',
    'author': 'sean pollock',
    'author_email': 'seanap@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
