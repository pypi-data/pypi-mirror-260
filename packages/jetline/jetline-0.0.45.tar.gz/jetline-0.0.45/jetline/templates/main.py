import sys
from jetline.pipeline.pipeline import PipelineManager


def run_pipelines():
    """Lädt und führt Pipelines aus den Unterordnern aus."""
    try:
        
        pipeline_manager = PipelineManager()
        PIPELINE_ORDER = ["example_pipeline"]
        pipeline_manager.run(PIPELINE_ORDER)

    except Exception as e:
        print(f"Fehler beim Ausführen der Pipelines: {e}")
        sys.exit(1)

if __name__ == "__main__":
    
    run_pipelines()
