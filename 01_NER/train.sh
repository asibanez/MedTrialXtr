gpu=1

# task: pos | ner
export TASK_NAME=ner
tagset=reaction

export TASK_DIR=/data/rsg/nlp/sibanez/00_MedTrialXtr/02_runs/00_NER/10_run_base_test_notab_bluebert_lowcase_40ep/

#model_dir: bert-base-cased, path_to_biobert, path_to_chembert
#export MODEL_DIR=bert-base-cased
export MODEL_DIR=/data/rsg/nlp/sibanez/00_MedTrialXtr/03_models/04_blueBERT/

output_dir=$TASK_DIR

n_epochs=40

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
    --save_steps -1 \
    --do_lower_case
    # --freeze_bert \
    # --local_rank 2
