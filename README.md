# Approach

Given that we are going to process text and to get text as an output, it seems quite natural to run Large Language Models (LLM) to deal with this challenge.

Since we are processing data coming from clients, we do not want the data to get lost in the open. Therefore I chose to run the Large Language Models with Ollama, locally. This also means every call to the LLM will be free.

To simulate the data from the clients, I decided to let chatGPT write 20 emails coming from the customers of the SaaS startup, already gathered in a json file.
> Prompt:
Please invent 20 emails that a SaaS startup that develops a project management platform might receive from their clients. Keep them short. In these emails I want to see feedback, new features requests and bug reports. Make it so that a few of these are recurrent across several of the 20 emails. Put these emails into a json file. Start with "email_1" refering to the text of the first email.

For the LLM I chose Mistral, because they offer a 7b model that is made easy to download by Ollama. 7b also means it can run decently fast on my personnal computer. Not to mention it is a French model, cocorico!

To be one step closer to a Hands-On delivery, I decided to run my app in a Docker container. Ollama runs in a second Docker container. This also remove the need to install too many third-parties software on my personnal computer (e.g. Python & Ollama are installed in the containers, not on my machine).

I programmed the app in Python, because of the many libraries it offers and the ease of impletentation compared to other programming languages.

For the frontend I decided to go for streamlit, a Python library I have some experience with, and will suit the needs of this tiny project very well.

# How to run it

To run this app, you basically just need to install Docker Desktop. Once you have that software, open a terminal from it, go to the /app folder of this repo, and run ```docker-compose up --build```.
> The first time you build it, you will have to go manually to the ollama container to pull Mistral manually from there. That can probably be done automatically in the Containerfile, but I encountered too many errors while trying and wanted to move forward.
Run ```docker exec -it ollama sh``` then ```ollama pull mistral```

Once this is done, open a web browser and go to http://localhost:8501

# Tests

As I am already a bit more than 3 hours in, I decided not to bother too much with proper testing.

# A few idea of improvements
* The data could be stored in a SQL or PostgreSQL database. This database could be linked with the actual mailbox of the PO.
* Being able to select mails with keywords (for instance all mail coming from a important client X).
* In the docker-compose.yml file, I added a gpu resource. I did not checked if the LLM is actually running on my gpu or not, would be nice to make sure it is.
* Make the installation of mistral automated in the ollama Containerfile.
* The prompts for the LLM could be stored in a cleaner way (here they are directly embedded in the python script), and we could do proper prompt templating with langchain.
* Would be nice to be able to save the outputs we generate in text files.