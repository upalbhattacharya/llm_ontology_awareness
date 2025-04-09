#!/usr/bin/env bash

SHOTS=(2 4 6 7 8 9)
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
BASE_PATH="$HOME/Results/llm_ontology_awareness/term_typing/ranked_retrieval"
MODEL="gpt-4o"
STRAT_SUFFIX="/most_common"

for shot in "${SHOTS[@]}"; do
    for ont in "${ONTOLOGIES[@]}"; do
        if [ ${shot} -eq 2 ] && [ ${ont} == "wines-ontology" ]; then
            echo "Skipping"
            continue
        fi
        for r_args in "${BASE_PATH}/${shot}_shot${STRAT_SUFFIX}/${MODEL}/${ont}"/*; do
            # echo ${r_args}
            python3 "${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/open_ai/batch/retrieve_response.py" -j "${r_args}/runs/run_1/ids.json"
        done 
    done
done

