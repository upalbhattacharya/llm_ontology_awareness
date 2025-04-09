#!/usr/bin/env bash

SHOTS=(2 4 6 7 8 9)
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
RUN_ARGS_PATH="$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval"
MODEL="gpt-4o"
STRAT_SUFFIX="/most_common"

for shot in "${SHOTS[@]}"; do
    for ont in "${ONTOLOGIES[@]}"; do
        for r_args in "${RUN_ARGS_PATH}/${shot}_shot${STRAT_SUFFIX}/${MODEL}/${ont}"/*; do
            echo ${r_args}
            python3 "${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/open_ai/batch/create_batch/term_typing.py" -f "${r_args}"
        done 
    done
done

