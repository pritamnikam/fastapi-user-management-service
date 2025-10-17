"""Streamlit Admin Portal for Prompt Management"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import select, update, desc

# Add the parent directory to sys.path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent))

# Now we can import using the app prefix
from app.db.schema import SessionLocal, Prompt
from app.models.prompt import PromptCreate, PromptRead

def main():
    """Main Streamlit application"""
    st.set_page_config(page_title="Prompt Catalog Admin", layout="wide")
    st.title("Prompt Catalog Admin Portal")
    
    # Initialize session state for storing selected values
    if 'selected_app_id' not in st.session_state:
        st.session_state.selected_app_id = None
    if 'selected_prompt' not in st.session_state:
        st.session_state.selected_prompt = None
    
    # Database connection
    db = SessionLocal()
    
    try:
        # 1. Application Selector
        st.header("1. Application Selector")
        
        # Get unique app_ids from the database
        app_ids_query = select(Prompt.app_id).distinct()
        app_ids = [row[0] for row in db.execute(app_ids_query).all()]
        
        # If no app_ids found, provide some defaults
        if not app_ids:
            app_ids = ["app1", "app2", "app3"]
        
        selected_app = st.selectbox(
            "Select Application",
            options=app_ids,
            key="app_selector"
        )
        st.session_state.selected_app_id = selected_app
        
        if st.session_state.selected_app_id:
            # 2. Prompt List
            st.header("2. Prompt List")
            
            # Query prompts for the selected application
            prompts_query = select(Prompt).where(Prompt.app_id == st.session_state.selected_app_id).order_by(Prompt.prompt_key, Prompt.version.desc())
            prompts = db.execute(prompts_query).scalars().all()
            
            if prompts:
                # Create a DataFrame for display
                prompt_data = []
                for prompt in prompts:
                    prompt_data.append({
                        "id": prompt.id,
                        "prompt_key": prompt.prompt_key,
                        "version": prompt.version,
                        "is_active": prompt.is_active,
                        "created_by": prompt.created_by,
                        "created_at": prompt.created_at
                    })
                
                df = pd.DataFrame(prompt_data)
                st.dataframe(df)
                
                # Select a prompt to edit
                selected_prompt_key = st.selectbox(
                    "Select Prompt to Edit",
                    options=list(set([p["prompt_key"] for p in prompt_data])),
                    key="prompt_selector"
                )
                
                if selected_prompt_key:
                    # Get all versions of this prompt
                    versions = [p for p in prompt_data if p["prompt_key"] == selected_prompt_key]
                    versions_df = pd.DataFrame(versions)
                    st.dataframe(versions_df)
                    
                    # Get the active version
                    active_version = next((p for p in prompts 
                                         if p.prompt_key == selected_prompt_key and p.is_active), None)
                    
                    if active_version:
                        st.session_state.selected_prompt = active_version
                    
                    if st.session_state.selected_prompt:
                        # 3. Prompt Editor
                        st.header("3. Prompt Editor")
                        
                        prompt_text = st.text_area(
                            "Edit Prompt Text",
                            value=st.session_state.selected_prompt.prompt_text,
                            height=300
                        )
                        
                        username = st.text_input("Your Username", value="admin")
                        
                        if st.button("Save New Version"):
                            # Create a new version of the prompt
                            try:
                                # 1. Set is_active=False for all previous versions
                                deactivate_stmt = update(Prompt).where(
                                    (Prompt.app_id == st.session_state.selected_app_id) & 
                                    (Prompt.prompt_key == selected_prompt_key)
                                ).values(is_active=False)
                                db.execute(deactivate_stmt)
                                
                                # 2. Get the latest version number
                                latest_version = db.execute(
                                    select(Prompt.version)
                                    .where(
                                        (Prompt.app_id == st.session_state.selected_app_id) & 
                                        (Prompt.prompt_key == selected_prompt_key)
                                    )
                                    .order_by(Prompt.version.desc())
                                    .limit(1)
                                ).scalar_one_or_none() or 0
                                
                                # 3. Create a new version with is_active=True
                                new_prompt = Prompt(
                                    app_id=st.session_state.selected_app_id,
                                    prompt_key=selected_prompt_key,
                                    prompt_text=prompt_text,
                                    version=latest_version + 1,
                                    is_active=True,
                                    created_by=username
                                )
                                db.add(new_prompt)
                                db.commit()
                                st.success(f"New version {latest_version + 1} created successfully!")
                                
                                # Refresh the page
                                st.experimental_rerun()
                            except Exception as e:
                                db.rollback()
                                st.error(f"Error creating new version: {e}")
                        
                        # 4. History & Rollback
                        st.header("4. History & Rollback")
                        
                        # Query all versions of this prompt
                        history_query = select(Prompt).where(
                            (Prompt.app_id == st.session_state.selected_app_id) & 
                            (Prompt.prompt_key == selected_prompt_key)
                        ).order_by(Prompt.version.desc())
                        
                        history_prompts = db.execute(history_query).scalars().all()
                        
                        history_data = [{
                            "id": p.id,
                            "version": p.version,
                            "is_active": p.is_active,
                            "created_by": p.created_by,
                            "created_at": p.created_at
                        } for p in history_prompts]
                        
                        history_df = pd.DataFrame(history_data)
                        st.dataframe(history_df)
                        
                        # Rollback functionality
                        if len(history_data) > 1:  # Only show rollback if there are multiple versions
                            rollback_version = st.selectbox(
                                "Select a version to rollback:",
                                options=[p["version"] for p in history_data if not p["is_active"]],
                                format_func=lambda x: f"Version {x}"
                            )
                            
                            if st.button("Set as Active Version"):
                                try:
                                    # 1. Set is_active=False for all versions
                                    deactivate_stmt = update(Prompt).where(
                                        (Prompt.app_id == st.session_state.selected_app_id) & 
                                        (Prompt.prompt_key == selected_prompt_key)
                                    ).values(is_active=False)
                                    db.execute(deactivate_stmt)
                                    
                                    # 2. Set is_active=True for the selected version
                                    activate_stmt = update(Prompt).where(
                                        (Prompt.app_id == st.session_state.selected_app_id) & 
                                        (Prompt.prompt_key == selected_prompt_key) &
                                        (Prompt.version == rollback_version)
                                    ).values(is_active=True)
                                    db.execute(activate_stmt)
                                    
                                    db.commit()
                                    st.success(f"Version {rollback_version} set as active!")
                                    
                                    # Refresh the page
                                    st.experimental_rerun()
                                except Exception as e:
                                    db.rollback()
                                    st.error(f"Error setting active version: {e}")
                        else:
                            st.info("Only one version exists. Create more versions to enable rollback.")
            else:
                st.info("No prompts found for the selected application.")
    finally:
        db.close()

if __name__ == "__main__":
    main()