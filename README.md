### What this contains?

There are 4 files excluding README file
```
.gitignore
requirements.txt
.env
app.py
```

### Pre-requisites

STEP 1 - Get this project to the project folder

```
git clone <this project> 
```

STEP 2 - Get the numind/NuExtract-v1.5 model from https://huggingface.co/numind/NuExtract-v1.5. I recommend having the model folder in a subfolder within the project folder itself

``` 
git lfs install
git clone https://huggingface.co/numind/NuExtract-v1.5
```

STEP 3 - Create a python virtual environment in the project folder 
```
python -m venv myenv
```

STEP 4 - Activate the newly created python virtual environment in the project folder 
```
source myenv/bin/activate
```

STEP 5 - Install requirements.txt contents to the newly created virtual environment

```
pip install --upgrade pip
pip install -r requirements.txt
```

### Set up and run app.py 
STEP 6 - Check the following line in .env file, change the path to nuextract-v1.5 model folder if needed.

```
NUEXTRACT_1_5_MODEL_PATH='./NuExtract-v1.5'
```

STEP 7 - In app.py change the following line to right deployment settings.

```
    app.run(debug=True, host='0.0.0.0', port=6999)
```

STEP 8 At command line in the project folder run. (Ensure that myenv is active and not base env)

```
python app.py  
```

This should show messages "loading model first time" and "model successfully loaded"

STEP 9 Open another terminal window, go to poroject folder. Activate python virtual env using Step 4. Test the correct working by running 
```
python test_NuExtract_1_5_client.py 
```


