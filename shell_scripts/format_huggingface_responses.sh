#!/usr/bin/env bash
ONTOLOGIES=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
LLM="llama3-7B"
SHOTS=(3)
# RUN="run_2"
STRAT_SUFFIX="/most_common"

for ont in "${ONTOLOGIES[@]}"; do
	for shot in "${SHOTS[@]}"; do
		for r_args in "${HOME}/Results/llm_ontology_awareness/term_typing/ranked_retrieval/${shot}_shot${STRAT_SUFFIX}/${LLM}/${ont}"/*; do
			uid=$(basename "${j}")
            for run_path in "${r_args}"/*; do
                echo ${run_path}
			    # python3 $HOME/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/hugging_face/format_response_content/term_typing.py -f ${j}/${RUN}/responses.json \
				#         -l ${j}/${RUN}/label_mapping.json \
				#         -r "${HOME}/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/${i}_shot/${LLM}/${ont}/${uid}.json"
            done
		done
	done
done
