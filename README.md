# Artifact of the paper "Accounting for Missing Events in Statistical Information Leakage Estimation"

## Repository Description (Purpose)

This replication repository contains the data, result, and scripts for the paper "Accounting for Missing Events in Statistical Information Leakage Estimation" accepted at the 47th International Conference on Software Engineering (ICSE 2025). The artifact is intended to reproduce the results in the paper and to provide the estimation results for the readers to analyze the information leakage of their own systems. The authors of the artifact claim 'Available,' 'Functional,' and 'Reusable' badges as the artifact is available for download, the scripts are functional, and well-documented for reuse.

## Provenance

The preprint of the paper is available at [Link](https://nimgnoeseel.github.io/resources/paper/leak.pdf).

## Requirements

- python 3
- numpy
- scipy
- pandas
- matplotlib
- seaborn
- jupyter

## Structure

```bash
$ tree .
.
├── README.md                       # This file
├── HyLeak-data/                    # Subject programs (HyLeak IR) and results of HyLeak for RQ1-3
├── data1M/                         # Directory containing the 1M samples for the ground truth of the subject programs for RQ1-3
├── data-epassport/                 # Directory containing the data for the ePassport experiment (RQ4)
├── data-LocPrivacy/                # Directory containing the data for the location privacy experiment (RQ4)
├── result/                         # Directory containing the results of estimation for RQ1-3
├── figures/                        # Directory containing the figures for the paper
├── notebook                        # Directory containing the Jupyter notebooks for the paper
│   ├── RQ1-RQ2(partial).ipynb      # Notebook for RQ1 and RQ2
│   ├── RQ1-RQ2(partial)-normalized.ipynb # Notebook for RQ1 and RQ2 with normalized results
│   │                                     # (the results are normalized by the log of the secret domain size (i.e., the maximum MI))
│   ├── RQ2.ipynb                   # Notebook for RQ2
|   ├── RQ2-normalized.ipynb        # Notebook for RQ2 with normalized results
│   ├── RQ3.ipynb                   # Notebook for RQ3
│   ├── LocPrivacyProbgen.ipynb     # Notebook for generating the joint distribution of LPPMs
│   ├── RQ4-ePassport.ipynb         # Notebook for RQ4 on ePassport experiment
│   └── RQ4-figgen.ipynb            # Notebook for generating the figures for RQ4
├── Dockerfile                      # Dockerfile for building the replication environment
├── chao.py
├── empirical.py
├── estimate.py
├── experiment.py
├── ground_truth.py
├── lychee.py
├── miller.py
├── util.py
├── run-para.py                     # Script for running the experiments for RQ1-3
├── combine-hyleak-result.py        # Script for combining the results of HyLeak
└── run-locprivacy.py               # Script for running the experiments for RQ4, location privacy
```

## Usage

### Preparation

#### Installation on Bare-Metal 

\#1: Download the repository and install Python 3 with the required packages written in the `requirements.txt` file. You can use the following command:
```bash 
$ pip3 install -r requirements.txt
```
If you are installing this in a more recent version of Linux, you may initially receive an `error: externally-managed-environment` message. In this case, you may either install the requirements within a python virtual environment, or you can override the warning at your own risk with the addition of the flag `--break-system-packages`.

\#2: Run the jupyter notebook service with the command:

```bash
$ jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```
\#3: The service will produce a message stating something along the lines of:

```
 To access the server, open this file in a browser:
        file:///home/xxxxxx/.local/share/jupyter/runtime/jpserver-16695-open.html
    Or copy and paste one of these URLs:
        http://xxxxxx:8888/tree?token=xxxxx
        http://127.0.0.1:8888/tree?token=xxxxxx
```
The final displayed link is the most reliable, copy-paste it into your browser of choice in order to view and run the jupyter notebooks.

#### (Optional) Build Docker Image

If you want to run the experiments in a Docker container, start here and ignore the earlier set of instructions. You can build the Docker image with the following command:

```bash
$ docker build -t icse2025-replication .
```

Then, you can run the container with the following command with the port 8888 exposed:

```bash
$ docker run -it -p 8888:8888 icse2025-replication
```

Run the Jupyter notebook server in the container with the following command:

```bash
$ jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

Then, you can access the Jupyter notebook server at the URL shown in the terminal. This will most likely be the third option listed in the dropdown.
```
    Or copy and paste one of these URLs:
        http://127.0.0.1:8888/tree?token=xxx
```

If you face `*.ubuntu.com host inaccessible` error, one possible solution is to add `--network=host` option to the `docker build` and `docker run` commands.


### 1. Analysis and Visualization: Reproduce the tables and figures in the paper

The estimation results for RQ1-3 and RQ4 are already provided in the `result/`, `data-LocPrivacy/`, and `data-epassport/` directories. If you want to reproduce the tables and figures in the paper, follow the instructions in the next section. Here, we use the notebooks in the `notebook/` directory to analyze the results and generate the figures.

- **RQ1 and RQ2**: Run the notebook `RQ1-RQ2(partial).ipynb` and `RQ2.ipynb` in the `notebook/` directory.
- **RQ3**: Run the notebook `RQ3.ipynb` in the `notebook/` directory.
- **RQ4**: Run the notebook `RQ4-figgen.ipynb` and `RQ4-ePassport.ipynb` in the `notebook/` directory.

### 2. Generate the estimation results for RQ1-3 and RQ4

In this section, we provide the instructions to generate the estimation results for RQ1-3 and RQ4.

#### 2-1. Run the experiments for RQ1-3

First, set the parameters:

- the number of repetitions for each configuration, i.e., (subject, sample ratio) pair in the script `run-para.py` (`NUM_RUNS_PER_NUM_SAMPLES`); 30 is the number we used in the paper.
- the number of repetitions for our proposed method with the same sample in the script `run-para.py` (`NUM_RUNS_PER_NUM_SAMPLES`); 30 is the number we used in the paper.
- the number of cores for parallel computation in the script `experiment.py` (`MAX_CORES`).

Then, run the script with the following command with the data in the `data1M/` directory:

```bash
$ python3 run-para.py
```

The script will generate the results in the `result/` directory. The time to run the script may take a long time (more than a day) depending on the computational environment: in our experiment, we used a server with 64-Core server with 256 GB of RAM to run the experiments with 30 repetitions for each configuration and 30 repetitions for our proposed method. But, the time mainly takes for the subject with a large domain size (e.g., 'reservior' and 'random walk'). In the script `run-para.py`, we suggest a smaller size experiment by commenting out the subject programs with a large domain size and less repetitions (5 $\times$ 5) with less cores (5). For a regular laptop, the expected time to run `run-para.py` is less than 30 minutes.

##### Combine the results of HyLeak

Run the script `combine-hyleak-result.py` with the following command (less than a minute):

```bash
$ python3 combine-hyleak-result.py
```

#### 2-2. Run the experiments for RQ4

- **Location Privacy**

`prob_df-Opt.csv` and `prob_df-PG2.csv` in the `data-LocPrivacy/` directory are the pre-generated joint probability distribution of LPPMs, which are used for the location privacy experiment. They are generated by the notebook `LocPrivacyProbgen.ipynb` in the `notebook/` directory with the data `data-LocPrivacy/Gowalla_totalCheckins.txt`.

To estimate the MI, first, set the number of cores for parallel computation in the script `run-locprivacy.py` (`MAX_CORES`).

Then, run the script with the following command:

```bash
$ python3 run-locprivacy.py --subject {pg2,opt} --maxsample M --numruns N
```

where `M` is the maximum number of samples to use. the number of samples considered will be $400$ (the domain size of the secret location)$ \times 2^i$ for $i \in [0..]$ until the maximum number of samples is reached.

For example, to run the experiments for the optimal mechanisms proposed by Oya et al. (Blahut-Arimoto method) with 1M samples and 30 runs (the experiment we conducted in the paper)

```bash
$ python3 run-locprivacy.py --subject opt --maxsample 1000000 --numruns 30
```

The script will generate the results in the `data-LocPrivacy/` directory. The expected time to run the script with 1M samples is less than two minutes given the same number of cores as the number of runs.

- **ePassport Privacy**

Run the notebook `RQ4-ePassport.ipynb` in the `notebook/` directory with the data `data-epassport/raw-time-data/*.csv`.

The notebook will generate the results in the `data-epassport/estimate` directory.


## Extending the Artifact

The artifact can be easily extended to analyze the information leakage of other systems. All one needs to do is to provide the information of the ground truth joint probability distribution of the secret and the public variables. The way to provide the information is to generate a sample matrix of the joint distribution with a sufficient amount of samples (so that the empirical distribution is close to the true distribution), and save it as a CSV file under the `data1M/` directory. Please refer to the `data1M/` directory for the format of the CSV file. Finally, add the name of the new subject system with the domain size to the `run-para.py` script and run the script.

## License

The code in this repository is licensed under the MIT License.

## Contact

If you have any questions or need help with the artifact, please contact Seongmin Lee at [seongmin.lee@mpi-sp.org](mailto:seongmin.lee@mpi-sp.org).
