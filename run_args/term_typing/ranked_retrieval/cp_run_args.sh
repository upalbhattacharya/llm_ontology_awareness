#!/usr/bin/env sh

SRC_DIR=~/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/1_shot/most_common
for i in {2..10}; do
    for j in {astronomy-ontology,case-uco-owl-trafficking,wines-ontology}; do
        cd "$i_shot/most_common/$j/llama3-7B"
        echo $(pwd)
        echo "---"
        for x in "$SRC_DIR/$j/llama3-7B"/*; do
            echo ${x}

        done
        cd ../../../..
    done
done
