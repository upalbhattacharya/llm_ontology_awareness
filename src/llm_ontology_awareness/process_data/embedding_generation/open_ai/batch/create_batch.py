#!/usr/bin/env python

import ontospy
import polars as pl
from llm_ontology_awareness.model.open_ai.datasets.term_typing import (
    TermTypingRankedRetrievalDataset,
)
from llm_ontology_awareness.process_data.embedding_generation.open_ai.run_args import (
    RunArguments,
)
from tqdm import tqdm


def create_embedding_batch(
    run_args: RunArguments, **kwargs
) -> (list[dict], pl.DataFrame):
    model = ontospy.Ontospy(run_args.input, hide_individuals=False)

    tasks = []
    label_mapping = []

    if run_args.entity_type == "concepts":
        entities = [ent.locale for ent in model.all_classes]
    elif run_args.entity_type == "individuals":
        entities = [ent.locale for ent in model.all_individuals]
    else:
        raise Exception(f"Entity type {run_args.entity_type} not defined")
    print(entities)

    for i, ent_name in tqdm(enumerate(entities))):
        task = {
            "custom_id": f"embedding_task-{i}",
            "method": "POST",
            "url": "/v1/embeddings",
            "body": {
                "model": run_args.model,
                "input": ent_name,
                "encoding_format": run_args.encoding_format,
                "dimensions": run_args.dimensions,
            },
        }
        tasks.append(task)
        label_mapping.append((f"embedding_task-{i}", ent_name))
    df = pl.DataFrame(
        label_mapping,
        schema=[
            ("Custom ID", str),
            ("Entity Label", list[str]),
        ],
    )

    return tasks, df


if __name__ == "__main__":
    import argparse
    import json

    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--args_file",
        help="Path to `RunArguments` file",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    with open(args.args_file, "r") as f:
        args_raw = f.read()
        run_args = RunArguments.parse_raw(args_raw)

    tasks, df = create_embedding_batch(run_args)
    df.write_ndjson(os.path.join(run_args.output_dir, "embedding_mapping.json"))
    iterator = iter(tasks)

    for i in range(math.ceil(len(tasks) / 50000)):
        with open(
            os.path.join(
                run_args.output_dir,
                f"{run_args.entity_type}_embedding_batch_tasks_{i + 1}.jsonl",
            ),
            "w",
        ) as f:
            try:
                for j in range(50000):
                    f.write(json.dumps(next(iterator)) + "\n")
            except StopIteration:
                exit(0)
