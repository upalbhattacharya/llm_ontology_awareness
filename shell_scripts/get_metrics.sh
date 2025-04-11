#!/usr/bin/env bash

ONTOLOGIES=("wines-ontology" "case-uco-owl-trafficking" "astronomy-ontology")
DATES=("2024-09-05" "2024-09-05" "2024-11-04")
# DATES=("2025-03-30" "2025-03-30" "2025-03-30")
DEPTHS=(4 8 10)

LLM="llama3-7B"
# LLM_SUFFIX="/runs"
LLM_SUFFIX=""
SHOTS=(0)
STRAT_SUFFIX=""
# STRAT_SUFFIX="/most_common"
# SHOTS=$(seq 1 10)
RESULTS_BASE_PATH=$HOME/Results/llm_ontology_awareness/term_typing/ranked_retrieval
DATA_BASE_PATH=$HOME/Data/ontologies

for shot in "${SHOTS[@]}"; do
    for ont_idx in "${!ONTOLOGIES[@]}"; do 
	    for r_args in "${RESULTS_BASE_PATH}/${shot}_shot${STRAT_SUFFIX}/${LLM}/${ONTOLOGIES[ont_idx]}"/*; do
            for run_path in "${r_args}${LLM_SUFFIX}"/*; do
                echo ${run_path}
                echo $DATES[ont_idx]}
                echo ${DEPTHS[ont_idx]}
		        # python3 ${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/metrics/results/term_typing.py \
                #         -yt "${DATA_BASE_PATH}/${ONTOLOGIES[ont_idx]}/data/term_typing/ranked_retrieval/${shot}_shot${STRAT_SUFFIX}/${DATES[ont_idx]}/term_typing_ranked_retrieval_dataset.json" \
                #         -yp ${run_path}/predictions.json \
                #         -n ranked_retrieval \
                #         --kwargs k=${DEPTHS[ont_idx]}
            done
        done
	done
done

