#!/usr/bin/env sh

SCRIPT_NAME="Experiments/llm_ontology_awareness/src/llm_ontology_awareness/metrics/results/term_typing.py"

DEPTH=8
Y_TRUE="Data/ontologies/case-uco-owl-trafficking/data/term_typing/ranked_retrieval/2024-09-05/term_typing_ranked_retrieval_dataset.json"

ONTOLOGY="case-uco-owl-trafficking"
RESULTS_DIR="Results/llm_ontology_awareness/term_typing/ranked_retrieval/zero_shot/$ONTOLOGY"

# Check for environment
echo $(which python)

# Set paths from home directory
cd "$HOME"

for model_dir in $RESULTS_DIR/*/
do
    model_dir=${model_dir%*/} 
    for variant_dir in $model_dir/*/
    do
        variant_dir=${variant_dir%*/} 
        for run_dir in $variant_dir/runs/*/
        do
            run_dir=${run_dir%*/}
            echo $run_dir
            python $SCRIPT_NAME \
                   -yt $Y_TRUE \
                   -yp $run_dir/predictions.json \
                   -n ranked_retrieval \
                   -k k=$DEPTH
        done
    done
done
