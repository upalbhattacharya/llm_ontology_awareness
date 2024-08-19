#!/usr/bin/env python

"""Processing of ontologies for target and prompt generation"""

from collections import defaultdict

import more_itertools
import owlready2


class ProcessedOntology:
    def __init__(self, ontologyPath: str):
        loadPath = (
            ontologyPath
            if ontologyPath.startswith("file:///")
            else f"file:///{ontologyPath}"
        )
        onto = owlready2.get_ontology(loadPath).load(only_local=False)
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
        self.class_individuals = self._get_class_individuals()

    def _get_class_individuals(self):
        class_individuals = defaultdict(list)
        for cls in self.classes:
            class_individuals[cls.name] = [
                inst.name for inst in self.namespace.ontology.search(type=cls)
            ]
        return class_individuals
