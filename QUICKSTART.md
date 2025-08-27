# 🚀 Quick Start Guide

Get your PII Detection Tool up and running in 5 minutes!

## Prerequisites

- Python 3.7 or higher
- Git (optional, for cloning)

## Option 1: Automated Setup (Recommended)

1. **Run the deployment script:**
   ```bash
   python deploy.py
   ```

   This will automatically:
   - ✅ Check Python version
   - ✅ Create virtual environment
   - ✅ Install dependencies
   - ✅ Run tests
   - ✅ Test with sample data

2. **Activate the virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Run the tool:**
   ```bash
   python detector_varikuti_Narendra_Reddy.py examples/sample_input.csv
   ```

## Option 2: Manual Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the installation:**
   ```bash
   python tests/test_detector.py
   ```

5. **Run with sample data:**
   ```bash
   python detector_varikuti_Narendra_Reddy.py examples/sample_input.csv
   ```

## 🎯 Your First Run

1. **Prepare your CSV file** with this format:
   ```csv
   record_id,data_json
   1,"{""name"": ""John Doe"", ""phone"": ""9876543210""}"
   2,"{""email"": ""jane@example.com"", ""address"": ""123 Main St""}"
   ```

2. **Run the tool:**
   ```bash
   python detector_varikuti_Narendra_Reddy.py your_data.csv
   ```

3. **Check the output:**
   - Look for `redacted_output_varikuti_narendra_reddy.csv`
   - Each row shows the redacted data and whether PII was detected

## 📊 Example Output

```csv
record_id,redacted_data_json,is_pii
1,"{""name"": ""JXXX DXX"", ""phone"": ""98XXXXXX10""}",true
2,"{""email"": ""jXXXe@example.com"", ""address"": ""[REDACTED_ADDRESS]""}",true
```

## 🔧 Common Commands

```bash
# Basic usage
python detector_varikuti_Narendra_Reddy.py input.csv

# Custom output file
python detector_varikuti_Narendra_Reddy.py input.csv -o my_output.csv

# Run tests
python tests/test_detector.py

# Get help
python detector_varikuti_Narendra_Reddy.py --help
```

## 🆘 Troubleshooting

### "Python not found"
- Make sure Python 3.7+ is installed
- Add Python to your PATH environment variable

### "Module not found"
- Activate the virtual environment first
- Run `pip install -r requirements.txt`

### "File not found"
- Check that your CSV file exists in the current directory
- Use the full path to the file if needed

### "Permission denied"
- On Windows: Run PowerShell as Administrator
- On Linux/macOS: Use `sudo` if needed

## 📞 Need Help?

- 📖 Read the full [README.md](README.md)
- 🧪 Run the tests: `python tests/test_detector.py`
- 🐛 Check the deployment script: `python deploy.py`

---

**🎉 You're all set!** Your PII Detection Tool is ready to protect sensitive data.
