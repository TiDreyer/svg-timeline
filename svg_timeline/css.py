""" base classes for handling CSS """
class CascadeStyleSheet(dict):
    """ basic representation of a CSS """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.full_validate()

    def full_validate(self):
        """ check that the object represents valid CSS """
        for key, value in self.items():
            self.__validate_one_entry(key, value)

    def __setitem__(self, key, value):
        self.__validate_one_entry(key, value)
        super().__setitem__(key, value)

    @staticmethod
    def __validate_one_entry(key, value):
        if not isinstance(key, str):
            raise TypeError(f"Invalid key {key}. All CSS keys must be strings.")
        if not isinstance(value, dict):
            raise TypeError(f"Invalid entry for key {key}. All CSS entries must be dicts.")
        for sub_key, sub_value in value.items():
            if not isinstance(sub_key, str):
                raise TypeError(f"Invalid subkey {sub_key} in entry {key}. All CSS keys must be strings.")
            if not isinstance(sub_value, str):
                raise TypeError(f"Invalid value for {sub_key} in entry {key}. All CSS values must be strings.")

    def compile(self, indent='', line_break='\n') -> str:
        """ compile the contained style definition into a css file """
        css_section = ""
        for selector, props in self.items():
            css_section += f'{selector} {{{line_break}'
            for name, value in props.items():
                css_section += f'{indent}{name}: {value};{line_break}'
            css_section += f'}}{line_break}'
        return css_section