#!/usr/bin/env bash

ONTOLOGIES=(("wines-ontology" 4 "2024-09-05") ("astronomy-ontology" 10 "2024-11-04") ("case-uco-owl-trafficking" 8 "2024-09-05"))

# ONTOLOGIES=(("wines-ontology" 4 "2025-03-30") ("astronomy-ontology" 10 "2025-03-30") ("case-uco-owl-trafficking" 8 "2025-03-30"))

LLM="llama3-7B"
SHOTS=(0)
STRAT_SUFFIX=""
# STRAT_SUFFIX="/most_common"
# SHOTS=$(seq 1 10)
RESULTS_BASE_PATH=$HOME/Results/llm_ontology_awareness/term_typing/ranked_retrieval

for shot in "${SHOTS[@]}"; do
    for ont in "${ONTOLOGIES[@]}"; do 
	    for r_args in "${HOME}/Results/llm_ontology_awareness/term_typing/ranked_retrieval/${shot}_shot${STRAT_SUFFIX}/${LLM}/${ont[1]}"/*; do
		    python3 ${HOME}/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/metrics/results/term_typing.py \
                    -yt "${RESULTS_BASE_PATH}/${i}_shot${STRAT_SUFFIX}/${DATE}/term_typing_ranked_retrieval_dataset.json \
                    -yp ${j}/${RUN}/predictions.json \
                    -n ranked_retrieval \
                    --kwargs k=${DEPTH}
        done
	done
done

