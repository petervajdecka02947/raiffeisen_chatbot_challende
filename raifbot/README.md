# RaifBot Generative AI Chatbot
This generative chatbot repository was created for the Python AI Code Challenge at Raiffeisen Bank Vienna.

## Access to this work:
- This work has been done and tested in a Linux (Ubuntu) environment.
- You can directly try this demo on my domain [**vajpet.com**](http://vajpet.com).
- Run `docker-compose up -d` to create a package that can be accessed at your `localhost`.

### Demo
- This is the easiest way to access this work.
- Navigate to **vajpet.com** and all details will be provided on the website.
- This website is running on an AWS EC2 instance server.

#### Custom domain address (OPTIONAL)
- The repository is set primarily to HTTP, but I run the demo securely on HTTPS.
- To run it on your own domain, you need to do the following steps:
   - Create your own domain.
   - Get DNS A records for `<your_domain>` and `www.<your_domain>` and add your endpoint to it.
   - Obtain SSL certificates (I used CertBot in my Linux environment).
   - Add SSL certificates to nginx with domains and redirect HTTP and HTTPS to only HTTPS.
   - Then just set your domain in nginx.conf in the HTTPS folder and copy-paste all files from the HTTPS folder to the root directory.
   - Now you can follow the following docker-compose option, which can be run without customizing the domain.

### Docker Compose
- From the root directory:
1. **Download the Script**  
   Download the `install_docker_compose.sh` script from the provided location.
2. **Make the Script Executable**  
   Open a terminal, navigate to the directory containing the script, and run:  
   `chmod +x install_docker_compose.sh`
3. **Execute the Script**  
   Run the script with:  
   ```bash
   ./install_docker_compose.sh

## Configuration .env file structure:
- this file should be placed in folder raifbot
- Please replace *<YOUR_VALUE>* with your actual values.

### Backend
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
PINECONE_API_KEY=<YOUR_PINECONE_API_KEY>
PINECONE_ENV=<YOUR_PINECONE_ENVIRONMENT>
INDEX_NAME=<YOUR_INDEX_NAME>
EMBEDDING_NAME=<YOUR_EMBEDDING_NAME>
LLM_NAME=<YOUR_LLM_NAME>
MONGO_DB_KEY=<YOUR_MONGODB_CONNECTION_STRING>

### Frontend
PAGE_ICON=<PATH_TO_PAGE_ICON>
PAGE_TITLE=<YOUR_PAGE_TITLE>
RAIF_IMAGE_PATH=<PATH_TO_RAIF_IMAGE>
PROFILE_IMAGE_PATH=<PATH_TO_PROFILE_IMAGE>
AUTHOR_NAME=<YOUR_NAME>
AUTHOR_EMAIL=<YOUR_EMAIL>
ENDPOINT=<YOUR_ENDPOINT>

## Testing
- tests are saved in folder tests
      1. we can run it in root:
         ```bash
         poetry run pytest tests
      2. after docker-compose up is executed, the tests for backend are run automatically as 
prerequsities for vuilding of backend (see entry.sh in backend folder) 

