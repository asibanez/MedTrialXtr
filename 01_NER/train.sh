gpu=1

# task: pos | ner
export TASK_NAME=ner
tagset=reaction

export TASK_DIR=/data/rsg/nlp/sibanez/00_MedTrialXtr/02_runs/00_NER/03_run_split_juan_80-20/

#model_dir: bert-base-cased, path_to_biobert, path_to_chembert
#export MODEL_DIR=/data/rsg/chemistry/sibanez/11_MedTrialExtractor/02_models/00_blueBERT/
export MODEL_DIR=bert-base-cased

output_dir=$TASK_DIR

n_epochs=10

CUDA_VISIBLE_DEVICES=${gpu} python3 run_tagging.py \
    --model_name_or_path ${MODEL_DIR} \
    --task_name $TASK_NAME \
    --tagset ${tagset} \
    --do_train \
    --do_eval \
    --data_dir $TASK_DIR \
    --max_seq_length 512 \
    --per_gpu_eval_batch_size=8   \
    --per_gpu_train_batch_size=8   \
    --learning_rate 3e-5 \
    --num_train_epochs ${n_epochs} \
    --output_dir ${output_dir} \
    --overwrite_output_dir \
    --evaluate_during_training \
    --logging_steps 200 \
    --save_steps -1
    # --freeze_bert \
    # --local_rank 2
