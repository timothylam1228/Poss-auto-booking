# POSS Helper

POSS Helper is a Python library for booking sport facility

## Pre-request

Docker https://www.docker.com/products/docker-desktop/
Docker CLI
Python

## Installation

1. Clone the project

```bash
git clone https://github.com/timothylam1228/polyu-faci-booking
```

2. Create a virtual environment for python

```bash
python -m venv venv
```

3. Activate the venv

```bash
.\venv\Scripts\activate
```

or (MAC)

```bash
source venv/bin/activate
```

4. Install the library

```bash
pip install -r requirements.txt
```

5. Pull the docker image

```bash
docker pull tensorflow/serving:nightly
```

## Usage

0. Create your own ocr model to bypass the captcha, example can be refer to https://github.com/emedvedev/attention-ocr

1. Serve the model with docker

```bash
docker run -t --rm -p 8501:8501 -v "{Project_dir}\{your_model_name}:/models/{your_model_name}" -e MODEL_NAME={your_model_name} tensorflow/serving:nightly
```

2. Run the python file under bot folder

## Setup

replace the booking data yourself

```json
{
  "develop": false, // is Develop mode
  "play_date": "18 Oct 2022", // Target Date
  "book_time": "2022-10-11 08:30:01", // Time to submit the booking
  "center": "HALL", // Select the sport center (HALL,FSC,SHAW)
  "account": [
    {
      "username": "xxxd",
      "password": "xxx",
      "start_time": "19:30" // Time slot
    },
    {
      "username": "xxxxd",
      "password": "xxx",
      "start_time": "20:30"
    }
  ]
}
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
