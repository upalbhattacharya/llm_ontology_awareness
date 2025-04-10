#!/usr/bin/env bash

# SHOTS=(1 2 3 4 5 6 7 8 9 10)
# SHOTS=(3)
SHOTS=(0)
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
BASE_PATH="$HOME/Results/llm_ontology_awareness/term_typing/ranked_retrieval"
MODEL="o1-preview"
# STRAT_SUFFIX="/most_common"
STRAT_SUFFIX=""

for shot in "${SHOTS[@]}"; do
    for ont in "${ONTOLOGIES[@]}"; do
        # if [ ${shot} -eq 2 ] && [ ${ont} == "wines-ontology" ]; then
        #     echo "Skipping"
        #     continue
        # fi
        for r_args in "${BASE_PATH}/${shot}_shot${STRAT_SUFFIX}/${MODEL}/${ont}"/*; do
            for run in "${r_args}/runs"/*; do
                echo ${run}
                python3 "${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/open_ai/batch/retrieve_response.py" -j "${run}/ids.json"
            done
        done 
    done
done

