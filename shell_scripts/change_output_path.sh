#!/usr/bin/env bash

RUN_ARGS_DIR=$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval

ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
SHOTS=$(seq 1 10)

for ont in "${ONTOLOGIES[@]}"; do
    for i in ${SHOTS}; do
        for j in ${RUN_ARGS_DIR}/${i}_shot/most_common/llama3-7B/${ont}/*; do
            echo ${j}
        done
    done
done

