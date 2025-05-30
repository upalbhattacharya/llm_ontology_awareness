#!/usr/bin/env sh

REF_JOB=~/PhD/Experiments/llm_ontology_awareness/jobs/term_typing/ranked_retrieval/sample_job
BASE_RUN_ARGS_PATH=~/PhD/Experiments/llm_ontology_awareness/run_args/term_typing/ranked_retrieval
BASE_JOBS_PATH=~/PhD/Experiments/llm_ontology_awareness/jobs/term_typing/ranked_retrieval
for i in {1..10}; do
    for j in {astronomy-ontology,wines-ontology,case-uco-owl-trafficking}; do
        dest_path="${BASE_JOBS_PATH}/${i}_shot/${j}/llama3-7B"
        cd ${dest_path}
        echo $(pwd)
        for run_args in "${BASE_RUN_ARGS_PATH}/${i}_shot/most_common/${j}/llama3-7B"/*; do
            uuid=$(basename ${run_args} .json)
            echo ${uuid}
            cp ${REF_JOB} job_${uuid}
            $(sed -i -e "s@job_path@${run_args}@g" "job_${uuid}")
        done
    done
done


