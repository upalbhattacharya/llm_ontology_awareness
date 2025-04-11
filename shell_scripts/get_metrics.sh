#!/usr/bin/env bash

ONTOLOGIES=(("wines-ontology" 4 "2024-09-05") ("astronomy-ontology" 10 "2024-11-04") ("case-uco-owl-trafficking" 8 "2024-09-05"))

# ONTOLOGIES=(("wines-ontology" 4 "2025-03-30") ("astronomy-ontology" 10 "2025-03-30") ("case-uco-owl-trafficking" 8 "2025-03-30"))

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
    for ont in "${ONTOLOGIES[@]}"; do 
	    for r_args in "${RESULTS_BASE_PATH}/${shot}_shot${STRAT_SUFFIX}/${LLM}/${ont[1]}"/*; do
            for run_path in "${r_args}${LLM_SUFFIX}"/*; do
                
		        python3 ${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/metrics/results/term_typing.py \
                        -yt "${DATA_BASE_PATH}/${ont[0]}/data/term_typing/ranked_retrieval/${shot}_shot${STRAT_SUFFIX}/${ont[2]}/term_typing_ranked_retrieval_dataset.json" \
                        -yp ${run_path}/predictions.json \
                        -n ranked_retrieval \
                        --kwargs k=${DEPTH}
            done
        done
	done
done

