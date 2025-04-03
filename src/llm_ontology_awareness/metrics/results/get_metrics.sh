#!/usr/bin/env bash

ONT="case-uco-owl-trafficking"
DEPTH=8
for i in $(seq 1 10); do
	for j in "${HOME}/Results/llm_ontology_awareness/term_typing/ranked_retrieval/${i}_shot/most_common/${ONT}/llama3-7B"/*; do
		./term_typing.py -yt ${HOME}/Data/ontologies/${ONT}/data/term_typing/ranked_retrieval/${i}_shot/most_common/2025-03-30/term_typing_ranked_retrieval_dataset.json -yp ${j}/run_2/predictions.json -n ranked_retrieval --kwargs k=${DEPTH}
	done
done

