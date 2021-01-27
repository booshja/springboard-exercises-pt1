"""Python serial number generator."""


class SerialGenerator:
    """Machine to create unique incrementing serial numbers.

    Attributes:
    current = serial number to be shown on generation
    next = serial number to be shown after generation
    start = original starting point for serial numbers

    >>> serial = SerialGenerator(start=100)

    >>> serial.generate()
    100

    >>> serial.generate()
    101

    >>> serial.generate()
    102

    >>> serial.reset()

    >>> serial.generate()
    100
    """

    def __repr__(self):
        """Shows developer friendlier representation of object instance"""
        return f"<SerialGenerator start={self.start} current={self.current} next={self.next}>"

    def __str__(self):
        """Shows plain english representation of object instance"""
        return f"SerialGenerator Class, Original Start is {self.start}, the current serial number is {self.current}, and the next serial number is {self.next}."

    def __init__(self, start):
        """Creates starting point, sets up next serial"""
        self.current = start
        self.start = start
        self.next = self.current + 1

    def generate(self):
        """Generates the next iteration of the serial number"""
        display = self.current
        self.current += 1
        self.next += 1
        return display

    def reset(self):
        """Resets the generator back to its original start number"""
        self.current = self.start
