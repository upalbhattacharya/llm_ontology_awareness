#!/usr/bin/env bash

SRC_DIR=~/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/2_shot/most_common/
RUN_ARGS_DIR=$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/
LLM="gpt-4o"
SHOTS=$(seq 1 10)
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
for i in "${SHOTS[@]}"; do
    echo ${i}
    for j in "${ONTOLOGIES[@]}"; do
        echo ${j}
        cd "${RUN_ARGS_DIR}/${i}_shot/most_common/${LLM}/${j}"
        echo $(pwd)
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
