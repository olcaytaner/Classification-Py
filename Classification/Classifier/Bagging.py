from Classification.Classifier.Classifier import Classifier
from Classification.InstanceList.InstanceList import InstanceList
from Classification.Model.DecisionTree.DecisionNode import DecisionNode
from Classification.Model.DecisionTree.DecisionTree import DecisionTree
from Classification.Model.TreeEnsembleModel import TreeEnsembleModel
from Classification.Parameter.BaggingParameter import BaggingParameter
from Classification.Parameter.Parameter import Parameter


class Bagging(Classifier):

    """
    Bagging bootstrap ensemble method that creates individuals for its ensemble by training each classifier on a random
    redistribution of the training set.
    This training method is for a bagged decision tree classifier. 20 percent of the instances are left aside for
    pruning of the trees 80 percent of the instances are used for training the trees. The number of trees (forestSize)
    is a parameter, and basically the method will learn an ensemble of trees as a model.

    PARAMETERS
    ----------
    trainSet : InstanceList
        Training data given to the algorithm.
    parameters : Parameter
        Parameters of the bagging trees algorithm. ensembleSize returns the number of trees in the bagged forest.
    """
    def train(self, trainSet: InstanceList, parameters: BaggingParameter):
        partition = trainSet.stratifiedPartition(0.2, parameters.getSeed())
        forestSize = parameters.getEnsembleSize()
        forest = []
        for i in range(forestSize):
            bootstrapTrain = partition.get(1).bootstrap(i)
            bootstrapPrune = partition.get(0).bootstrap(i)
            tree = DecisionTree(DecisionNode(InstanceList(bootstrapTrain.getSample())))
            tree.prune(InstanceList(bootstrapPrune.getSample()))
            forest.append(tree)
        self.model = TreeEnsembleModel(forest)