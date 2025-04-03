#!/usr/bin/env bash
ARR=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
for ont in "${ARR[@]}"; do
	echo $ont
	for i in $(seq 1 10); do
		for j in "${HOME}/Results/llm_ontology_awareness/term_typing/ranked_retrieval/${i}_shot/most_common/${ont}/llama3-7B"/*; do
			uid=$(basename "${j}")
			echo ${uid}
			./term_typing.py -f ${j}/run_2/responses.json \
				-l ${j}/run_2/label_mapping.json \
				-r "${HOME}/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/${i}_shot/most_common/${ont}/llama3-7B/${uid}.json"
		done
	done
done
