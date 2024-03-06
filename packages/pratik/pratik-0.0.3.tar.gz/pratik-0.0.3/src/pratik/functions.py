from pratik.text import Color


class Menu:
    """Managing an interactive menu"""

    def __init__(self, *choices, title=..., description=..., back_button=..., description_center=False):
        self.title = ... if title is ... or title == '' or title.isspace() else title
        self.description = ... if description is ... or description == '' or description.isspace() else description
        self.description_center = description_center
        self.choices = choices
        self.back_button = back_button

        self.selected = 0

    def __len__(self):
        return len(self.choices)

    def __str__(self):
        def get_title():
            if isinstance(self.title, str):
                line1 = f"  ╔═{'═' * len(self.title)}═╗  ".center(width) + "\n"
                line2 = "╔" + f"═╣ {self.title} ╠═".center(width - 2, '═') + "╗\n"
                line3 = "║" + f" ╚═{'═' * len(self.title)}═╝ ".center(width - 2) + "║\n"

                return line1 + line2 + line3
            else:
                return f"╔{'═' * (width - 2)}╗\n"

        def get_description(desc=...):
            if desc is ...:
                if self.description is ...:
                    return ''
                desc: list[str] = self.description.split()

            result = ""

            while len(desc) != 0:
                word = desc.pop(0)
                if len(f"║{result} {word} ║") > width:
                    if self.description_center:
                        return "║" + result.center(width - 3) + " ║\n" + get_description([word] + desc)
                    else:
                        return "║" + result.ljust(width - 3) + " ║\n" + get_description([word] + desc)
                else:
                    result += f" {word}"

            if self.description_center:
                return "║" + result.center(width - 3) + " ║\n" + get_separator()
            else:
                return "║" + result.ljust(width - 3) + " ║\n" + get_separator()

        def get_choice_button(number, choice: str):
            if number == self.selected:
                return (
                    f"║ {Color.RED}╔═{'═' * nb_width}═╗╔═{'═' * (width - nb_width - 12)}═╗{Color.STOP} ║\n"
                    f"║ {Color.RED}║ {str(number).zfill(nb_width)} ╠╣ {choice.ljust(width - nb_width - 12)} ║{Color.STOP} ║\n"
                    f"║ {Color.RED}╚═{'═' * nb_width}═╝╚═{'═' * (width - nb_width - 12)}═╝{Color.STOP} ║\n"
                )
            else:
                return (
                    f"║ ┌─{'─' * nb_width}─┐┌─{'─' * (width - nb_width - 12)}─┐ ║\n"
                    f"║ │ {str(number).zfill(nb_width)} ├┤ {choice.ljust(width - nb_width - 12)} │ ║\n"
                    f"║ └─{'─' * nb_width}─┘└─{'─' * (width - nb_width - 12)}─┘ ║\n"
                )

        def get_back_button():
            if isinstance(self.back_button, str):
                return get_separator() + get_choice_button(0, self.back_button)
            else:
                return ''

        def get_separator():
            return f"╟{'─' * (width - 2)}╢\n"

        def get_footer():
            return f"╚{'═' * (width - 2)}╝"

        if len(self) == 0:
            return "The menu is empty."

        width = self._width
        nb_width = self._width_number

        return (
                get_title() +
                get_description() +
                ''.join(get_choice_button(i + 1, self.choices[i]) for i in range(len(self.choices))) +
                get_back_button() +
                get_footer()
        )

    def __repr__(self):
        return repr(self.choices)

    def __iter__(self):
        return iter(self.choices)

    def __next__(self):
        self.selected = (self.selected % len(self.choices)) + 1

    @property
    def _width(self):
        if isinstance(self.title, str):
            title_size = len(f"╔═╣ {self.title} ╠═╗")
        else:
            title_size = 0

        if isinstance(self.description, str):
            desc_data = {
                len(word): word for word in self.description.split()
            }
            description_size = len(f"║ {desc_data[max(desc_data.keys())]} ║")
            del desc_data
        else:
            description_size = 0

        choice_data = {
            len(word): word for word in self.choices
        }
        choice_size = len(f"║ │ {len(self.choices)} ├┤ {choice_data[max(choice_data.keys())]} │ ║")
        del choice_data

        if isinstance(self.back_button, str):
            back_size = len(f"║ │ {len(self.choices)} ├┤ {self.back_button} │ ║")
        else:
            back_size = 0

        return max(title_size, description_size, choice_size, back_size)

    @property
    def _width_number(self):
        return len(str(len(self.choices)))

    def select(self):
        """Selects the value entered by the user"""
        chx = enter(">> ")
        if chx not in range(0 if isinstance(self.back_button, str) else 1, len(self.choices) + 1):
            raise IndexError
        self.selected = chx
        return chx


def enter(__prompt='', __type=int):
    """This function allows to input any type.

    Types:
    ------
    - bool
    - complex
    - float
    - int
    - list
    - set
    - slice
    - str

    :param __prompt:  Text to print before recovery.
    :type __prompt: str
    :param __type: The type to recover. [bool, complex, float, int, list, set, slice, str]
    :type __type: type

    :return: The input in the requested type.
    :rtype: bool | complex | float | int | list | set | slice | str

    :raise TypeError: If __type is not in return type.
    """
    if __type not in [
        bool, complex, float, int, list, set, slice, str
    ]:
        raise TypeError(f'{__type} is not a possible type.')
    var: str = input(__prompt)
    while True:
        try:
            '''  '''
            if __type == bool:
                if var.lower() in [
                    "yes", "是的", "हां", "sí", "si", "نعم", "হ্যাঁ", "oui", "да", "sim", "جی ہاں",
                    "y", "1", "true"
                ]:
                    return True
                elif var.lower() in [
                    "no", "不", "नहीं", "no", "لا", "না", "non", "нет", "não", "nao", "نہیں",
                    "n", "0", "false"
                ]:
                    return False
                else:
                    raise ValueError(f"could not convert string to bool: '{var}'")
            elif __type == slice:
                return slice(*var.split(':'))
            return __type(var)
        except ValueError:
            print(Color.RED + f"\"{var}\" is not of type {__type.__name__}" + Color.STOP)
            var: str = input(__prompt)


def humanize_number(__number, __fill_char='.'):
    """Humanizes the writing of a number.

    :param __number: The number to humanize
    :type __number: int
    :param __fill_char: The separator
    :type __fill_char: str

    :return: The humanized number
    :rtype: str
    """
    number = list(reversed(str(__number)))
    return ''.join(reversed(__fill_char.join(''.join(number[x:x+3])for x in range(0, len(number), 3))))


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
