# PII Detection and Redaction Tool

A robust Python-based tool for detecting and redacting Personally Identifiable Information (PII) from CSV datasets. This tool implements both standalone and combinatorial PII detection algorithms to ensure comprehensive data privacy protection.

## � Quick Setup & Deliverables

### Key Files and Commands
```bash
# Clone Repository
git clone https://github.com/yourusername/pii-detection-tool.git

# Main Script
detector_varikuti_Narendra_Reddy.py

# Default Output File
redacted_output_varikuti_narendra_reddy.csv

# Run Command
python detector_varikuti_Narendra_Reddy.py iscp_pii_dataset_-_Sheet1.csv

# Deployment Strategy Document
PII Masking Deployment.pdf
```

## �🚀 Features

- **Standalone PII Detection**: Identifies individual PII elements like phone numbers, Aadhar numbers, passport numbers, and UPI IDs
- **Combinatorial PII Detection**: Detects PII patterns when multiple identifiers appear together
- **Intelligent Redaction**: Applies context-aware redaction techniques to preserve data utility while protecting privacy
- **CSV Processing**: Handles large CSV datasets with JSON-encoded data fields
- **Error Handling**: Robust error handling for malformed data and edge cases

## 📋 Supported PII Types

### Standalone PII
- **Phone Numbers**: 10-digit Indian phone numbers
- **Aadhar Numbers**: 12-digit Aadhar identification numbers
- **Passport Numbers**: Indian passport format validation
- **UPI IDs**: UPI payment identifiers

### Combinatorial PII
- **Name + Email + Address**: Personal identification patterns
- **Device Context**: IP addresses and device identifiers
- **Multi-field Patterns**: Complex PII combinations

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pii-detection-tool.git
   cd pii-detection-tool
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Basic Usage

```bash
python detector_varikuti_Narendra_Reddy.py input_file.csv
```

### Advanced Usage

```bash
# Specify custom output file
python detector_varikuti_Narendra_Reddy.py input_file.csv -o custom_output.csv

# Process with verbose output
python detector_varikuti_Narendra_Reddy.py input_file.csv --verbose
```

### Example Commands

```bash
# Process the sample dataset
python detector_varikuti_Narendra_Reddy.py iscp_pii_dataset_-_Sheet1.csv

# Generate output with custom name
python detector_varikuti_Narendra_Reddy.py iscp_pii_dataset_-_Sheet1.csv -o my_redacted_data.csv
```

## 📊 Input/Output Format

### Input CSV Format
The tool expects a CSV file with the following columns:
- `record_id`: Unique identifier for each record
- `data_json`: JSON string containing the data to be processed

**Example Input:**
```csv
record_id,data_json
1,"{""name"": ""John Doe"", ""email"": ""john.doe@example.com"", ""phone"": ""9876543210"", ""address"": ""123 Main St, City""}"
2,"{""name"": ""Jane Smith"", ""aadhar"": ""1234 5678 9012"", ""passport"": ""A1234567"", ""upi_id"": ""jane@upi""}"
```

### Output CSV Format
The tool generates a CSV file with the following columns:
- `record_id`: Original record identifier
- `redacted_data_json`: JSON string with redacted data
- `is_pii`: Boolean indicating if PII was detected

**Example Output:**
```csv
record_id,redacted_data_json,is_pii
1,"{""name"": ""JXXX DXX"", ""email"": ""jXXXe@example.com"", ""phone"": ""98XXXXXX10"", ""address"": ""[REDACTED_ADDRESS]""}",true
2,"{""name"": ""JXXX SXXXX"", ""aadhar"": ""XXXXXXXX9012"", ""passport"": ""AXXXXXX7"", ""upi_id"": ""[REDACTED_UPI]""}",true
```

## 🔧 Redaction Examples

### Phone Number Redaction
- **Input**: `9876543210`
- **Output**: `98XXXXXX10`

### Aadhar Number Redaction
- **Input**: `1234 5678 9012`
- **Output**: `XXXXXXXX9012`

### Name Redaction
- **Input**: `John Doe`
- **Output**: `JXXX DXX`

### Email Redaction
- **Input**: `john.doe@example.com`
- **Output**: `jXXXe@example.com`

## 🏗️ Project Structure

```
pii-detection-tool/
├── detector_varikuti_Narendra_Reddy.py    # Main PII detection script
├── requirements.txt                        # Python dependencies
├── README.md                              # This file
├── examples/                              # Example datasets
│   ├── sample_input.csv                   # Sample input file
│   └── sample_output.csv                  # Sample output file
├── tests/                                 # Test files
│   └── test_detector.py                   # Unit tests
└── docs/                                  # Documentation
    └── API.md                             # API documentation
```

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python tests/test_detector.py
```

Or run the deployment script for comprehensive testing:

```bash
python deploy.py
```

## 📈 Performance

- **Processing Speed**: ~1000 records/second (depending on data complexity)
- **Memory Usage**: Optimized for large datasets
- **Accuracy**: High precision PII detection with minimal false positives

## 🔒 Security Features

- **No Data Storage**: Processes data in-memory without persistent storage
- **Secure Redaction**: Irreversible data transformation
- **Input Validation**: Robust validation of input data formats
- **Error Logging**: Comprehensive error tracking without exposing sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Varikuti Narendra Reddy**
- GitHub: [@NandhaReddy8](https://github.com/NandhaReddy8)
- Email: narendravarikuti.2003@gmail.com

## 🙏 Acknowledgments

- Built for ISCP (Info-Sec Certification Program) dataset processing
- Implements industry-standard PII detection algorithms
- Designed for production-ready data privacy compliance

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: nandhareddy.05@gmail.com
- Documentation: [Wiki](https://github.com/yourusername/pii-detection-tool/wiki)

---

**⚠️ Important**: This tool is designed for data privacy protection. Always ensure compliance with local data protection regulations when processing sensitive information.
