"""
Script to create an HTML dashboard combining all interactive plots.
Organized for Vercel deployment.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Optional
import json
from datetime import datetime
import shutil
import sys
from src.visualisation.interactive import save_interactive_plots

def create_dashboard_html(
    plots_dir: Path,
    output_file: Path,
    title: str = "Australian Health & Dietary Trends Analysis"
) -> None:
    """
    Create an HTML dashboard combining all interactive plots.
    
    Args:
        plots_dir: Directory containing the interactive plot HTML files
        output_file: Path to save the dashboard HTML
        title: Dashboard title
    """
    # HTML template with relative paths for Vercel
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            .header {{
                background-color: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .section {{
                background-color: white;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .plot-container {{
                width: 100%;
                height: 600px;
                margin-bottom: 20px;
            }}
            h1, h2 {{
                color: #333;
                margin-top: 0;
            }}
            .timestamp {{
                color: #666;
                font-size: 0.9em;
                margin-top: 10px;
            }}
            .description {{
                margin: 20px 0;
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{title}</h1>
                <p class="timestamp">Generated on: {datetime.now().strftime('%d %B %Y %H:%M:%S')}</p>
                <div class="description">
                    <p>This dashboard presents an analysis of Australian dietary patterns and health outcomes, focusing on the relationship between seed oil consumption (particularly linoleic acid) and various health metrics from 1980 to present.</p>
                    <p>The analysis combines data from multiple authoritative sources including FAOSTAT, NCD-RisC, IHME GBD, and the Australian Bureau of Statistics.</p>
                </div>
            </div>
            
            <div class="section">
                <h2>Time Series Analysis</h2>
                <div class="plot-container">
                    <iframe src="./plots/health_metrics_time_series.html" width="100%" height="100%" frameborder="0"></iframe>
                </div>
                <div class="plot-container">
                    <iframe src="./plots/dietary_metrics_time_series.html" width="100%" height="100%" frameborder="0"></iframe>
                </div>
            </div>
            
            <div class="section">
                <h2>Correlation Analysis</h2>
                <div class="plot-container">
                    <iframe src="./plots/correlation_heatmap.html" width="100%" height="100%" frameborder="0"></iframe>
                </div>
            </div>
            
            <div class="section">
                <h2>Key Relationships</h2>
                {generate_scatter_iframes(plots_dir)}
            </div>
            
            <div class="section">
                <h2>Model Results</h2>
                {generate_model_iframes(plots_dir)}
            </div>
            
            <div class="section">
                <h2>GAM Analysis</h2>
                {generate_gam_iframes(plots_dir)}
            </div>
        </div>
    </body>
    </html>
    """
    
    output_file.write_text(html_template)

def generate_scatter_iframes(plots_dir: Path) -> str:
    """Generate iframe HTML for scatter plots."""
    iframes = []
    for plot_file in plots_dir.glob("scatter_*.html"):
        iframes.append(f'''
        <div class="plot-container">
            <iframe src="./plots/{plot_file.name}" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        ''')
    return "\n".join(iframes)

def generate_model_iframes(plots_dir: Path) -> str:
    """Generate iframe HTML for model result plots."""
    iframes = []
    for plot_name in ["feature_importance.html", "model_comparison.html"]:
        if (plots_dir / plot_name).exists():
            iframes.append(f'''
            <div class="plot-container">
                <iframe src="./plots/{plot_name}" width="100%" height="100%" frameborder="0"></iframe>
            </div>
            ''')
    return "\n".join(iframes)

def generate_gam_iframes(plots_dir: Path) -> str:
    """Generate iframe HTML for GAM plots."""
    iframes = []
    for plot_file in plots_dir.glob("gam_pdp_*.html"):
        iframes.append(f'''
        <div class="plot-container">
            <iframe src="./plots/{plot_file.name}" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        ''')
    return "\n".join(iframes)

def organize_for_vercel(base_dir: Path) -> None:
    """
    Organize files for Vercel deployment.
    
    Args:
        base_dir: Project root directory
    """
    # Create deployment directory structure
    deploy_dir = base_dir / "public"
    plots_dir = deploy_dir / "plots"
    deploy_dir.mkdir(exist_ok=True)
    plots_dir.mkdir(exist_ok=True)
    
    # Copy all plot files to the plots directory
    source_plots_dir = base_dir / "figures" / "interactive"
    if source_plots_dir.exists():
        for plot_file in source_plots_dir.glob("*.html"):
            shutil.copy2(plot_file, plots_dir)
    
    # Copy dashboard to public directory
    dashboard_file = base_dir / "figures" / "dashboard.html"
    if dashboard_file.exists():
        shutil.copy2(dashboard_file, deploy_dir / "index.html")

def main():
    """Main function to create the dashboard and organize for Vercel."""
    # Define paths
    base_dir = Path(__file__).parent.parent.parent
    plots_dir = base_dir / "figures" / "interactive"
    output_file = base_dir / "figures" / "dashboard.html"
    
    # Load the analytical dataset
    df = pd.read_csv(base_dir / "data" / "processed" / "analytical_data_australia_final.csv")
    
    # Load model results if available
    model_results = None
    results_file = base_dir / "reports" / "model_results.json"
    if results_file.exists():
        with open(results_file, 'r') as f:
            model_results = json.load(f)
    
    # Create interactive plots
    save_interactive_plots(df, plots_dir, model_results)
    
    # Create dashboard
    create_dashboard_html(plots_dir, output_file)
    print(f"Dashboard created successfully at {output_file}")
    
    # Organize files for Vercel deployment
    organize_for_vercel(base_dir)
    print("Files organized for Vercel deployment in the 'public' directory")

if __name__ == "__main__":
    # Add the project root directory to Python path to allow absolute imports
    project_root = str(Path(__file__).parent.parent.parent)
    if project_root not in sys.path:
        sys.path.append(project_root)
    main() 