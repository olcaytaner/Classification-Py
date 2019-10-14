from Sampling.KFoldCrossValidation import KFoldCrossValidation

from Classification.Experiment.Experiment import Experiment
from Classification.Experiment.KFoldRunSeparateTest import KFoldRunSeparateTest
from Classification.Performance.ExperimentPerformance import ExperimentPerformance


class MxKFoldRunSeparateTest(KFoldRunSeparateTest):

    """
    Constructor for KFoldRunSeparateTest class. Basically sets K parameter of the K-fold cross-validation and M for the
    number of times.

    PARAMETERS
    ----------
    M : int
        number of cross-validation times.
    K : int
        K of the K-fold cross-validation.
    """
    def __init__(self, M: int, K: int):
        super().__init__(K)
        self.M = M

    """
    Execute the MxKFold run with separate test set with the given classifier on the given data set using the given 
    parameters.
    
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
        for j in range(self.M):
            crossValidation = KFoldCrossValidation(partition.get(1).getInstances(), self.K, experiment.getParameter().getSeed())
            self.runExperiment(experiment.getClassifier(), experiment.getParameter(), result, crossValidation, partition.get(0))
        return result
