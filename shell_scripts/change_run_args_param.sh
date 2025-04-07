#!/usr/bin/env bash

RUN_ARGS_DIR=$HOME/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval
OUTPUT_PATH_PREFIX=/scratch/bhatt006/Results/llm_ontology_awareness/term_typing/ranked_retrieval
LLM="deepseekr1-distill-llama3-8B"

ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
# SHOTS=$(seq 1 10)
SHOTS=(0)
STRAT_SUFFIX=""
# STRAT_SUFFIX="/most_common"

for ont in "${ONTOLOGIES[@]}"; do
    for i in ${SHOTS}; do
        for j in ${RUN_ARGS_DIR}/${i}_shot${STRAT_SUFFIX}/${LLM}/${ont}/*; do
            echo ${j}
            # sed -i -e "s@${OUTPUT_PATH_PREFIX}/${ont}@${OUTPUT_PATH_PREFIX}/${i}_shot/most_common/llama3-7B/${ont}@g" ${j}
            sed -i - e "s@500@1500@g" ${j}
        done
    done
done

