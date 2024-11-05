#!/usr/bin/env sh

SCRIPT_NAME="Experiments/llm_ontology_awareness/src/llm_ontology_awareness/metrics/results/term_typing.py"

DEPTH=4
Y_TRUE="Data/ontologies/wines-ontology/data/term_typing/ranked_retrieval/2024-09-05/term_typing_ranked_retrieval_dataset.json"

RESULTS_DIR="Results/llm_ontology_awareness/term_typing/ranked_retrieval/zero_shot/wines-ontology"

# Check for environment
echo $(which python)

cd "$HOME"

# GPT-4o

python $SCRIPT_NAME \
       -yt $Y_TRUE \
       -yp $RESULTS_DIR/gpt-4o/34be5cbb-9f49-4e85-af5d-9c2444fb66e2/runs/run_1/responses.json \
       -n ranked_retrieval \
       -k k=$DEPTH

python $SCRIPT_NAME \
       -yt $Y_TRUE \
       -yp $RESULTS_DIR/gpt-4o/520aa919-1326-4f1d-bb46-bde3ef86a74d/runs/run_1/responses.json \
       -n ranked_retrieval \
       -k k=$DEPTH

python $SCRIPT_NAME \
       -yt $Y_TRUE \
       -yp $RESULTS_DIR/gpt-4o/5b1111cc-902b-465b-9e4f-257774be59b0/runs/run_1/responses.json \
       -n ranked_retrieval \
       -k k=$DEPTH

python $SCRIPT_NAME \
       -yt $Y_TRUE \
       -yp $RESULTS_DIR/gpt-4o/5d599257-8bf3-4470-96ff-4f344bcc6947/runs/run_1/responses.json \
       -n ranked_retrieval \
       -k k=$DEPTH

# Llama3-7B

python $SCRIPT_NAME \
       -yt $Y_TRUE \
       -yp $RESULTS_DIR/llama3-7B/34be5cbb-9f49-4e85-af5d-9c2444fb66e2/predictions.json \
       -n ranked_retrieval \
       -k k=$DEPTH

python $SCRIPT_NAME \
       -yt $Y_TRUE \
       -yp $RESULTS_DIR/llama3-7B/520aa919-1326-4f1d-bb46-bde3ef86a74d/predictions.json \
       -n ranked_retrieval \
       -k k=$DEPTH

python $SCRIPT_NAME \
       -yt $Y_TRUE \
       -yp $RESULTS_DIR/llama3-7B/5b1111cc-902b-465b-9e4f-257774be59b0/predictions.json \
       -n ranked_retrieval \
       -k k=$DEPTH

python $SCRIPT_NAME \
       -yt $Y_TRUE \
       -yp $RESULTS_DIR/llama3-7B/5d599257-8bf3-4470-96ff-4f344bcc6947/predictions.json \
       -n ranked_retrieval \
       -k k=$DEPTH
# o1-preview




