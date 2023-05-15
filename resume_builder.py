import streamlit as st
import openai
import os
from langchain import PromptTemplate
from langchain.llms import OpenAI

openai.api_key = os.environ.get('OPENAI_API_KEY')

# Model

template = '''Emulate the writing style of the following resume bullet points:
{few_shot_examples}
=====
Write {bullet_points_n} resume bullet points that summarize the following experience: {exp_description}
====
Resume bullet points for the given experience:'''

prompt_template = PromptTemplate(
    input_variables=['exp_description', 'bullet_points_n', 'few_shot_examples'],
    template=template
)

call_llm = OpenAI()

# Streamlit app

st.set_page_config(page_title='Resume Builder')
st.header('Resume Builder')

st.markdown('Don\'t know where to start on writing your resume? Try this tool to get started!')

# with col2:
#     st.image(image=r'C:\Users\mnw47\coding projects\resume_builder\resume_example.jpeg', width=500)

col1, col2 = st.columns(2)

with col1:
    example_points_selector = st.selectbox(
        'Do you want to provide example resume points?',
        ('No', 'Yes')
    )

with col2:
    bullet_points_n = st.number_input(
        label='How many bullets points do you want?',
        min_value=1,
        max_value=8,
        value=3
    )

if example_points_selector == 'Yes':
    example_points = st.text_area(label='Example resume points')

exp_description = st.text_area(label='Experience description', placeholder='Description of experience to resumize ')

run_button = st.button(label='Generate resume points!')

if run_button:
    if example_points_selector == 'No':
        few_shot_examples = f'''- Automated video review: ~$2M annual cost savings from deprecating manual safety review; Productionized a model that automatically hides videos with high content risk based on machine learning signals, leading a cross-functional team across product, engineering, and operations
        - Idea pin (new content format) safety: met OKR by reducing unsafe content on Pinterest by 10x; Conducted metric investigations and model performance analyses as the official metrics owner of idea pin safety, sizing opportunities and problems as well as fixing critical bugs
        - Fake following: identified 1% of user follows as bots to degame monetized engagement; Productionized a model that detected anomalous coordinated behavior among clusters of users using handcrafted features in SQL and Python
        - Launching spam rules: owned analysis to production end-to-end; Disabled ~300K policy violating users by shipping rules into production through events-based analyses of 100M+ events per day and hundreds of features
        - Payment network anticompetition defense: damages estimated at $1+B; Led a team of ten analysts to prove competition among the largest US payment cards firms, owning the accuracy of a ~200 page expert report
        - Department of Justice approval of health insurance merger: ~$50B valuation; Proved that the US health insurance industry would remain competitive post-merger of two Fortune 500 companies by analyzing win-loss Salesforce data using SQL and R
        '''
    if example_points_selector == 'Yes':
        few_shot_examples = example_points

    prompt = prompt_template.format(
        exp_description=exp_description,
        bullet_points_n=bullet_points_n,
        few_shot_examples=few_shot_examples)
    resume_points = call_llm(prompt)

    st.markdown('#### Your resume bullet points')
    st.write(resume_points)