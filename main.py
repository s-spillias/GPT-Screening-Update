import os
import pandas as pd
import traceback
import random
import sys
import time
from dotenv import load_dotenv
from config import load_config, get_ai_model_name
from data_processing import load_papers, load_screening_criteria, prepare_headers
from file_operations import get_last_processed_paper, save_results, update_html
from screening_logic import process_paper
from server import update_screening_progress
from ai_interaction import ask_ai_about_paper

load_dotenv()

def main(pilot_percentage=100, use_pilot=False):
    try:
        # Load configuration
        config = load_config()
        model_to_use = config['model_to_use']
        n_agents = config['n_agents']
        proj_location = config['proj_location']
        debug = config['debug']
        skip_criteria = config['skip_criteria']
        resume_from = config.get('resume_from', 0)  # Get resume point, default to 0
        
        print(f"Resuming from paper {resume_from}")
        print(f"Pilot percentage: {pilot_percentage}%")
        print(f"Using pilot mode: {use_pilot}")
        
        # Load papers
        excel_sheet = "all_1400.xlsx"
        screen_name = 'screening_results'
        
        # Read papers and prepare data
        papers, title_column, abstract_column, n_studies = load_papers(excel_sheet, debug)
        screening_criteria = load_screening_criteria()
        
        # Setup headers
        headers = prepare_headers(n_agents, screening_criteria)
        
        # Setup output directory
        new_proj_location = os.path.join('AI_Output', model_to_use)
        os.makedirs(new_proj_location, exist_ok=True)
        out_path = new_proj_location
        os.makedirs(out_path, exist_ok=True)
        
        # Prepare data
        info = papers[[title_column, abstract_column]]
        info = info[:n_studies]
        print(f'\nTotal papers: {len(info)}')
        
        # Calculate number of papers for pilot screening
        n_pilot_papers = int(len(info) * (pilot_percentage / 100))
        pilot_papers = info.sample(n=n_pilot_papers) if pilot_percentage < 100 else info
        pilot_papers = pilot_papers.reset_index(drop=True)  # Reset index for pilot papers
        print(f'Assessing {len(pilot_papers)} papers for {"pilot" if use_pilot else "full"} screening ({pilot_percentage}%)')
        
        info_all = [pilot_papers.copy() for _ in range(n_agents)]
        summary_decisions = pd.DataFrame(index=pilot_papers.index)
        
        # Save initial headers only if starting fresh
        if resume_from == 0:
            print("Starting fresh screening - writing headers")
            from auxiliary import save_row
            summary_row = ["Paper Number", "Title", "Abstract", "Summary Decision"]
            save_row(f"{screen_name}_summary", summary_row, out_path)
            
            for agent in range(n_agents):
                save_row(str(agent), headers[agent], out_path)
        else:
            print("Resuming existing screening - skipping headers")
        
        # Process papers starting from resume point
        for index, row in pilot_papers.iterrows():
            try:
                print(f'\nProcessing Paper Number: {index} (Paper {index + 1} of {n_pilot_papers})')
                
                if use_pilot:
                    # In pilot mode, we'll wait for user input before processing each paper
                    user_decision = wait_for_user_decision(index, row[title_column], row[abstract_column], model_to_use)
                    summary_decision = user_decision
                else:
                    summary_decision = process_paper(
                        index, pilot_papers, title_column, abstract_column, n_agents, 
                        screening_criteria, info_all, get_ai_model_name(model_to_use), 
                        out_path, screen_name, skip_criteria, resume_from,
                        update_screening_progress,
                        n_pilot_papers
                    )
                
                summary_decisions.at[index, 'Accept'] = summary_decision
                
                # Update progress
                update_screening_progress(index, row[title_column], summary_decision)
                
            except Exception as e:
                print(f"Error processing paper {index}: {str(e)}")
                print(traceback.format_exc())
                summary_decisions.at[index, 'Accept'] = 'Error'
        
        # Update progress with completion status
        update_html(out_path, n_pilot_papers - 1, "Screening Complete", "Complete", update_screening_progress, n_pilot_papers)
        
        # Save final results
        save_results(summary_decisions, f"{screen_name}_summary", out_path)
        
    except Exception as e:
        print(f"An error occurred during the screening process: {str(e)}")
        print(traceback.format_exc())

def wait_for_user_decision(index, title, abstract, model_to_use):
    """
    This function waits for user input in pilot mode.
    It updates the screening progress and waits for a decision from the frontend.
    """
    print(f"Waiting for user decision on paper {index}:")
    print(f"Title: {title}")
    print(f"Abstract: {abstract}")
    
    # Get initial AI assessment
    ai_assessment = ask_ai_about_paper(title, abstract, model_to_use)
    
    # Update progress with AI assessment
    update_screening_progress(index, title, f"AI Assessment: {ai_assessment}")
    
    # In a real implementation, we would wait for input from the frontend
    # For now, we'll simulate waiting for user input
    decision = None
    while decision not in ['Include', 'Exclude']:
        try:
            decision = input("Enter decision (Include/Exclude): ").capitalize()
        except KeyboardInterrupt:
            print("\nScreening interrupted by user.")
            sys.exit(0)
    
    return decision

if __name__ == "__main__":
    if len(sys.argv) > 2:
        pilot_percentage = float(sys.argv[1])
        use_pilot = sys.argv[2].lower() == 'true'
    else:
        pilot_percentage = 100
        use_pilot = False
    main(pilot_percentage, use_pilot)
