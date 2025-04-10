#!/usr/bin/env bash

SHOTS=(1 2 3 4 5 6 7 8 9 10)
BASE_RESULTS_PATH=$HOME/Results/llm_ontology_awareness/term_typing/ranked_retrieval

ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
MODEL="gpt-4o"
STRAT_SUFFIX="/most_common"
for shot in "${SHOTS[@]}"; do
    for ont in "${ONTOLOGIES[@]}"; do
        for r_args in "${BASE_RESULTS_PATH}/${shot}_shot${STRAT_SUFFIX}/${MODEL}/${ont}"/*; do
            for run in "${r_args}/runs"/*; do
                # echo ${run}
                python3 ${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/open_ai/format_response_content/term_typing.py -f ${run} -r ${r_args}/params.json -l ${r_args}/label_mapping.json
            done
        done
    done
done

