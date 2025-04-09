#!/usr/bin/env bash

SHOTS=(1 3 5 10)
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
BASE_PATH="$HOME/Results/llm_ontology_awareness/term_typing/ranked_retrieval"
MODEL="gpt-4o"
STRAT_SUFFIX="/most_common"

for shot in "${SHOTS[@]}"; do
    for ont in "${ONTOLOGIES[@]}"; do
        echo $(tree "${BASE_PATH}/${shot}_shot${STRAT_SUFFIX}/${MODEL}/${ont}/")
    done
done

