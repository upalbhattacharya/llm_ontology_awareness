#!/usr/bin/env sh

SCRIPT_NAME="Experiments/llm_ontology_awareness/src/llm_ontology_awareness/metrics/results/term_typing.py"

DEPTH=4
Y_TRUE="Data/ontologies/wines-ontology/data/term_typing/ranked_retrieval/few_shot/2024-11-06/term_typing_ranked_retrieval_dataset.json"

ONTOLOGY="wines-ontology"
RESULTS_DIR="Results/llm_ontology_awareness/term_typing/ranked_retrieval/few_shot/$ONTOLOGY"

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
