def _get_custom_attributes(self):
    # Create a dictionary to store non-method attributes and their values
    custom_properties = {}
    custom_methods = {}

    # Iterate through the attributes using dir()
    for attr_name in dir(self):
        attr_value = getattr(self, attr_name)

        # Exclude attributes that are callable (methods)
        # print(type(attr_value))
        if not attr_name.startswith("_"):
            if callable(attr_value):
                # Add the attribute and its value to the dictionary
                docstring = attr_value.__doc__
                if docstring:
                    first_line = attr_value.__doc__.split("\n")[1].strip()
                else:
                    first_line = ""
                custom_methods[attr_name] = first_line
            else:
                custom_properties[attr_name] = attr_value

    return custom_methods, custom_properties
