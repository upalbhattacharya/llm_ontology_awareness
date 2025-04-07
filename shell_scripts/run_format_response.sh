#!/usr/bin/env bash
ARR=("astronomy-ontology" "case-uco-owl-trafficking" "wines-ontology")
LLM="deepseekr1-distill-llama3-8B"
shots=(0)
RUN="run_1"
for ont in "${ARR[@]}"; do
	echo $ont
	for i in "${shots[@]}"; do
        echo ${i}
		for j in "${HOME}/Results/llm_ontology_awareness/term_typing/ranked_retrieval/${i}_shot/${ont}/${LLM}"/*; do
			uid=$(basename "${j}")
			echo ${uid}
			python3 $HOME/PhD/Experiments/llm_ontology_awareness/src/llm_ontology_awareness/model/hugging_face/format_response_content/term_typing.py -f ${j}/${RUN}/responses.json \
				-l ${j}/${RUN}/label_mapping.json \
				-r "${HOME}/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval/${i}_shot/most_common/${ont}/${LLM}/${uid}.json"
		done
	done
done
