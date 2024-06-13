#!/usr/bin/env python

"""
Module to generate different datasets for various prompts for Llama3 models.
"""

from itertools import product

from torch.utils.data import Dataset

from llm_ontology_awareness.data_processing.ontology_processing.ontology_processing import (
    ProcessedOntology,
)


class IndividualToClassInstructBinaryDataset(Dataset):
    """Generate various individual to class mapping prompts"""

    system_message: str = "Classify the following as true or false"

    prompt_template: str = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        f"{system_message}<|eot_id|><|start_header_id|>user<|end_header_id|>"
        "{}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    )
    classify_statement: str = "{} is a {}"

    def __init__(self, ontologyPath: str):
        self.onto = ProcessedOntology(ontologyPath)
        self.data_pairs = list(product(self.onto.individuals, self.onto.classes))

    def __len__(self):
        return len(self.onto.classes) * len(self.onto.individuals)

    def __getitem__(self, idx):
        inst = self.data_pairs[idx][0]
        cl = self.data_pairs[idx][1]
        print(inst, cl)
        sentence = self.classify_statement.format(inst.name, cl.name)
        return self.prompt_template.format(sentence), self.is_direct_member(inst, cl)

    def is_direct_member(self, inst, cl):
        return cl in inst.is_a


if __name__ == "__main__":
    print("Running")
    onto_path = "file:///home/upal/Data/ontologies/wines-ontology/wine-clean.rdf"
    itcib = IndividualToClassInstructBinaryDataset(onto_path)
    for i, (d, label) in enumerate(iter(itcib)):
        print(d, label)
        if i == 19:
            break
