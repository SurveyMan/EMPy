import numpy
import scipy.stats as stats
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
            assert issubclass(measurement_level, Lattice)
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

    def _incremental_independence(self):
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

    def independence_test(self, other):
        measurement_level = min(self.measurement_level, other.measurement_level)
        return measurement_level.independence_test(measurement_level.convert(self, other))

    def set_size(self):
        if self.obs:
            assert isinstance(self.obs[0], Lattice)
            return len(self.obs[0].poset[0])


class Lattice(object):
    """Lattices are used to convey type information."""

    def __init__(self, bot, top, poset=[], order=1):
        self.bot = bot
        self.top = top
        self.poset = poset
        self.order = order

    def __cmp__(self, other):
        return self.order.__cmp__(other)


class Nominal(Lattice):

    def __init__(self, poset):
        super(Nominal, self).__init__(None, None, poset, 1)
        self.name = __nominal__

    @staticmethod
    def independence_test(contingency_table):
        return stats.chi2_contingency(contingency_table, correction=True)

    @staticmethod
    def convert(self, other, partition=None):
        assert len(self.obs) == len(other.obs)
        r = len(self.set_size())
        if other.measurement_level == __nominal__ or other.measurement_level == __ordinal__:
            c = len(other.poset)
            table = numpy.matrix([[0 for _ in range(c)] for _ in range(r)])
            for i in range(r):
                j = self.poset.index(self.obs[i].obs)
                k = other.poset.index(other.obs[i].obs)
                table[j, k] += 1
            return table
        else:
            partitions = partition(other.obs)
            c = len(partitions)
            table = numpy.matrix([[0 for _ in range(c)] for _ in range(r)])
            for i in range(r):
                j = self.poset.index(self.obs[i].obs)
                val = other.obs[i].obs
                for (l, (lower, upper)) in enumerate(partitions):
                    if lower <= val <= upper:
                        k = l
                table[j, k] += 1
            return table


class Ordinal(str, Lattice):

    def __init__(self, bot, top, poset):
        Lattice.__init__(self, bot, top, poset, 2)
        self.name = __ordinal__


class Interval(float, Lattice):

    def __init__(self, bot, top, poset):
        Lattice.__init__(self, bot, top, poset, 3)
        self.name = __interval__


class Ratio(float, Lattice):

    def __init__(self, bot, top, poset):
        Lattice.__init__(self, bot, top, poset, 4)
        self.name = __ratio__


__measurement_levels__ = [Ratio, Interval, Ordinal, Nominal]
