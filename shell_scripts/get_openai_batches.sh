#!/usr/bin/env bash

SHOTS=(1 3 5 10)
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
BASE_PATH="$HOME/Results/llm_ontology_awareness/term_typing/ranked_retrieval"
MODEL="gpt-4o"
STRAT_SUFFIX="/most_common"

for shot in "${SHOTS[@]}"; do
    for ont in "${ONTOLOGIES[@]}"; do
        for r_args in "${BASE_PATH}/${shot}_shot${STRAT_SUFFIX}/${MODEL}/${ont}"/*; do
            echo ${r_args}
            # python3 "${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/open_ai/batch/retrieve_response.py" "${r_args}/runs/run_1/ids.json"
        done 
    done
done

