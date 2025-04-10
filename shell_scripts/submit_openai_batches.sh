#!/usr/bin/env bash

REPETITIONS=(1 2 3 4 5 6 7 8 9)
SHOTS=(3)
ONTOLOGIES=("wines-ontology" "case-uco-owl-trafficking")
BASE_PATH="$HOME/Results/llm_ontology_awareness/term_typing/ranked_retrieval"
MODELS=("gpt-4o-temp_high" "gpt-4o-temp_low")
STRAT_SUFFIX="/most_common"
# STRAT_SUFFIX=""

for rep in "${REPETITIONS[@]}"; do
    for shot in "${SHOTS[@]}"; do
        for ont in "${ONTOLOGIES[@]}"; do
            # if [ ${shot} -eq 2 ] && [ ${ont} == "wines-ontology" ]; then
            #     echo "Skipping"
            #     continue
            # fi
            for MODEL in "${MODELS[@]}"; do
                for r_args in "${BASE_PATH}/${shot}_shot${STRAT_SUFFIX}/${MODEL}/${ont}"/*; do
                    echo ${rep}
                    # python3 "${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/open_ai/batch/submit_batch.py" -b "${r_args}"
                done
            done 
        done
    done
done

