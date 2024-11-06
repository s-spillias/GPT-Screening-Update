import os
import pandas as pd
import traceback
from dotenv import load_dotenv
from config import load_config, get_ai_model_name
from data_processing import load_papers, load_screening_criteria, prepare_headers
from file_operations import get_last_processed_paper, save_results, update_html
from screening_logic import process_paper
from server import update_screening_progress

load_dotenv()

def main():
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
        print(f'\nAssessing {len(info)} Papers')
        
        info_all = [info.copy() for _ in range(n_agents)]
        summary_decisions = info
        
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
        for paper_num in range(resume_from, len(info)):
            try:
                print(f'\nProcessing Paper Number: {paper_num}')
                
                summary_decision = process_paper(
                    paper_num, info, title_column, abstract_column, n_agents, 
                    screening_criteria, info_all, get_ai_model_name(model_to_use), 
                    out_path, screen_name, skip_criteria, resume_from,
                    update_screening_progress,  # Pass this function to process_paper
                    n_studies  # Pass n_studies to process_paper
                )
                
                summary_decisions.at[paper_num, 'Accept'] = summary_decision
            except Exception as e:
                print(f"Error processing paper {paper_num}: {str(e)}")
                print(traceback.format_exc())
                summary_decisions.at[paper_num, 'Accept'] = 'Error'
        
        # Update progress with completion status
        update_html(out_path, n_studies - 1, "Screening Complete", "Complete", update_screening_progress, n_studies)
        
    except Exception as e:
        print(f"An error occurred during the screening process: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
