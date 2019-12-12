
# ttH multi-lepton DNN

This python script uses the Keras library to train deep neural network for ttH multilepton dilepton analysis region. The script is setup up to use a TensorFlow backend but can easily be setup to use other backends compatible with keras.

#### Authors: Joshuha Thomas-Wilsker (IHEP CAS CERN), Binghuan Li (IHEP CAS CERN)

## Introduction 
- The script and the setup in this .md has been written assuming one has install [anaconda][ana] on the local machine.
- Running on local machine takes advantages of anaconda, which brings many of the tools used in ML with just one install.
- Using Keras interface with Tensorflow backend to create DNN model for ttH multilpeton dilepton analysis region.
- Import all Keras libraries along with TensorFlow backend into pyROOT so that we can easily produce .root files.
- Also using ROOT library: necessary for book-keeping / ROOT data structures etc.
- All scripts will create .csv of input root files the first time they are run on the files.
- Outputs from training stored in hard-coded output directory in train-DNN.py. Similar story for application outputs.

[ana]:https://www.anaconda.com/distribution/

## Install packages
- Core packages: python=3.7.3, keras=2.3.1, tensorflow=2.2.0, root=6.18.04, root_numpy=4.8.0, scikit-learn=0.22,  matplotlib=3.1.2, numpy=1.16.4, pandas=0.25.3, seaborn=0.9.0
- Suggest to create new environment from the `environment.yml` file, the first line of the `yml` file sets the new environment's name.
```
conda env create -f environment.yml
```
- Activate the new environment: 
```
conda activate my_root_env
```

## DNN Training
Before you start, make sure you have input .root files stored somewhere and make sure the path to these files and the correct names are hardcoded into the train-DNN.py script. Also, make sure the input features in the input features .json you are using (e.g. input_vars_SigRegion_wFwdJet.json) exist in the input .root files you want to use. There is also currently some training region selection applied to the .root files before the .csv files are created. These use variables that are required to be in the input files. Please chekc this before running otherwise the code may crash.

Now, the first script to run is train_DNN.py. This script uses keras to train and test a DNN using Tensorflow. The input arguments are described below and more information can be found in the code:
```
python train-DNN.py -t <train and plot=1, plot only=0> -r <DiLepRegion> -s <training region selection>
```
e.g.:
```
python train-DNN.py -t 1 -s tH
```
4 ntuples (ttH signal, 'rest' reducible background, tt+W irreducible background, tHq signal) containing events selected in the ttH multilepton training region will be loaded. One will need to change the default directory path for the input root files. The .root files are converted to numpy data-frames and then .csv files to be read by Keras.

Global event weights / class weights are set in order to resolve the large class imbalance in the training dataset. The model is then built and trained using Keras+Tensorflow. A collection of outputs can be found in the output directory named in the script.

Outputs:
- The output data-frame is stored in your output directory so you don't have to create it each time you want to retrain.
- '.h5' file (stores multidimensional arrays of scientific data) stores model and model weights.
- Also output human readable model in serialised .json
- Model architecture displayed in a .png
- All diagnostic plots are stored inside a subdirectory called 'plots' e.g. overtraining, confusion matrices, loss-function evolution & output node distributions ('categorised' = only values where events value on this node was maximum of all nodes).
- The script relies on the 'plotting' package in order to make these.

The script
```
convert_hdf5_2_pb.py
```

Converts the .h5 model to .pb format so that it can be run in CMSSW framework. To convert model to be run in C++ framework refer to the package here:
```
https://github.com/BinghuanLi/lwtnn_example_lxplus
```

## DNN Application
Inside the `application` directory are the scripts that apply the trained networks in the signal region. To evaluate the network and add outputs to the input TTrees and create diagnostic distributions for the signal region, one can run the following script:
```
run_network_evaluation.py
```
This scripts will apply the network to the files found in the hardcoded input directory in the script (read from EOS to avoid having to store large/many files locally). Examples on how to run this script can be seen in the run_application_XXXX.sh scripts. The script uses many classes found in the 'apply.py' script in the 'evaluation' package.

A second script can make further diagnostics plots such as the stacked node response plots:
```
DNN_Evaluation_Control_Plots.py
```
This script can be run using the following example:
```
python DNN_Evaluation_Control_Plots.py -r <signal region = DiLepRegion> -d <0 = blinded, 1 = with data> -m <model dir>
```
For more information on the input arguments, one can check the code or use the -h option.

In order to run all nominal JES varied samples needed for fit machinery, one can run the script:
```
run_application_series_DiLepRegion.sh
```
The outputs from these scripts are stored in hardcoded directories in the code that one can change as needed. The plotting in these scripts also rely on the 'plotting' package.
