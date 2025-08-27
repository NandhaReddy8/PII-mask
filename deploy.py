#!/usr/bin/env python3
"""
Deployment script for PII Detection and Redaction Tool
Automates setup, testing, and validation of the tool
"""

import os
import sys
import subprocess
import shutil
import tempfile
import json
from pathlib import Path


class PIIDeployment:
    """Deployment manager for PII Detection Tool"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.requirements_file = self.project_root / "requirements.txt"
        self.main_script = self.project_root / "detector_varikuti_Narendra_Reddy.py"
        self.test_script = self.project_root / "tests" / "test_detector.py"
        self.sample_input = self.project_root / "examples" / "sample_input.csv"
        
    def print_step(self, step_name, description=""):
        """Print a formatted step header"""
        print(f"\n{'='*60}")
        print(f"🔧 {step_name}")
        if description:
            print(f"   {description}")
        print(f"{'='*60}")
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        self.print_step("Checking Python Version")
        
        version = sys.version_info
        print(f"Python version: {version.major}.{version.minor}.{version.micro}")
        
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            print("❌ Python 3.7 or higher is required!")
            return False
        
        print("✅ Python version is compatible")
        return True
    
    def create_virtual_environment(self):
        """Create a virtual environment"""
        self.print_step("Creating Virtual Environment")
        
        if self.venv_path.exists():
            print("Virtual environment already exists. Skipping creation.")
            return True
        
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], 
                         check=True, capture_output=True, text=True)
            print("✅ Virtual environment created successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    
    def get_venv_python(self):
        """Get the Python executable path for the virtual environment"""
        if os.name == 'nt':  # Windows
            return self.venv_path / "Scripts" / "python.exe"
        else:  # Unix/Linux/macOS
            return self.venv_path / "bin" / "python"
    
    def get_venv_pip(self):
        """Get the pip executable path for the virtual environment"""
        if os.name == 'nt':  # Windows
            return self.venv_path / "Scripts" / "pip.exe"
        else:  # Unix/Linux/macOS
            return self.venv_path / "bin" / "pip"
    
    def install_dependencies(self):
        """Install required dependencies"""
        self.print_step("Installing Dependencies")
        
        pip_path = self.get_venv_pip()
        
        try:
            # Install requirements (skip pip upgrade to avoid issues)
            subprocess.run([str(pip_path), "install", "-r", str(self.requirements_file)], 
                         check=True, capture_output=True, text=True)
            
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("Note: This tool uses only built-in Python modules, so dependencies are optional.")
            return True  # Continue anyway since we only use built-in modules
    
    def run_tests(self):
        """Run the test suite"""
        self.print_step("Running Tests")
        
        python_path = self.get_venv_python()
        test_path = self.test_script
        
        if not test_path.exists():
            print("❌ Test file not found!")
            return False
        
        try:
            result = subprocess.run([str(python_path), str(test_path)], 
                                  check=True, capture_output=True, text=True)
            print("✅ All tests passed!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            print(f"Test output: {e.stdout}")
            print(f"Test errors: {e.stderr}")
            return False
    
    def test_sample_data(self):
        """Test the tool with sample data"""
        self.print_step("Testing with Sample Data")
        
        python_path = self.get_venv_python()
        main_script = self.main_script
        sample_input = self.sample_input
        
        if not sample_input.exists():
            print("❌ Sample input file not found!")
            return False
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_output = f.name
        
        try:
            # Run the tool
            result = subprocess.run([
                str(python_path), str(main_script), 
                str(sample_input), "-o", temp_output
            ], check=True, capture_output=True, text=True)
            
            # Check if output file was created
            if os.path.exists(temp_output):
                print("✅ Sample data processed successfully")
                
                # Read and display sample output
                with open(temp_output, 'r') as f:
                    lines = f.readlines()
                    print(f"   Processed {len(lines)-1} records")
                
                # Clean up
                os.unlink(temp_output)
                return True
            else:
                print("❌ Output file was not created")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to process sample data: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def create_directories(self):
        """Create necessary directories"""
        self.print_step("Creating Project Directories")
        
        directories = [
            "examples",
            "tests", 
            "docs",
            "output"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(exist_ok=True)
            print(f"✅ Created directory: {directory}")
        
        return True
    
    def validate_project_structure(self):
        """Validate that all required files exist"""
        self.print_step("Validating Project Structure")
        
        required_files = [
            "detector_varikuti_Narendra_Reddy.py",
            "requirements.txt",
            "README.md",
            "LICENSE",
            ".gitignore"
        ]
        
        missing_files = []
        for file_name in required_files:
            file_path = self.project_root / file_name
            if not file_path.exists():
                missing_files.append(file_name)
            else:
                print(f"✅ Found: {file_name}")
        
        if missing_files:
            print(f"❌ Missing files: {', '.join(missing_files)}")
            return False
        
        return True
    
    def generate_usage_examples(self):
        """Generate usage examples and documentation"""
        self.print_step("Generating Usage Examples")
        
        examples = {
            "basic_usage": "python detector_varikuti_Narendra_Reddy.py input.csv",
            "custom_output": "python detector_varikuti_Narendra_Reddy.py input.csv -o output.csv",
            "sample_data": "python detector_varikuti_Narendra_Reddy.py examples/sample_input.csv",
            "run_tests": "python tests/test_detector.py"
        }
        
        print("📋 Usage Examples:")
        for name, command in examples.items():
            print(f"   {name}: {command}")
        
        return True
    
    def deployment_summary(self):
        """Display deployment summary"""
        self.print_step("Deployment Summary")
        
        print("🎉 PII Detection Tool Deployment Complete!")
        print("\n📁 Project Structure:")
        print("   ├── detector_varikuti_Narendra_Reddy.py (Main script)")
        print("   ├── requirements.txt (Dependencies)")
        print("   ├── README.md (Documentation)")
        print("   ├── examples/ (Sample data)")
        print("   ├── tests/ (Test suite)")
        print("   └── venv/ (Virtual environment)")
        
        print("\n🚀 Next Steps:")
        print("   1. Activate virtual environment:")
        if os.name == 'nt':  # Windows
            print("      venv\\Scripts\\activate")
        else:  # Unix/Linux/macOS
            print("      source venv/bin/activate")
        
        print("   2. Run the tool:")
        print("      python detector_varikuti_Narendra_Reddy.py your_data.csv")
        
        print("   3. Run tests:")
        print("      python tests/test_detector.py")
        
        print("\n📚 Documentation:")
        print("   - README.md contains detailed usage instructions")
        print("   - examples/sample_input.csv shows expected input format")
        
        return True
    
    def deploy(self):
        """Run the complete deployment process"""
        print("🚀 Starting PII Detection Tool Deployment...")
        
        steps = [
            ("Python Version Check", self.check_python_version),
            ("Create Directories", self.create_directories),
            ("Validate Project Structure", self.validate_project_structure),
            ("Create Virtual Environment", self.create_virtual_environment),
            ("Install Dependencies", self.install_dependencies),
            ("Run Tests", self.run_tests),
            ("Test Sample Data", self.test_sample_data),
            ("Generate Usage Examples", self.generate_usage_examples),
            ("Deployment Summary", self.deployment_summary)
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Deployment failed at step: {step_name}")
                return False
        
        print("\n🎉 Deployment completed successfully!")
        return True


def main():
    """Main deployment function"""
    deployer = PIIDeployment()
    
    try:
        success = deployer.deploy()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during deployment: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
