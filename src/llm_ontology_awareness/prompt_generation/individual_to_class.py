#!/usr/bin/env python

# Script for various forms of prompting Individual -> Concept/Class mapping

import json

from llm_ontology_awareness.ontology_processing.ontology_processing import (
    OntologyProcessing,
)


class IndividualToClassPrompts:
    """Generate various individual to class mapping prompts"""

    def __init__(self, targetFile: str):
        with open(targetFile, "r") as f:
            individual_classes = json.load(f)

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
