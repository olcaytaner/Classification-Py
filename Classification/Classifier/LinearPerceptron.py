from Classification.Classifier.Classifier import Classifier
from Classification.InstanceList.InstanceList import InstanceList
from Classification.Model.LinearPerceptronModel import LinearPerceptronModel
from Classification.Parameter.LinearPerceptronParameter import LinearPerceptronParameter


class LinearPerceptron(Classifier):

    """
    Training algorithm for the linear perceptron algorithm. 20 percent of the data is separated as cross-validation
    data used for selecting the best weights. 80 percent of the data is used for training the linear perceptron with
    gradient descent.

    PARAMETERS
    ----------
    trainSet : InstanceList
        Training data given to the algorithm
    parameters : LinearPerceptronParameter
        Parameters of the linear perceptron.
    """
    def train(self, trainSet: InstanceList, parameters: LinearPerceptronParameter):
        partition = trainSet.stratifiedPartition(parameters.getCrossValidationRatio(), parameters.getSeed())
        self.model = LinearPerceptronModel(partition.get(1), partition.get(0), parameters)