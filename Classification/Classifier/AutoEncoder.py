from Classification.Classifier.Classifier import Classifier
from Classification.InstanceList.InstanceList import InstanceList
from Classification.Model.AutoEncoderModel import AutoEncoderModel
from Classification.Parameter.MultiLayerPerceptronParameter import MultiLayerPerceptronParameter
from Classification.Performance.Performance import Performance


class AutoEncoder(Classifier):

    """
    Training algorithm for auto encoders. An auto encoder is a neural network which attempts to replicate its input at
    its output.

    PARAMETERS
    ----------
    trainSet : InstanceList
        Training data given to the algorithm.
    parameters : MultiLayerPerceptronParameter
        Parameters of the auto encoder.
    """
    def train(self, trainSet: InstanceList, parameters: MultiLayerPerceptronParameter):
        partition = trainSet.stratifiedPartition(0.2, parameters.getSeed())
        self.model = AutoEncoderModel(partition.get(1), partition.get(0), parameters)

    """
    A performance test for an auto encoder with the given test set..

    PARAMETERS
    ----------
    testSet : InstanceList
        Test data (list of instances) to be tested.
        
    RETURNS
    -------
    Performance
        Error rate.
    """
    def test(self, testSet: InstanceList) -> Performance:
        return self.model.testAutoEncoder(testSet)