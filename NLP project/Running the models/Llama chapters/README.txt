In order to run this model, you need to create an environment 
with the following dependencies

$ conda create --name torch_test_3 pytorch torchvision torchaudio pytorch-cuda=12.1 transformers -c pytorch-nightly -c nvidia

otherwise the GPUS will not work

We also did not include the output in this folder as it would have wasted space
The result for this are in /code/Scoring/data/resLlama