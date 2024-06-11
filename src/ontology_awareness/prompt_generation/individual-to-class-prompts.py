#!/usr/bin/env python

# Script for various forms of prompting Individual -> Concept/Class mapping

import itertools
import random

import more_itertools
import owlready2

random.seed(42)


class IndividualToClassPrompts:
    """Generate various individual to class mapping prompts"""

    def __init__(self, ontologyPath: str):
        onto = owlready2.get_ontology(ontologyPath).load(only_local=True)
        # Get correct namespace to use for access
        namespaces = list(onto._namespaces.keys())
        for n in namespaces:
            namespace = owlready2.get_namespace(n)
            if namespace[more_itertools.first_true(onto.classes()).name] is not None:
                break

        self.namespace = namespace
        self.namespace.ontology = onto.ontology
        self.individuals = list(self.namespace.ontology.individuals())
        self.classes = list(self.namespace.ontology.classes())
        self.indClsPairs = list(itertools.product(self.individuals, self.classes))
        random.shuffle(self.indClsPairs)

    def noStructureZeroShot(self) -> str:
        """Create zero shot, no hierarchy information context prompts"""

        header = "Answer in true or false only."

        prompt = [
            f"{idx}. {inst.name} is a {cl.name}"
            for idx, (inst, cl) in enumerate(self.indClsPairs)
        ]

        return "\n".join(prompt)


if __name__ == "__main__":
    print("Running")
    onto_path = "file:///home/upal/Data/ontologies/wines-ontology/wine-clean.rdf"
    ind2ClsPrompt = IndividualToClassPrompts(onto_path)
    prompt = ind2ClsPrompt.noStructureZeroShot()
    print(prompt)
