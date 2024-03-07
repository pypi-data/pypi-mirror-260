# GPT Service

Welcome to the GPT Service README! This service utilizes OpenAI's GPT (Generative Pre-trained Transformer) model to interact with AWS services and Google Shopping.



## Features

- **Text Generation**: Generate human-like text based on given prompts.
- **Deploy Public cloud AWS services**(Supported services: ec2,s3)
- **Google Shoppin**: Assistant can search for products on Google Shopping.



## Getting Started: 

### Local Setup for development

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Setup your environment variables:

```bash
export aws_secret_key=YOUR_AWS_SECRET_KEY
export aws_access_key=YOUR_AWS_ACCESS_KEY
export openai_key=YOUR_OPENAI_KEY
```

3. Run the main script 

```bash
python -m gptservice.apps
```


### Local Setup for personal use

1. Install the gptservice package:

```bash
pip install gptservice
```

2. Setup your environment variables:

```bash
export aws_secret_key=YOUR_AWS_SECRET_KEY
export aws_access_key=YOUR_AWS_ACCESS_KEY
export openai_key=YOUR_OPENAI_KEY
```
3. Run the binary

```bash
gptservice
```


## Contributing:

Contributions are welcome. Please submit a pull request.

## Contributors

A list of contributors can be found at [Contributors](https://github.com/samroffe/gptservice/graphs/contributors).


## License
This project is licensed under the terms of the MIT license.