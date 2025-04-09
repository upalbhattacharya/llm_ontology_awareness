#!/usr/bin/env bash

SHOTS=(0)
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking")
RUN_ARGS_PATH="$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval"
MODEL="o1-preview"
# STRAT_SUFFIX="/most_common"
STRAT_SUFFIX=""

for shot in "${SHOTS[@]}"; do
    for ont in "${ONTOLOGIES[@]}"; do
        # if [ ${shot} -eq 2 ] && [ ${ont} == "wines-ontology" ]; then
        #     echo "Skipping"
        #     continue
        # fi
        for r_args in "${RUN_ARGS_PATH}/${shot}_shot${STRAT_SUFFIX}/${MODEL}/${ont}"/*; do
            echo ${r_args}
            python3 "${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/open_ai/batch/create_batch/term_typing.py" -f "${r_args}"
        done 
    done
done

