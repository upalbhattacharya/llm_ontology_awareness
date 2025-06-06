#!/usr/bin/env bash
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
LLM="deepseekr1-distill-llama3-8B"
SHOTS=(0)
# RUN="run_2"
# STRAT_SUFFIX="/most_common"
STRAT_SUFFIX=""

for ont in "${ONTOLOGIES[@]}"; do
	for shot in "${SHOTS[@]}"; do
		for r_args in "${HOME}/Results/llm_ontology_awareness/term_typing/ranked_retrieval/${shot}_shot${STRAT_SUFFIX}/${LLM}/${ont}"/*; do
			uid=$(basename "${r_args}")
            for run_path in "${r_args}"/*; do
                echo ${run_path}
			    python3 $HOME/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/hugging_face/format_response_content/term_typing.py -f ${run_path}/responses.json \
				        -l ${run_path}/label_mapping.json \
				        -r "${HOME}/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/${shot}_shot${STRAT_SUFFIX}/${LLM}/${ont}/${uid}.json"
            done
		done
	done
done
