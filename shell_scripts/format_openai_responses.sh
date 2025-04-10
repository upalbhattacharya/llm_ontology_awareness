#!/usr/bin/env bash

SHOTS=(1 2 3 4 5 6 7 8 9 10)
BASE_RESULTS_PATH=$HOME/Results/llm_ontology_awareness/term_typing/ranked_retrieval

ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
MODEL="gpt-4o"
STRAT_SUFFIX="/most_common"

for shot in "${SHOTS[@]}"; do
    for ont in "${ONTOLOGIES[@]}"; do
        for r_args in "${BASE_RESULTS_PATH}/${shot}_shot${STRAT_SUFFIX}/${MODEL}"/*; do
            for run in "${r_args}/runs"/*; do
                echo ${run}
            done
        done
    done
done

