# Pratik for Python
<div align="center">

[![LassaInora - Pratik](https://img.shields.io/static/v1?label=LassaInora&message=Pratik&color=yellow&logo=github)](https://github.com/LassaInora/Pratik "Go to GitHub repo")
[![GitHub tag](https://img.shields.io/github/tag/LassaInora/Pratik?include_prereleases=&sort=semver&color=orange)](https://github.com/LassaInora/Pratik/releases/)
[![stars - Pratik](https://img.shields.io/github/stars/LassaInora/Pratik?style=social)](https://github.com/LassaInora/Pratik)
[![forks - Pratik](https://img.shields.io/github/forks/LassaInora/Pratik?style=social)](https://github.com/LassaInora/Pratik)

[![PyPI version](https://badge.fury.io/py/pratik.svg)](https://pypi.org/project/Pratik)
[![Supported Versions](https://img.shields.io/pypi/pyversions/pratik.svg)](https://pypi.org/project/Pratik)

___

</div>

<h1 id="1-overview">Overview</h1>
It is a library of various functions and classes helping to program more efficiently and more intuitively

<h1 id="2-summary">Summary</h1>
<details markdown="1">
  <summary>Table of Contents</summary>

-   [1 Overview](#1-overview)
-   [2 Summary](#2-summary)
-   [3 How to use](#3-how_to_use)
    *   [3.1 Installation](#3_1-installation)
    *   [3.2 Librairies](#3_2-librairies)
        +   [3.2.1 package functions](#3_2_1-functions)
            *   [3.2.1.1 Menu](#3_2_1_1-Menu)
            *   [3.2.1.2 enter()](#3_2_1_2-enter)
            *   [3.2.1.3 humanize_number()](#3_2_1_3-humanize_number)
        +   [3.2.2 package singleton](#3_2_2-singleton)
            *   [3.2.2.1 Singleton](#3_2_2_1-Singleton)
        +   [3.2.3 package text](#3_2_3-text)
            *   [3.2.3.1 Color](#3_2_3_1-Color)
            *   [3.2.3.2 Highlight](#3_2_3_2-Highlight)
            *   [3.2.3.3 Style](#3_2_3_3-Style)
            *   [3.2.3.4 generate()](#3_2_3_4-generate)
            *   [3.2.3.5 information()](#3_2_3_5-information)
            *   [3.2.3.6 STOP](#3_2_3_6-STOP)
-   [4 Contributors](#4-contributors)
-   [5 Licence](#5-license)

</details>

<h1 id="3-how_to_use">How to use</h1>

<h2 id="3_1-installation">Installation</h2>

By PyPI:
```bash
python -m pip install pratik
```

<h2 id="3_2-librairies">Librairies</h2>

<h3 id="3_2_1-functions">package functions</h3>

<h4 id="3_2_1_1-Menu">Menu</h4>

```
>> from pratik.functions import Menu
>> menu = Menu("to be", "not to be", title="Question", description="That is the question", back_button="to death", description_center=True)
>> print(menu)
     ╔══════════╗     
╔════╣ Question ╠════╗
║    ╚══════════╝    ║
║     That is the    ║
║      question      ║
╟────────────────────╢
║ ┌───┐┌───────────┐ ║
║ │ 1 ├┤ to be     │ ║
║ └───┘└───────────┘ ║
║ ┌───┐┌───────────┐ ║
║ │ 2 ├┤ not to be │ ║
║ └───┘└───────────┘ ║
╟────────────────────╢
║ ╔═══╗╔═══════════╗ ║ 
║ ║ 0 ╠╣ to death  ║ ║ # This button is in red color
║ ╚═══╝╚═══════════╝ ║
╚════════════════════╝
>> menu.select()
?> 1
>> print(menu)
     ╔══════════╗     
╔════╣ Question ╠════╗
║    ╚══════════╝    ║
║     That is the    ║
║      question      ║
╟────────────────────╢
║ ╔═══╗╔═══════════╗ ║
║ ║ 1 ╠╣ to be     ║ ║ # This button is in red color
║ ╚═══╝╚═══════════╝ ║
║ ┌───┐┌───────────┐ ║
║ │ 2 ├┤ not to be │ ║
║ └───┘└───────────┘ ║
╟────────────────────╢
║ ┌───┐┌───────────┐ ║
║ │ 0 ├┤ to death  │ ║
║ └───┘└───────────┘ ║
╚════════════════════╝
>> menu.selected = 2
>> print(menu)
     ╔══════════╗     
╔════╣ Question ╠════╗
║    ╚══════════╝    ║
║     That is the    ║
║      question      ║
╟────────────────────╢
║ ┌───┐┌───────────┐ ║
║ │ 1 ├┤ to be     │ ║
║ └───┘└───────────┘ ║
║ ╔═══╗╔═══════════╗ ║
║ ║ 2 ╠╣ not to be ║ ║ # This button is in red color
║ ╚═══╝╚═══════════╝ ║
╟────────────────────╢
║ ┌───┐┌───────────┐ ║
║ │ 0 ├┤ to death  │ ║
║ └───┘└───────────┘ ║
╚════════════════════╝
>> menu = Menu("to be", "not to be", title="Question", description="That is the question", back_button="to death")
>> print(menu)
     ╔══════════╗     
╔════╣ Question ╠════╗
║    ╚══════════╝    ║
║ That is the        ║
║ question           ║
╟────────────────────╢
║ ┌───┐┌───────────┐ ║
║ │ 1 ├┤ to be     │ ║
║ └───┘└───────────┘ ║
║ ┌───┐┌───────────┐ ║
║ │ 2 ├┤ not to be │ ║
║ └───┘└───────────┘ ║
╟────────────────────╢
║ ╔═══╗╔═══════════╗ ║
║ ║ 0 ╠╣ to death  ║ ║
║ ╚═══╝╚═══════════╝ ║
╚════════════════════╝
>> menu = Menu("to be", "not to be", title="Question", back_button="to death")
>> print(menu)
     ╔══════════╗     
╔════╣ Question ╠════╗
║    ╚══════════╝    ║
║ ┌───┐┌───────────┐ ║
║ │ 1 ├┤ to be     │ ║
║ └───┘└───────────┘ ║
║ ┌───┐┌───────────┐ ║
║ │ 2 ├┤ not to be │ ║
║ └───┘└───────────┘ ║
╟────────────────────╢
║ ╔═══╗╔═══════════╗ ║
║ ║ 0 ╠╣ to death  ║ ║
║ ╚═══╝╚═══════════╝ ║
╚════════════════════╝
>> menu = Menu("to be", "not to be", title="Question")
>> print(menu)
     ╔══════════╗     
╔════╣ Question ╠════╗
║    ╚══════════╝    ║
║ ┌───┐┌───────────┐ ║
║ │ 1 ├┤ to be     │ ║
║ └───┘└───────────┘ ║
║ ┌───┐┌───────────┐ ║
║ │ 2 ├┤ not to be │ ║
║ └───┘└───────────┘ ║
╚════════════════════╝
>> menu = Menu("to be", "not to be")
>> print(menu)
╔════════════════════╗
║ ┌───┐┌───────────┐ ║
║ │ 1 ├┤ to be     │ ║
║ └───┘└───────────┘ ║
║ ┌───┐┌───────────┐ ║
║ │ 2 ├┤ not to be │ ║
║ └───┘└───────────┘ ║
╚════════════════════╝
>> menu = Menu()
>> print(menu)
The menu is empty.
```

This class simply manages a menu of choice

<h4 id="3_2_1_2-enter">enter(__prompt='', __type=int)</h4>

```
>> from pratik.functions import enter
>> enter("Your number here: ") # default -> int
?> Your number here: 42
42
>> enter()
?> 5
5
>> enter("Result: ", list)
?> Result: FRANCE
['F', 'R', 'A', 'N', 'C', 'E']
>> ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'][enter("Where: ", slice)]
?> Where: 2:6:2
['C', 'E']
```

This function is inspired by the input() function by adding the type of a class in which to return the value

<h4 id="3_2_1_3-humanize_number">humanize_number(__number, __fill_char='.')</h4>

```
>> from pratik.functions import humanize_number
>> print(humanize_number(1234567))
1.234.567
>> print(humanize_number(1234567, ' '))
1 234 567
```

This function helps to display numbers in a way that is easier for a human to read.

<h3 id="3_2_2-singleton">package singleton</h3>

<h4 id="3_2_2_1-Singleton">Singleton</h4>

```python
from pratik.singleton import Singleton

class Foo(Singleton):
    def singleton_init(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    @property
    def var(self):
        return self.var1 + self.var2
```

```
>> f1 = Foo(2, 5)
>> print(f1.var1)
2
>> f2 = Foo()
>> print(f2.var1)
2
>> f3 = Foo(3, 8)
>> print(f1.var1)
3
>> print(f2.var1)
3
>> print(f3.var1)
3
```

Singleton is a class allowing the easy creation of a singleton.</br>
To instantiate it like a regular class you can overwrite the `singleton_init(self, *args, **kwargs)` method.

<h3 id="3_2_3-text">package text</h3>

<h4 id="3_2_3_1-Color">Color</h4>

```python
from pratik.text import Color

print(f"{Color.GREEN}Is good!{Color.STOP}")
print(f"{Color.LIGHT_RED}Is Bad!{Color.STOP}")
print(f"{Color.get_rgb(42, 128, 200)}I don't know!{Color.STOP}")
print(f"{Color.get_hex('#ACAB42')}Meh !{Color.STOP}")
```

To color text

- get_rgb(red, green, blue)
  - Get the ANSI escape sequence for an RGB color.

- get_hex(hexadecimal)
  - Get the ANSI escape sequence for an RGB color.

<h4 id="3_2_3_2-Highlight">Highlight</h4>

```python
from pratik.text import Highlight

print(f"{Highlight.GREEN}Is good!{Highlight.STOP}")
print(f"{Highlight.LIGHT_RED}Is Bad!{Highlight.STOP}")
print(f"{Highlight.get_rgb(42, 128, 200)}I don't know!{Highlight.STOP}")
print(f"{Highlight.get_hex('#ACAB42')}Meh !{Highlight.STOP}")
```

To highlight text

- get_rgb(red, green, blue)
  - Get the ANSI escape sequence for an RGB color.

- get_hex(hexadecimal)
  - Get the ANSI escape sequence for an RGB color.

<h4 id="3_2_3_3-Style">Style</h4>

To stylize text. (Bold, Italic, ...)

<h4 id="3_2_3_4-generate">generate(*code)</h4>

```python
from pratik.text import generate

print(f"{generate(31, 45)}It's too much!{generate(0)}")
```

For concat too many codes.

<h4 id="3_2_3_5-information">information()</h4>

All ANSI code in table

<h4 id="3_2_3_6-STOP">STOP</h4>

Reset the ANSI sequence with \033[0m character .

<h1 id="4-contributors">Contributors</h1>

- [Axelle V.](https://github.com/LassaInora)
  + [lassa.inora@gmail.com](mailto:lassa.inora@gmail.com)
  + [Discord](https://discord.gg/SBsCxyTDqc)

<h1 id="5-license">Licence</h1>

This library is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE)
