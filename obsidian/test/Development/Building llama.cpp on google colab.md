cmake -B build -DLLAMA_CUDA=ON

[[cmake]] --build build/ --config Release

Then I can run the: `bin/llama-cli -m path to the model -p "Prompt that we want to inference on" -ngl # of gpu layers that we want to have`


When we do this we are going to have an error where it does not have [[nvcc]]. And that is related to not having the nvidia-tool-kit installed.

In order for this to run with the gpu cores we are going to have to install the [[nvidia-tool-kit]] via `apt install nvidia-cuda-toolkit`