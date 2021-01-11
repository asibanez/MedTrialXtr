gpu=0

# oversample_rate=5

#task: pos | ner
export TASK_NAME=ner
tagset=reaction
data_type=sent

export TASK_DIR=/data/rsg/chemistry/sibanez/01_chem_nlp/16_valid_annot_all_rev_sil_hg/03_role_recognition/01_run_all/01_run_3.0

export MODEL_DIR=$TASK_DIR

output_dir=$TASK_DIR

n_epochs=3
output_file="test.tags.preds"

CUDA_VISIBLE_DEVICES=${gpu} python3 run_tagging.py \
    --model_name_or_path ${MODEL_DIR} \
    --task_name $TASK_NAME \
    --tagset ${tagset} \
    --do_eval \
    --eval_on_test \
    --data_dir $TASK_DIR \
    --max_seq_length 256 \
    --per_gpu_eval_batch_size=8   \
    --per_gpu_train_batch_size=8   \
    --learning_rate 2e-5 \
    --num_train_epochs ${n_epochs} \
    --output_dir ${output_dir} \
    --write_outputs \
    --output_file ${output_file} \
    --overwrite_output_dir
    # --local_rank 2

# merge "test.pred"
test_file=${TASK_DIR}/test.txt
python3 compile_outputs.py \
    --test_file ${test_file} \
    --tag_file ${output_dir}/${output_file} \
    --output ${output_dir}/test.preds
echo "Compiled outputs to:", ${output_dir}/test.preds

