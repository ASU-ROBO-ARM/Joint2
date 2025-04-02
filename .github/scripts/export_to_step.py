# Save this script to .github/scripts/export_to_step.py

import sys
import os
import win32com.client
import pythoncom

def export_to_step(inventor_file_path):
    try:
        # Initialize the COM objects
        pythoncom.CoInitialize()
        
        # Get the running instance of Inventor or create a new one
        try:
            inventor_app = win32com.client.GetActiveObject('Inventor.Application')
            print("Connected to running Inventor instance")
        except:
            inventor_app = win32com.client.Dispatch('Inventor.Application')
            inventor_app.Visible = False
            print("Started new Inventor instance")
        
        # Open the document
        document = inventor_app.Documents.Open(inventor_file_path)
        
        # Generate output path
        output_dir = os.path.dirname(inventor_file_path)
        base_name = os.path.splitext(os.path.basename(inventor_file_path))[0]
        step_file_path = os.path.join(output_dir, f"{base_name}.step")
        
        # Get the translator add-in
        translator_add_in = inventor_app.ApplicationAddIns.ItemById["{90AF7F40-0C01-11D5-8E83-0010B541CD80}"]
        
        # Set up the STEP translator options
        context = inventor_app.TransientObjects.CreateTranslationContext()
        options = inventor_app.TransientObjects.CreateNameValueMap()
        
        # Configure STEP export options
        if translator_add_in.HasSaveCopyAsOptions[document, context, options]:
            # Standard STEP AP214 configuration
            options.Value["ApplicationProtocolType"] = 3  # AP214 - automotive design
            options.Value["Author"] = "GitHub Action"
            options.Value["Organization"] = "Automated Export"
            
        # Execute the translation
        result = translator_add_in.SaveCopyAs(document, context, options, step_file_path)
        
        if result:
            print(f"Successfully exported to {step_file_path}")
        else:
            print(f"Failed to export {inventor_file_path}")
        
        # Close the document
        document.Close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Clean up COM objects
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python export_to_step.py <inventor_file_path>")
        sys.exit(1)
    
    inventor_file_path = os.path.abspath(sys.argv[1])
    if not os.path.exists(inventor_file_path):
        print(f"File not found: {inventor_file_path}")
        sys.exit(1)
    
    export_to_step(inventor_file_path)