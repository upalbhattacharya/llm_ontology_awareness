#!/usr/bin/env sh

SRC_DIR="~/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/1_shot/most_common"
for i in {2..10}; do
    for j in {astronomy-ontology,case-uco-owl-trafficking,wines-ontology}; do
        cd ${i}_shot/most_common/${j}/llama3-7B
        for x in $(${SRC_DIR}/${j}/llama3-7B/); do
            # cp ${x} $(uuidgen).json
            echo ${x}
        done
        cd ../../../..
    done
done
