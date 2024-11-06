import re
from ask_AI import ask_ai

def add_criteria(Criterion):
    base_prompt = ("You are a reviewer for a research project and have been asked to assess whether the "
                  "given paper Title and Abstract meets the following Screening Criteria (SC)."
                  " In assessing, do not re-interpret the SC, simply assess the SC at face value.\n"
                  "We are only interested in papers that strictly meet the SC.\n"
                  "If not enough information is available, be inclusive as we can follow-up at a later stage.")
    
    base_prompt += '\n\n' + f'SC: {Criterion["type"]}'
    base_prompt += f'\nIncluded: {Criterion["included"]}'
    base_prompt += f'\nExcluded: {Criterion["excluded"]}'
    base_prompt += ('\n\n' + "Task: Given the following Title and Abstract, respond"
                   " to the Screening Criteria (SC) with the following elements, "
                   "Initial Response, Reflection on Initial Response, and Final Response."
                   " Here is an example of how your response should look:\n"
                   "Format: \n"
                   "SC -\n"
                   "Initial Response: Only respond with a Yes or No; Short explanation as rationale.\n"
                   "Reflection: Is the Initial Response correct? Be concise.\n"
                   "Final Response: Strictly only respond with a Yes or No; Short explanation based on reflection. "
                   "\nInitial Response and Final Response should consist of "
                   "only a Yes or No or Maybe "
                   "followed by a semicolon and a single sentence explanation for your reasoning. Like this: "
                   "\nSC: Final Response; One sentence of reasoning.")
    return base_prompt

def get_ai_assessment(Criterion, content, ai_model):
    prompt = add_criteria(Criterion) + "\n\n" + content + '\n\n'
    try:
        assessment = ask_ai(prompt, ai_model)
    except Exception as e:
        print(f"Error calling AI: {str(e)}")
        assessment = "No Data"
    
    print("\n**** Response ****\n")
    print(assessment)
    
    pattern = r'\b(Yes|No|Maybe)\b'
    matches = re.findall(pattern, assessment)
    
    try:
        final_decision = matches[-1]
        initial_decision = matches[0]
        thoughts = assessment
    except:
        print("Bad Parsing...")
        final_decision = initial_decision = "No Data"
        thoughts = assessment
    
    return assessment, initial_decision, final_decision, thoughts

def get_data(Criterion, content, n_agents, SC_num, info_all, paper_num, ai_model, title, abstract):
    assessments = []
    initial_decisions = []
    final_decisions = []
    decided = False
    
    for agent in range(0, n_agents):
        print(f"Agent {agent}")
        if decided:
            continue
        
        assessment, initial_decision, final_decision, thoughts = get_ai_assessment(Criterion, content, ai_model)
        
        assessments.append(assessment)
        initial_decisions.append(initial_decision)
        final_decisions.append(final_decision)
        
        col_decision = f"Final Decision - SC{SC_num}: {Criterion['type']}"
        col_initial = f"Initial Decision - SC{SC_num}: {Criterion['type']}"
        col_thoughts = f"Thoughts - SC{SC_num}: {Criterion['type']}"
        
        info_all[agent].loc[paper_num, ['Paper Number', "Title", "Abstract"]] = [paper_num, title, abstract] if title and abstract else 'NO DATA'
        info_all[agent].loc[paper_num, col_decision] = final_decision 
        info_all[agent].loc[paper_num, col_initial] = initial_decision 
        info_all[agent].loc[paper_num, col_thoughts] = thoughts 
        
        if not "No" in initial_decision[:6] and not "No" in final_decision:
            decided = True
    
    return assessments, initial_decisions, final_decisions
