import json
import random
import unittest
from ontolearn.learning_problem import PosNegLPStandard
from owlapy.model import OWLNamedIndividual, IRI

from ontolearn.knowledge_base import KnowledgeBase
from ontolearn.concept_learner import EvoLearner, CELOE, OCEL
from ontolearn.learners import Drill
from ontolearn.metrics import F1

import os
import time
from owlapy.model import OWLNamedIndividual, IRI


class TestConceptLearnerReg:

    def test_regression_family(self):
        with open('examples/synthetic_problems.json') as json_file:
            settings = json.load(json_file)
        kb = KnowledgeBase(path=settings['data_path'][3:])
        max_runtime=10

        ocel = OCEL(knowledge_base=kb, quality_func=F1(), max_runtime=max_runtime)
        celoe = CELOE(knowledge_base=kb, quality_func=F1(), max_runtime=max_runtime)
        evo = EvoLearner(knowledge_base=kb, quality_func=F1(), max_runtime=max_runtime)
        drill = Drill(knowledge_base=kb, quality_func=F1(), max_runtime=max_runtime)

        drill_quality=[]
        celoe_quality=[]
        ocel_quality=[]
        evo_quality=[]

        for str_target_concept, examples in settings['problems'].items():
            pos = set(map(OWLNamedIndividual, map(IRI.create, set(examples['positive_examples']))))
            neg = set(map(OWLNamedIndividual, map(IRI.create, set(examples['negative_examples']))))
            print('Target concept: ', str_target_concept)

            lp = PosNegLPStandard(pos=pos, neg=neg)
            # Untrained & max runtime is not fully integrated.
            ocel_quality.append(ocel.fit(lp).best_hypotheses(n=1).quality)
            celoe_quality.append(celoe.fit(lp).best_hypotheses(n=1).quality)
            evo_quality.append(evo.fit(lp).best_hypotheses(n=1).quality)
            drill_quality.append(drill.fit(lp).best_hypotheses(n=1).quality)


        assert sum(evo_quality)>=sum(drill_quality)
        assert sum(celoe_quality)>=sum(ocel_quality)

