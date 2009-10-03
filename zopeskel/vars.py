from paste.script.templates import var as base_var


##########################################################################
# Mode constants
EXPERT = 'expert'
EASY = 'easy'

##########################################################################
# Variable classes

class ValidationException(ValueError):
    """Invalid value provided for variable."""


class var(base_var):

    _default_widget = 'string'

    def __init__(self, name, description,
                 default='', should_echo=True,
                 title=None, help=None, widget=None,
                 modes=(EASY, EXPERT)):
        self.name = name
        self.description = description
        self.default = default
        self.should_echo = should_echo
        self.title = title
        self.help = help
        if not widget:
            self.widget = self._default_widget
        else:
            self.widget = widget
        self.modes = modes

    def pretty_description(self):
        title = getattr(self, 'title', self.name) or self.name

        if self.description:
            return '%s (%s)' % (title, self.description)
        else:
            return title
    
    def further_help(self):
        """ return the help string for this class or inform user that none is
            available
        """
        no_help = "Sorry, no further help is available for %s\n" % self.name
        return self.help and self.help or no_help

    def validate(self, value):
        raise NotImplementedError


class BooleanVar(var):
    _default_widget = 'boolean'

    def validate(self, value):
        #Get rid of bonus whitespace
        if isinstance(value, basestring):
            value = value.strip().lower()

        #Map special cases to correct values.
        if value in ['t', 'y', 'yes', 'true', 1]: 
            value = True
        elif value in ['f','n','no', 'false', 0]:
            value = False

        if type(value) != bool:
            raise ValidationException("Not a valid boolean value: %s" % value)

        return value


class StringVar(var):
    """Single string values."""

    _default_widget = 'string'

    def validate(self, value):
        if not isinstance(value, basestring):
            raise ValidationException("Not a string value: %s" % value)

        value = value.strip()

        return value


class TextVar(StringVar):
    """Multi-line values."""

    _default_widget = 'text'


class DottedVar(var):
    """Variable for 'dotted Python name', eg, 'foo.bar.baz'"""

    _default_widget = 'string'

    def validate(self, value):
        if not isinstance(value, basestring):
            raise ValidationException("Not a string value: %s" % value)
        value = value.strip()

        names = value.split(".")
        for name in names:
            # Check if Python identifier, http://code.activestate.com/recipes/413487/
            try:
                class test(object): __slots__ = [name]
            except TypeError:
                raise ValidationException("Not a valid Python dotted name: %s ('%s' is not an identifier)" % (value, name))

        return value

