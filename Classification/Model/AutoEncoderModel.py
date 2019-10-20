from Math.Vector import Vector

from Classification.Instance.Instance import Instance
from Classification.InstanceList.InstanceList import InstanceList
from Classification.Model.NeuralNetworkModel import NeuralNetworkModel
from Classification.Parameter.MultiLayerPerceptronParameter import MultiLayerPerceptronParameter
import copy

from Classification.Performance.Performance import Performance


class AutoEncoderModel(NeuralNetworkModel):

    """
    The AutoEncoderModel method takes two InstanceLists as inputs; train set and validation set. First it allocates
    the weights of W and V matrices using given MultiLayerPerceptronParameter and takes the clones of these
    matrices as the bestW and bestV. Then, it gets the epoch and starts to iterate over them. First it shuffles the
    train set and tries to find the new W and V matrices. At the end it tests the autoencoder with given validation
    set and if its performance is better than the previous one, it reassigns the bestW and bestV matrices. Continue to
    iterate with a lower learning rate till the end of an episode.

    PARAMETERS
    ----------
    trainSet : InstanceList
        InstanceList to use as train set.
    validationSet : InstanceList
        InstanceList to use as validation set.
    parameters : MultiLayerPerceptronParameter
        MultiLayerPerceptronParameter is used to get the parameters.
    """
    def __init__(self, trainSet: InstanceList, validationSet: InstanceList, parameters: MultiLayerPerceptronParameter):
        super().__init__(trainSet)
        self.K = trainSet.get(0).continuousAttributeSize()
        self.allocateWeights(parameters.getHiddenNodes())
        bestW = copy.deepcopy(self.W)
        bestV = copy.deepcopy(self.V)
        bestPerformance = Performance(1000000000)
        epoch = parameters.getEpoch()
        learningRate = parameters.getLearningRate()
        for i in range(epoch):
            trainSet.shuffle(parameters.getSeed())
            for j in range(trainSet.size()):
                self.createInputVector(trainSet.get(j))
                self.r = trainSet.get(j).toVector()
                hidden = self.calculateHidden(self.x, self.W)
                hiddenBiased = hidden.biased()
                self.y = self.V.multiplyWithVectorFromRight(hiddenBiased)
                rMinusY = self.r.difference(self.y)
                deltaV = rMinusY.multiplyWithVector(hiddenBiased)
                oneMinusHidden = self.calculateOneMinusHidden(hidden)
                tmph = self.V.multiplyWithVectorFromLeft(rMinusY)
                tmph.remove(0)
                tmpHidden = oneMinusHidden.elementProduct(hidden.elementProduct(tmph))
                deltaW = tmpHidden.multiplyWithVector(self.x)
                deltaV.multiplyWithConstant(learningRate)
                self.V.add(deltaV)
                deltaW.multiplyWithConstant(learningRate)
                self.W.add(deltaW)
            currentPerformance = self.testAutoEncoder(validationSet)
            if currentPerformance.getErrorRate() < bestPerformance.getErrorRate():
                bestPerformance = currentPerformance
                bestW = copy.deepcopy(self.W)
                bestV = copy.deepcopy(self.V)
        self.W = bestW
        self.V = bestV

    """
    The allocateWeights method takes an integer number and sets layer weights of W and V matrices according to given 
    number.

    PARAMETERS
    ----------
    H : int
        Integer input.
    """
    def allocateWeights(self, H: int):
        self.W = self.allocateLayerWeights(H, self.d + 1)
        self.V = self.allocateLayerWeights(self.K, H + 1)

    """
    The testAutoEncoder method takes an InstanceList as an input and tries to predict a value and finds the difference 
    with the actual value for each item of that InstanceList. At the end, it returns an error rate by finding the mean 
    of total errors.

    PARAMETERS
    ----------
    data : InstanceList
        InstanceList to use as validation set.
        
    RETURNS
    -------
    Performance
        Error rate by finding the mean of total errors.
    """
    def testAutoEncoder(self, data: InstanceList) -> Performance:
        total = data.size()
        error = 0.0
        for i in range(total):
            self.y = self.predictInput(data.get(i))
            self.r = data.get(i).toVector()
            error += self.r.difference(self.y).dotProductWithSelf()
        return Performance(error / total)

    """
    The predictInput method takes an Instance as an input and calculates a forward single hidden layer and returns the 
    predicted value.

    PARAMETERS
    ----------
    instance : Instance
        Instance to predict.
        
    RETURNS
    -------
    Vector
        Predicted value.
    """
    def predictInput(self, instance: Instance) -> Vector:
        self.createInputVector(instance)
        self.calculateForwardSingleHiddenLayer(self.W, self.V)
        return self.y

    """
    The calculateOutput method calculates a forward single hidden layer.
    """
    def calculateOutput(self):
        self.calculateForwardSingleHiddenLayer(self.W, self.V)
