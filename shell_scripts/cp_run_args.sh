#!/usr/bin/env sh

SRC_DIR=~/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/2_shot/most_common/
LLM="gpt-4o"
for i in {2..10}; do
    for j in {astronomy-ontology,case-uco-owl-trafficking,wines-ontology}; do
        cd "${i}_shot/most_common/${LLM}/${j}"
        echo $(pwd)
        for x in "${SRC_DIR}/${LLM}/${j}"/*; do
            # cp ${x} $(uuidgen).json
        done
        # find . \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s/1_shot/most_common/${i}_shot/g"
        # find . \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i "s/1-Shot/${i}-Shot/g"
        cd ../../../..
        echo "---"
    done
done
