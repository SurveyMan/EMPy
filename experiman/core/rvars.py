import warnings

__ratio__ = "ratio"
__interval__ = "interval"
__ordinal__ = "ordinal"
__nominal__ = "nominal"

class RVar(object):
    """Random variables are the atoms in experiman"""

    all_random_variables = {}

    @staticmethod
    def reset():
        del RVar.all_random_variables
        RVar.all_random_variables = {}

    def __new__(cls, name):
        if name in RVar.all_random_variables:
            warnings.warn("Returning previously declared random variable with the name %s." % name)
            return RVar.all_random_variables[name]
        else:
            retval = super(RVar, cls).__new__(cls, name)
            retval._init = False
            return retval

    def __init__(self, name, measurement_level=None, obs=[]):
        if self._init:
            return
        self.name = name
        self.obs = obs
        if measurement_level:
            self.measurement_level = measurement_level
        else:
            self.measurement_level = self._infer_measurement_level()
        RVar.all_random_variables[name] = self

    def _infer_measurement_level(self):
        """ Infers the measurement level from the supplied observations. Inference is conservative.
        :return: One of "ratio", "interval", "ordinal", or "nominal"
        """
        # TODO(etosch): create an internal "type system" for objects we define in the experiman universe.
        pass

class Lattice(object):
    """ Lattices are used to convey type information."""

    def __init__(self, bot=None, top=None, poset=[]):
        pass