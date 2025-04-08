#!/usr/bin/env bash

SRC_RUN_ARGS_DIR=$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/2_shot/most_common/gpt-4o/wines-ontology
SRC_ONTOLOGY_NAME="wines-ontology"
SRC_SHOT=2
RUN_ARGS_DIR=$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval

LLM="gpt-4o"
SHOTS=(1 2 3 4 5 6 7 8 9 10)
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
STRAT_SUFFIX="/most_common"

for i in "${SHOTS[@]}"; do
    for j in "${ONTOLOGIES[@]}"; do
        SRC_DIR="${RUN_ARGS_DIR}/${SRC_SHOT}_shot${STRAT_SUFFIX}/${LLM}/${j}"
        DEST_DIR="${RUN_ARGS_DIR}/${i}_shot${STRAT_SUFFIX}/${LLM}/${j}"
        echo ${SRC_DIR}
        echo ${DEST_DIR}
        if [ "${DEST_DIR}" == "${SRC_RUN_ARGS_DIR}" ]; then
            echo "Source and Destination are the same. Moving On"
            continue
        fi
        for x in "${SRC_RUN_ARGS_DIR}"/*; do
            N_UUID=$(uuidgen)
            N_RUN_ARGS="${DEST_DIR}/${N_UUID}.json"
            # echo ${N_RUN_ARGS}
            cp ${x} ${N_RUN_ARGS}
            sed -i "s@${SRC_ONTOLOGY_NAME}@${j}@g" ${N_RUN_ARGS}
            sed -i "s@Wines Ontology@${j}@g" ${N_RUN_ARGS}
            sed -i "s@${SRC_SHOT}_shot@${i}_shot@g" ${N_RUN_ARGS}
            sed -i "s@${SRC_SHOT}-Shot@${i}-Shot@g" ${N_RUN_ARGS}
        done
    done
done
