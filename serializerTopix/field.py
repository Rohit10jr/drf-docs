import re
from rest_framework import serializers

class Color:
    def __init__(self, red, green, blue):
        assert 0 <= red <= 255
        assert 0 <= red <= 255
        assert 0 <= red <= 255
        self.red = red
        self.green = green
        self.blue = blue


class ColorField(serializers.Field):
    default_error_messages = {
        'incorrect_type': 'Expected a string but got {input_type}.',
        'incorrect_format': 'Expected `rgb(#,#,#)` format.',
        'out_of_range': 'Values must be between 0 and 255.',
    }

    def to_representation(self, value):
        # Convert Color instance → string
        return f"rgb({value.red}, {value.green}, {value.blue})"

    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('incorrect_type', input_type=type(data).__name__)

        if not re.match(r'^rgb\(\d{1,3},\s?\d{1,3},\s?\d{1,3}\)$', data):
            self.fail('incorrect_format')

        stripped = data.strip('rgb()')
        red, green, blue = [int(x.strip()) for x in stripped.split(',')]

        if any(c < 0 or c > 255 for c in (red, green, blue)):
            self.fail('out_of_range')

        return Color(red, green, blue)
