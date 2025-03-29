#!/usr/bin/env sh

for i in {2..10}; do
    for j in {astronomy-ontology,case-uco-owl-trafficking,wines-ontology}; do
        cd ${i}_shot/most_common/${j}/llama3-7B
        for x in 1_shot/most_common/${j}/llama3-7B/*.json; do
            # cp ${x} $(uuidgen).json
            echo ${x}
            echo $(.)
        done
        cd ../../../..
    done
done
