# SAST-MT

SAST-MT is a metamorphic testing framework designed to detect false positives (FPs), false negatives (FNs), and analysis failures (AFs) in SAST tools. Given the popularity of CodeQL, we only support testing of CodeQL in our current release. Nevertheless, SAST-MT can easily be extended to support any other SAST framework. Our mutators can also be easily adopted or extended to the C/C++ code generator of any existing test pipeline. For more details on our study of state-of-the-art SAST tools, please refer to our paper, **Evaluating C/C++ Vulnerability Detectability of Query-Based Static Application Security Testing Tools**, published in **IEEE Transactions on Dependable and Secure Computing (TDSC)**. 

## High level overview of our framework

Our framework attempts to detect analysis inconsistencies by first applying semantics-preserving mutations to the seed (with known vulnerabilities identified by honggfuzz) and recording the mutant and its corresponding parent if any inconsistency is detected.
We have implemented 15 transformation passes for our testing framework. Each mutation transforms programs at different levels, including types, structures, and data flow. You can find a list of simplified examples [here](mutator.md), which provide a high-level overview of how the transformations work. 

## Issue we reported

Within 100 hours of testing, our framework detected 17 false positive and 228 false negatives of CodeQL. Given a large number of founding from testing CodeQL, we only listed and reported two types of FNs and two types of FPs we were able to generalize and reproduce manually in most of the related seed-QL pairs. Please check [here](issue.md) for details.

## Getting started with Docker

Follow [here](https://docs.docker.com/engine/install/) to install docker if didn't.

After installed docker, then do:

```bash
docker build -t sast-mt .
```

After the container is built, you can run the following to start it  

```bash
docker run --name=sast-mt -itd sast-mt bash 
```

To get in the container, you can run 

```bash
docker exec -it sast-mt bash
```

## Installation procedure (If not using docker)

You can also build on a Ubuntu machine by following steps

0. Download this repo and change directory to this repo.

1. Install python:
```bash
sudo apt install -y python-dev wget 
sudo apt install -y python3-dev  
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo apt install -y libpythonX-dev # libpython3.7-dev
```

2. Install Comby 
```bash
sudo apt install -y libev-dev clang-format
pip3 install comby
bash <(curl -sL get.comby.dev)
```

3. Install treesitter 
```bash
pip3 install tree-sitter==0.19.0
git clone https://github.com/tree-sitter/tree-sitter-cpp.git
git clone https://github.com/tree-sitter/tree-sitter-c.git
python3 build_treesitter_parser.py
```

After finish the above installation steps, you can cd to the /root/fuzzer/ (if you are in docker) OR ./src/

```bash
python3 fuzzer.py # Please check the usage section for details 
```

# Usage 

```bash
usage: fuzzer.py [-h] -s SEED -c CMD -q QL [-hf HOME_FOLDER] [-b BUILD_REQUIRED [BUILD_REQUIRED ...]] [-O OPT] [-max_iter MAX_RUN]

SAAS Fuzzing

optional arguments:
  -h, --help            show this help message and exit
  -s SEED, --seed SEED  File path to the seed file for mutation
  -c CMD, --cmd CMD     The command for building the given seed
  -q QL, --QL QL        The QL files required for testing
  -hf HOME_FOLDER, --home_folder HOME_FOLDER
                        The path to save the output
  -b BUILD_REQUIRED [BUILD_REQUIRED ...], --build_required BUILD_REQUIRED [BUILD_REQUIRED ...]
                        space delimited list of path
  -O OPT, --opt OPT     Compiler optimization level for testing, option 0,1,2,3. By default, we follow the opion of the cmd
  -max_iter MAX_RUN, --max_run MAX_RUN
                        The number of maximal cycle we execute the fuzzer

```

# Usage example 

After running the below command, our fuzzer will keep on mutate the testcase (CWE-119_tests.cpp here) until timeout (by default, it is set to 60 minutes)

```bash
python3 fuzzer.py -hf /root/ -s /root/CWE-119_tests.cpp -c "g++ -c CWE-119_tests.cpp" -q "/root/codeql-codeql-cli-v2.8.1/cpp/ql/src/Security/CWE/CWE-119/OverflowBuffer.ql" 
```

To check the result, you can go to /root/CWE-119_tests_OverflowBuffer/ OR any path specified in the ```-hf```  

The test case triggered inconsistency can be found under the failure folder, while perf logging can be found in the status.log file. 

# Case triaging 

cd to the ```./failure/``` folder

- if the folder starts with ```ANALYSIS_FAILURE_less_```, it means some lines were missing form the analysis result of the mutatnt compare to the seed.

- if the folder starts with ```ANALYSIS_FAILURE_more_```, it means some extra lines were found in the analysis result of the mutatnt compare to the seed.

You can try to look for the difference by: 

If the seed is a C file:

```bash
diff child.c parent.c
```

If the seed is a C++ file:

```bash
diff child.cpp parent.cpp
```


