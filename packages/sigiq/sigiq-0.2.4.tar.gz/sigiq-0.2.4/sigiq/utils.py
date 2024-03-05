import sys

def check_import_order():
    # package list that should be imported after monkey_patch
    required_after_imports = [
        'openai', 
        'llama_index', 
        'langchain'
    ]  
    
    for imported_module in sys.modules:
        if imported_module in required_after_imports:
            raise ImportError(f"Import order error: '{imported_module}' must be imported after 'sigiq'")


def monkey_patch_openai():
    import openai
    
    from .classes import OpenAI
    
    openai.OpenAI = OpenAI