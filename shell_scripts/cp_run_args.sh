#!/usr/bin/env bash

SRC_RUN_ARGS_DIR=$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/most_common/2_shot/gpt-4o/wines-ontology
RUN_ARGS_DIR=$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/

LLM="gpt-4o"
SHOTS=(1 2 3 4 5 6 7 8 9 10)
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")

for i in "${SHOTS[@]}"; do
    for j in "${ONTOLOGIES[@]}"; do
        # cd "${RUN_ARGS_DIR}/${i}_shot/most_common/${LLM}/${j}"
        # echo $(pwd)
        for x in "${SRC_DIR}/${LLM}/${j}"/*; do
            echo ${x}
            # cp ${x} $(uuidgen).json
        done
        # find . \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s/1_shot/most_common/${i}_shot/g"
        # find . \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s/1-Shot/${i}-Shot/g"
        cd ../../../..
        echo "---"
    done
done
