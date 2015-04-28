import warnings

__ratio__ = "ratio"
__interval__ = "interval"
__ordinal__ = "ordinal"
__nominal__ = "nominal"

__measurement_levels__ = [__ratio__, __interval__, __ordinal__, __nominal__]

class RVar(object):
    """Random variables are the atoms in experiman"""

    all_random_variables = {}

    @staticmethod
    def reset():
        del RVar.all_random_variables
        RVar.all_random_variables = {}

    def __new__(cls, name, measurement_level=None, obs=[]):
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
            assert measurement_level in __measurement_levels__
            self.measurement_level = measurement_level
        else:
            self.measurement_level = self._infer_measurement_level()
        RVar.all_random_variables[name] = self

    def _infer_measurement_level(self):
        """ Infers the measurement level from the supplied observations. Inference is conservative.
        :return: One of "ratio", "interval", "ordinal", or "nominal"
        """
        # TODO(etosch): create an internal "type system" for objects we define in the experiman universe.
        if self.obs:
            if isinstance(self.obs[0], Lattice):
                pass

    def iid_observes(self, observation):
        """A random variable is a function from some domain of interest to the reals. Observations are also random
        variables; if X_1 ~ X, then X is the r.v. that generates observations X_1. In this context, X_1 is another
        function -- one that generates another function that is indexed by the iteration in the sampling process.
        X_1 is observed to take on some value, x_1. However, X_1 could have taken on some other value.
        :param observation: An instance of Lattice. Its measurement level must agree with the generating random
        variable's measurement level.
        :return: A new Random variable corresponding to this observation.
        """
        # Add something to ensure that the measurement level of the observation is the same as the
        # measurement level of this r.v.
        assert isinstance(observation, Lattice)
        rvar_i = RVar(self.name + "_" + str(len(self.obs)), self.measurement_level, observation)
        self.obs.append(rvar_i)
        return rvar_i


class Lattice(object):
    """Lattices are used to convey type information."""

    def __init__(self, bot, top, poset=[]):
        self.bot = bot
        self.top = top
        self.poset = poset


class Nominal(Lattice):

    def __init__(self, poset):
        super(Nominal, self).__init__(None, None, poset)


class Ordinal(str, Lattice):
    pass


class Ratio(float, Lattice):
    pass


class String(str, Nominal):

    def __init__(self, mystring):
        str.__init__(self, mystring)
        Lattice.__init__(mystring)