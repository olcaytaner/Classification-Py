from Sampling.CrossValidation import CrossValidation
from Sampling.KFoldCrossValidation import KFoldCrossValidation

from Classification.Classifier.Classifier import Classifier
from Classification.Experiment.Experiment import Experiment
from Classification.Experiment.KFoldRun import KFoldRun
from Classification.InstanceList.InstanceList import InstanceList
from Classification.Parameter.Parameter import Parameter
from Classification.Performance.ExperimentPerformance import ExperimentPerformance


class KFoldRunSeparateTest(KFoldRun):

    """
    Constructor for KFoldRunSeparateTest class. Basically sets K parameter of the K-fold cross-validation.

    PARAMETERS
    ----------
    K : int
        K of the K-fold cross-validation.
    """
    def __init__(self, K: int):
        super().__init__(K)

    def runExperiment(self, classifier: Classifier, parameter: Parameter, experimentPerformance: ExperimentPerformance, crossValidation: CrossValidation, testSet: InstanceList):
        for i in range(self.K):
            trainSet = InstanceList(crossValidation.getTrainFold(i))
            classifier.train(trainSet, parameter)
            experimentPerformance.add(classifier.test(testSet))

    """
    Execute K-fold cross-validation with separate test set with the given classifier on the given data set using the given parameters.

    PARAMETERS
    ----------
    experiment : Experiment
        Experiment to be run.
        
    RETURNS
    -------
    ExperimentPerformance
        An ExperimentPerformance instance.
    """
    def execute(self, experiment: Experiment) -> ExperimentPerformance:
        result = ExperimentPerformance()
        instanceList = experiment.getDataSet().getInstanceList()
        partition = instanceList.partition(0.25, experiment.getParameter().getSeed())
        crossValidation = KFoldCrossValidation(partition.get(1).getInstances(), self.K, experiment.getParameter().getSeed())
        self.runExperiment(experiment.getClassifier(), experiment.getParameter(), result, crossValidation, partition.get(0))
        return result
