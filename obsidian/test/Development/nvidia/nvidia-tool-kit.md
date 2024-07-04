You will need to download the nvidia-tool-kit to get libraries like llama.cpp working with GPUs
https://developer.nvidia.com/cuda-downloads

Windows: Just download it from the website and install

Linux:
	`apt install nvidia-cuda-toolkit`



The NVIDIA toolkit, often referred to as the NVIDIA CUDA Toolkit, is a comprehensive suite of software development tools and libraries for developing applications that leverage the parallel computing power of NVIDIA GPUs (Graphics Processing Units). The CUDA (Compute Unified Device Architecture) Toolkit provides everything needed to develop GPU-accelerated applications, including:

### Key Components of the NVIDIA CUDA Toolkit

1. **CUDA Compiler (nvcc)**:
   - The CUDA compiler (nvcc) allows developers to compile CUDA code, which is written in a C-like language, into executable programs that can run on NVIDIA GPUs.

2. **CUDA Runtime Library**:
   - This library provides a set of APIs that allow applications to manage and use GPU resources, including memory management, kernel execution, and device management.

3. **CUDA Driver API**:
   - The CUDA driver API offers low-level control over GPU operations, providing more flexibility and control compared to the runtime API. It is often used for advanced applications requiring fine-grained GPU control.

4. **CUDA Libraries**:
   - NVIDIA provides several optimized libraries to help accelerate application development, including:
     - **cuBLAS**: Optimized implementations of BLAS (Basic Linear Algebra Subprograms) operations.
     - **cuFFT**: Fast Fourier Transform library.
     - **cuRAND**: Random number generation.
     - **cuSPARSE**: Sparse matrix operations.
     - **cuDNN**: Deep neural network library, which is crucial for AI and deep learning applications.
     - **Thrust**: A parallel algorithms library which resembles the C++ Standard Template Library (STL).

5. **CUDA Tools**:
   - A set of tools to aid in development and debugging, such as:
     - **CUDA-GDB**: A powerful debugger for CUDA applications.
     - **CUDA-MEMCHECK**: A tool to check for memory errors in CUDA applications.
     - **Nsight Systems**: A performance analysis tool to profile and optimize CUDA applications.
     - **Nsight Compute**: An interactive kernel profiler for CUDA applications.

6. **CUDA Samples**:
   - The toolkit includes a range of sample projects and code examples demonstrating various CUDA features and best practices. These samples can be used as a starting point for developing custom CUDA applications.

### Typical Workflow

1. **Installation**: Download and install the CUDA Toolkit from the NVIDIA website, ensuring compatibility with your NVIDIA GPU and operating system.
2. **Development**: Write CUDA code in a host (CPU) and device (GPU) setup, where the CPU offloads parallelizable tasks to the GPU.
3. **Compilation**: Use the `nvcc` compiler to compile the CUDA code.
4. **Execution**: Run the compiled application, leveraging the GPU for high-performance computing tasks.
5. **Debugging and Profiling**: Use the provided tools to debug and profile the application, optimizing performance and ensuring correctness.

### Use Cases

The CUDA Toolkit is widely used in various fields, including:

- **Scientific Computing**: Accelerating simulations, mathematical computations, and data analysis.
- **Deep Learning and AI**: Training and inference for neural networks, leveraging GPUs for faster processing.
- **High-Performance Computing (HPC)**: Enhancing computational capabilities for research and large-scale computations.
- **Graphics and Image Processing**: Improving rendering times and processing large datasets of images and videos.

### Getting Started

To get started with the NVIDIA CUDA Toolkit:

1. **Install the Toolkit**: Follow the installation guide on the [NVIDIA CUDA Toolkit website](https://developer.nvidia.com/cuda-toolkit).
2. **Explore the Samples**: Review and run the sample applications included in the toolkit to understand basic and advanced CUDA programming concepts.
3. **Refer to the Documentation**: The official documentation provides detailed information on all components of the toolkit, including API references and user guides.
4. **Join the Community**: Engage with the CUDA developer community through forums and events to learn from others and share your experiences.

By leveraging the NVIDIA CUDA Toolkit, developers can harness the power of GPU acceleration to significantly enhance the performance of their applications across a wide range of domains.