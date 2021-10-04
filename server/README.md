# NFT Factory Server

## How to setup server

Create a virtual environment under server folder
```
python -m venv
```
Activate  virtual environemnt
```
Windows Command: . venv/Scripts/Activate
```

Locate requirements.txt file, in the directory its located run the following command

```
pip install -r requirements.txt
```

```
Create .env file located under server directory
Add the following to the .env file

pinata_api_key="<Insert Api Key>"
pinata_secret="<Insert Secret>"
infura_id="<Add Infura Project Id>"
```

To run app then 
```
cd src
Flask run
```