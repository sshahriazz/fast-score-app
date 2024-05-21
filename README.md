### Installation

```
git clone https://github.com/sshahriazz/fast-score-app
cd fast-score-app
git checkout ResumeAI
```

### Env Setup

```
python -m venv resume-env
source resume-env/bin/activate
pip install -r requirements.txt
```


### OpenAI Key Set

```
# add the line in ~/.bashrc file of Linux OS
export OPENAI_API_KEY=your-api-key-here
source ~/.bashrc
```

### Run
```
fastapi dev server.py
```