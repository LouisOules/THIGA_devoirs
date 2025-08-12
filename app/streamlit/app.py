import streamlit as st
import requests
import json

st.title("AI agent for SaaS")

##Initialize output
if "emails_output" not in st.session_state:
    st.session_state.emails_output = ""
if "user_story_output" not in st.session_state:
    st.session_state.user_story_output = ""

##Prioritazation frameworks
prioritization_framework = st.selectbox(
    "Would you like to apply a specific prioritization frameworks?",
    ("no", "MoSCoW", "RICE"),
)

##Process emails
email_system_prompt = """You are an intelligent assistant for an SaaS startup that develops a project management platform. Your purpose is to help the product owner to process client feedback, feature requests and bug reports you receive via email."""

email_processing_prompt = """I am going to forward you some emails I received from our clients. In these emails they can write some feedback, request new features or report bugs. I want you to find the most important tasks to be carried out to tackle the issues mentioned in the emails. For each of these issues, I want you to give them a score between 1 and 10. 10 being the most urgent to tackle and 1 the less urgent. Rank them form highest to lowest score. You should score them based on how often you see them across the different emails, and on how crucial they seem. Here are the emails in between triple ticks:
```"""

email_index_input = st.text_input("Select the emails index you want to process")
if st.button("Process emails"):
	if email_index_input:
		#Figure out which mails to take into consideration
		with open("emails.json") as emails_json_file:
			client_emails = json.load(emails_json_file)
		emails_amount = len(list(client_emails.keys()))
		email_index_input=email_index_input.replace(" ", "")
		if email_index_input=='all':
			emails_index = range(1, emails_amount+1)
		else:
			try:
				index_list = email_index_input.split(",")
				for elt in index_list:
					if int(elt)<1 or int(elt)>emails_amount:
						raise Exception("number out of range")						
			except:
				e = ValueError("Please enter a valid selection of emails index, or 'all'.")
				st.exception(e)
				exit()
			emails_index = index_list
				
		for number in emails_index:
			key = f"email_{number}"
			email_processing_prompt += f"\nEmail {number}:\n{client_emails[key]}"
		if prioritization_framework in 'MoSCoWRICE':
			email_processing_prompt += f"\n```\n Please apply the {prioritization_framework} prioritization framework."
		else:
			email_processing_prompt += "\n```\n Now please generate the information I need."
		
		#Querry the LLM
		response = requests.post(
		"http://ollama:11434/api/chat",
		json={"model": "mistral", 
		"messages": [
		{
		"role": "system",
		"content": email_system_prompt
		},
		{
		"role": "user",
		"content": email_processing_prompt
		}
		]
		},
		stream=False
		)

		#Read the AI's response
		all_text = ""
		for line in response.text.strip().split("\n"):
			if line.strip():
				try:
					obj = json.loads(line)
					content = obj.get("message", {}).get("content", "")
					all_text += content
				except json.JSONDecodeError:
					st.error(f"Could not decode line: {line}")

		st.session_state.emails_output = all_text

#Save the AI's response	
if st.session_state.emails_output:
	st.subheader("Selection of tasks to be carried out:")
	st.write(st.session_state.emails_output)

##Create User Story
user_story_system_prompt = """You are an intelligent assistant for an SaaS startup that develops a project management platform. Your purpose is to help the product owner to process client feedback, feature requests and bug reports by creating appropriate User Stories."""

user_story_processing_prompt = ""
user_story_processing_prompt_1 = """Here is some context on a User Story to be created for my team, in between triple ticks: 
```"""
user_story_processing_prompt_2 = """
```
Now please generate a User Story, according to JIRA standards. In that Story I want you to propose relevant acceptance criteria, to perform a complexity estimation as well as an estimation of the relative development complexity. Please proceed.
"""

user_story_input = st.text_input("Please fill in some context on the user story to be created")
if st.button("Generate User Story"):
	if user_story_input:
		user_story_processing_prompt += user_story_processing_prompt_1 + user_story_input + user_story_processing_prompt_2
		#Querry the LLM
		response = requests.post(
		"http://ollama:11434/api/chat",
		json={"model": "mistral", 
		"messages": [
		{
		"role": "system",
		"content": user_story_system_prompt
		},
		{
		"role": "user",
		"content": user_story_processing_prompt
		}
		]
		},
		stream=False
		)

		#Read the AI's response
		all_text = ""
		for line in response.text.strip().split("\n"):
			if line.strip():
				try:
					obj = json.loads(line)
					content = obj.get("message", {}).get("content", "")
					all_text += content
				except json.JSONDecodeError:
					st.error(f"Could not decode line: {line}")

		st.session_state.user_story_output = all_text

#Save the AI's response	
if st.session_state.user_story_output:
	st.subheader("Generated User Story:")
	st.write(st.session_state.user_story_output)