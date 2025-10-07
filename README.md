# MDR (Master Document Register) Management System

A comprehensive **multi-application system** for managing Master Document Registers in EPC (Engineering, Procurement, and Construction) projects. Features both desktop (Tkinter) and web applications (Flask) with real-time collaboration, Excel integration, and complete document lifecycle tracking.

## 🌟 System Components

1. **Tkinter DCC App** - Desktop application for Document Control Centre
2. **Portfolio Manager** (App 1) - Web-based DCC interface with spreadsheet view
3. **Scheduler** (App 2) - Project scheduling and WBS management
4. **Discipline Dashboard** (App 3) - Web interface for engineering disciplines

## 🚀 Quick Start (Local Development)

```bash
# Install dependencies
pip install -r requirements_flask_apps.txt

# Start all Flask apps
start_all_apps.bat   # Windows
# or
./start_all_apps.sh  # Linux/Mac

# Or run Tkinter app
python mdr_planner.py
```

## ☁️ Cloud Deployment

**Ready for production deployment on Railway.app!**

- **Quick Start:** See [DEPLOYMENT_QUICK_START.md](DEPLOYMENT_QUICK_START.md)
- **Full Guide:** See [DEPLOYMENT_GUIDE_RAILWAY.md](DEPLOYMENT_GUIDE_RAILWAY.md)

Deployment time: **5 minutes** | Cost: **~$15-20/month**

---

## What is an MDR?

A Master Document Register (MDR) is a critical project management tool used in EPC projects to:
- Track all project documents and deliverables
- Monitor document progress through different stages (IFR, IFA, IFC)
- Manage document approval workflows
- Ensure project deliverables are completed on time
- Maintain document version control and transmittal records

## Document Lifecycle Stages

- **IFR (Information For Review)**: Initial document submission for review and comments
- **IFA (Information For Approval)**: Document submitted for formal approval after incorporating review comments  
- **IFC (Information For Construction)**: Final approved document ready for construction/implementation

## Features

### 🎯 **Comprehensive Document Tracking**
- Track documents across 7 engineering categories:
  - Project Management & Administration
  - Technical Safety
  - Process
  - Mechanical
  - Electrical
  - Instrumentation
  - Civil & Structural

### 📊 **Professional Excel Output**
- Generates formatted Excel files matching industry standards
- Color-coded sections for easy navigation
- Professional layout with proper headers and formatting
- Follows the format shown in the reference screenshot

### 🗂️ **Document Status Management**
- Track document status: Not Started, In Progress, Under Review, Approved, Completed
- Monitor dates for each lifecycle stage
- Track transmittal numbers and revision statuses

### 💼 **Project Information Management**
- Store project name, code, and client information
- Generate project-specific MDRs
- Export summary reports

### 🎮 **User-Friendly Interface**
- Intuitive GUI with organized sections
- Easy document entry and editing
- Built-in demo data for testing
- Comprehensive preview functionality

## Installation

1. **Clone or download** the MDR_Planner folder
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start

1. **Run the application**:
   ```bash
   python mdr_planner.py
   ```

2. **Load demo data** (optional):
   - Click "Load Demo Data" to see example documents
   - This loads a typical EPC project with 70+ documents

3. **Enter project information**:
   - Project Name: Your project's name
   - Project Code: Internal project identifier
   - Client: Client company name

4. **Add documents**:
   - Enter document title
   - Select appropriate category
   - Set initial status
   - Click "Add Document"

5. **Generate MDR**:
   - Click "Preview MDR" to review
   - Click "Generate Excel" to create the final MDR

### Detailed Workflow

#### Adding Documents
1. Fill in the "Document Title" field
2. Select the appropriate "Category" from the dropdown
3. Choose the current "Status"
4. Click "Add Document"

#### Managing Documents
- View all documents in the list below
- Right-click on documents for context menu options
- Delete unwanted documents with confirmation

#### Generating Output
- **Preview**: Shows a text summary of your MDR
- **Generate Excel**: Creates a professionally formatted Excel file
- Both functions also generate accompanying text summary files

## Document Categories

### Project Management & Administration
- Project plans, schedules, procedures
- HSE documentation
- Quality management documents
- Project control procedures

### Technical Safety
- HAZOP studies and reports
- Safety management systems
- Hazardous area classifications
- Emergency response plans

### Process
- Process flow diagrams
- Heat & material balances
- Equipment sizing calculations
- Simulation reports

### Mechanical
- Equipment specifications
- Piping designs and layouts
- Vessel calculations
- Installation procedures

### Electrical
- Electrical load lists
- Single line diagrams
- Power distribution designs
- Control center layouts

### Instrumentation
- P&ID drawings
- Instrument specifications
- Control system architecture
- SCADA configurations

### Civil & Structural
- Plot plans and layouts
- Foundation designs
- Structural calculations
- Site utilities

## File Structure

```
MDR_Planner/
├── mdr_planner.py          # Main application
├── demo_mdr_data.py        # Demo data module
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Generated Files

When you generate an MDR, the application creates:
- **`ProjectName_MDR.xlsx`**: Main Excel MDR file
- **`ProjectName_MDR_summary.txt`**: Text summary of the MDR

## Demo Data

The application includes comprehensive demo data featuring:
- **70+ typical EPC project documents**
- **All 7 engineering categories** represented
- **Various status levels** for realistic testing
- **Sample project information** for a Gas Processing Plant

## Tips for Use

1. **Start with demo data** to understand the format
2. **Use consistent naming** for document titles
3. **Keep categories organized** by engineering discipline
4. **Regular backups** - save your Excel files frequently
5. **Project codes** help with file organization

## Technical Requirements

- **Python 3.7+**
- **openpyxl** for Excel file generation
- **tkinter** for GUI (usually included with Python)
- **Windows/Mac/Linux** compatible

## Support

This tool is designed for EPC project managers and document controllers who need to maintain comprehensive document registers throughout project lifecycles.

For questions or issues:
1. Check that all dependencies are installed
2. Ensure you have write permissions for the output directory
3. Verify Excel files are not open when generating new ones

## License

This project is provided as-is for educational and professional use in EPC project management.