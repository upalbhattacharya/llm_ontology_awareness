#!/usr/bin/env bash

SRC_DIR=$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/0_shot/llama3-7B

ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
for ont in "${ONTOLOGIES[@]}"; do
    for j in ${SRC_DIR}/${ont}/*; do
        sed -i "s@/scratch/bhatt006/Results/llm_ontology_awareness/term_typing/ranked_retrieval/${ont}@/scratch/bhatt006/Results/llm_ontology_awareness/term_typing/ranked_retrieval/0_shot/llama3-7B/${ont}@g" ${j}
    done
done
