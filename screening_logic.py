from ai_interaction import get_data
from file_operations import save_results, update_html

def process_paper(paper_num, info, title_column, abstract_column, n_agents, screening_criteria, info_all, model_to_use, out_path, screen_name, skip_criteria, resume_from, update_screening_progress, n_studies):
    try:
        title = info[title_column].values[paper_num]
        abstract = info[abstract_column].values[paper_num]
    except Exception as e:
        print(f"Error accessing paper information: {str(e)}")
        return 'Error'

    if "No Abstract" in abstract or abstract == "":
        print("Skipping paper - no abstract")
        summary_decision = 'Maybe'
        update_html(out_path, paper_num, title, summary_decision, update_screening_progress, n_studies)
        return summary_decision

    content = f"Title: {title}\n\nAbstract: {abstract}"
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(content)

    save_stuff = {}
    summary_decision = 'Maybe'  # Default to 'Maybe' if no decision is made
    decision_numeric = {'Yes': 2, 'No': 0, 'Maybe': 1}

    # Process screening criteria
    for SC_num, Criterion in enumerate(screening_criteria, 1):
        print(f"\nProcessing Screening Criterion {SC_num}: {Criterion['type']}")
        try:
            assessments, initial_decisions, final_decisions = get_data(
                Criterion, content, n_agents, SC_num, info_all, paper_num, model_to_use,
                title, abstract
            )
        except Exception as e:
            print(f"Error in get_data for criterion {Criterion['type']}: {str(e)}")
            assessments = initial_decisions = final_decisions = ['Error'] * n_agents

        for lst in [assessments, initial_decisions, final_decisions]:
            while len(lst) < n_agents:
                lst.append("NOT RUN")

        save_stuff[Criterion['type']] = {
            "Initial": initial_decisions,
            "Final": final_decisions,
            "Assessment": assessments
        }

        print("\nInitial Decisions:", initial_decisions)
        print("Final Decisions:", final_decisions)

        converted_decisions = [
            decision_numeric.get(element, element) 
            for element in (initial_decisions + final_decisions)
        ]
        converted_decisions = [
            element for element in converted_decisions 
            if isinstance(element, int)
        ]

        if converted_decisions and sum(converted_decisions) == 0:
            print(f"Rejected at SC: {SC_num}")
            summary_decision = 'No'
            if skip_criteria:
                break
        elif all(decision == 'Yes' for decision in final_decisions):
            summary_decision = 'Yes'

    # Save results
    try:
        save_results(screen_name, out_path, paper_num, title, abstract, summary_decision, resume_from, n_agents, info_all, save_stuff, screening_criteria)
    except Exception as e:
        print(f"Error saving results: {str(e)}")

    # Update HTML and screening progress
    try:
        update_html(out_path, paper_num, title, summary_decision, update_screening_progress, n_studies)
    except Exception as e:
        print(f"Error updating HTML: {str(e)}")

    print(f"Completed processing paper {paper_num}")
    return summary_decision
