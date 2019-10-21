from Math.DiscreteDistribution import DiscreteDistribution

from Classification.Instance.Instance import Instance
from Classification.Model.GaussianModel import GaussianModel


class LdaModel(GaussianModel):

    """
    A constructor which sets the priorDistribution, w and w0 according to given inputs.

    PARAMETERS
    ----------
    priorDistribution : DiscreteDistribution
        DiscreteDistribution input.
    w : dict
        Dict of String and Vectors.
    w0 : dict
        Dict of String and float.
    """
    def __init__(self, priorDistribution: DiscreteDistribution, w: dict, w0: dict):
        self.priorDistribution = priorDistribution
        self.w = w
        self.w0 = w0

    """
    The calculateMetric method takes an Instance and a String as inputs. It returns the dot product of given Instance
    and wi plus w0i.

    PARAMETERS
    ----------
    instance : Instance
        Instance input.
    Ci : str      
        String input.
        
    RETURNS
    -------
    float
        The dot product of given Instance and wi plus w0i.
    """
    def calculateMetric(self, instance: Instance, Ci: str) -> float:
        xi = instance.toVector()
        wi = self.w[Ci]
        w0i = self.w0[Ci]
        return wi.dotProduct(xi) + w0i