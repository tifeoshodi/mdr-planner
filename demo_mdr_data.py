"""
Demo data for MDR (Master Document Register) Planner
Contains typical document types for EPC projects across different engineering disciplines.
"""

from mdr_planner import DocumentRecord, DocumentCategory, DocumentStatus


def get_demo_project_info():
    """Get demo project information"""
    return {
        'project_name': 'Sample EPC Project - Gas Processing Plant',
        'project_code': 'EPC-2024-001', 
        'client': 'Sample Oil & Gas Company'
    }


def get_demo_documents():
    """Get comprehensive demo document list for typical EPC project"""
    return [
        # Project Management & Administration Documents
        DocumentRecord("PMA-001", "Project Basis of Design", DocumentCategory.PROJECT_MGMT, DocumentStatus.COMPLETED, 
                     current_rev="Rev 5", current_status="AFC", current_transmittal_no="TR-008",
                     # IFR Stage
                     ifr_date_planned="15-01-2024", ifr_date_actual="15-01-2024", ifr_tr_no="TR-001", 
                     ifr_date_sent="15-01-2024", ifr_rev_status="A", ifr_issue_for="Review",
                     ifr_date_received="20-01-2024",
                     # IFH Stage
                     ifh_date_planned="22-01-2024", ifh_date_actual="22-01-2024", ifh_tr_no="TR-002",
                     ifh_date_sent="22-01-2024", ifh_rev_status="B", ifh_issue_for="HAZOP",
                     ifh_date_received="25-01-2024", ifh_next_rev="Rev C",
                     # IFD Stage
                     ifd_date_planned="28-01-2024", ifd_date_actual="28-01-2024", ifd_tr_no="TR-003",
                     ifd_date_sent="28-01-2024", ifd_rev_status="C", ifd_issue_for="Design",
                     ifd_date_received="02-02-2024", ifd_next_rev="Rev D",
                     # IFT Stage
                     ift_date_planned="05-02-2024", ift_date_actual="05-02-2024", ift_tr_no="TR-004",
                     ift_date_sent="05-02-2024", ift_rev_status="D", ift_issue_for="Tender",
                     ift_date_received="10-02-2024", ift_next_rev="Rev E",
                     # IFP Stage
                     ifp_date_planned="12-02-2024", ifp_date_actual="12-02-2024", ifp_tr_no="TR-005",
                     ifp_date_sent="12-02-2024", ifp_rev_status="E", ifp_issue_for="Procurement",
                     ifp_date_received="15-02-2024", ifp_next_rev="Rev 1",
                     # IFA Stage
                     ifa_date_planned="18-02-2024", ifa_date_actual="18-02-2024", ifa_tr_no="TR-006",
                     ifa_date_sent="18-02-2024", ifa_rev_status="Rev 1", ifa_issue_for="Approval",
                     ifa_date_received="22-02-2024", ifa_next_rev="Rev 2",
                     # IFC Stage
                     ifc_date_planned="25-02-2024", ifc_date_actual="25-02-2024", ifc_tr_no="TR-007",
                     ifc_date_sent="25-02-2024", ifc_rev_status="Rev 2", ifc_issue_for="Construction",
                     ifc_date_received="28-02-2024", ifc_next_rev="Rev 3",
                     # AFC Stage
                     afc_date_planned="01-03-2024", afc_date_actual="01-03-2024", afc_tr_no="TR-008",
                     afc_date_sent="01-03-2024", afc_rev_status="Rev 3", afc_issue_for="Construction",
                     afc_date_received="05-03-2024",
                     remarks="All stages completed - Final approved document"),
        DocumentRecord("PMA-002", "Project Schedule", DocumentCategory.PROJECT_MGMT, DocumentStatus.IN_PROGRESS,
                     current_rev="Rev 1", current_status="In Progress - IFD", current_transmittal_no="TR-012",
                     # IFR Stage
                     ifr_date_planned="20-01-2024", ifr_date_actual="20-01-2024", ifr_tr_no="TR-009",
                     ifr_date_sent="20-01-2024", ifr_rev_status="A", ifr_issue_for="Review",
                     ifr_date_received="25-01-2024",
                     # IFH Stage
                     ifh_date_planned="28-01-2024", ifh_date_actual="28-01-2024", ifh_tr_no="TR-010",
                     ifh_date_sent="28-01-2024", ifh_rev_status="B", ifh_issue_for="HAZOP",
                     ifh_date_received="01-02-2024", ifh_next_rev="Rev C",
                     # IFD Stage (in progress)
                     ifd_date_planned="05-02-2024", ifd_date_actual="", ifd_tr_no="",
                     ifd_date_sent="", ifd_rev_status="", ifd_issue_for="",
                     ifd_date_received="", ifd_next_rev="",
                     remarks="Currently being finalized for design"),
        DocumentRecord("PMA-003", "Project Execution Plan", DocumentCategory.PROJECT_MGMT, DocumentStatus.APPROVED,
                     current_rev="Rev 1", current_status="IFA Complete", current_transmittal_no="TR-015",
                     # IFR Stage
                     ifr_date_planned="25-01-2024", ifr_date_actual="25-01-2024", ifr_tr_no="TR-013",
                     ifr_date_sent="25-01-2024", ifr_rev_status="A", ifr_issue_for="Review",
                     ifr_date_received="28-01-2024",
                     # IFA Stage
                     ifa_date_planned="02-02-2024", ifa_date_actual="02-02-2024", ifa_tr_no="TR-015",
                     ifa_date_sent="02-02-2024", ifa_rev_status="Rev 1", ifa_issue_for="Approval",
                     ifa_date_received="05-02-2024", ifa_next_rev="Rev 2",
                     remarks="Approved by client, awaiting construction stage"),
        DocumentRecord("PMA-004", "Project Quality Plan", DocumentCategory.PROJECT_MGMT, DocumentStatus.IN_PROGRESS),
        DocumentRecord("PMA-005", "Communication Management Plan", DocumentCategory.PROJECT_MGMT, DocumentStatus.UNDER_REVIEW),
        DocumentRecord("PMA-006", "Project Management Plan", DocumentCategory.PROJECT_MGMT, DocumentStatus.NOT_STARTED),
        DocumentRecord("PMA-007", "HSE Plan", DocumentCategory.PROJECT_MGMT, DocumentStatus.UNDER_REVIEW),
        DocumentRecord("PMA-008", "Master Deliverables Register and Progress Measurement System", DocumentCategory.PROJECT_MGMT, DocumentStatus.NOT_STARTED),
        DocumentRecord("PMA-009", "Weekly Progress/Management Meetings Minutes", DocumentCategory.PROJECT_MGMT, DocumentStatus.NOT_STARTED),
        DocumentRecord("PMA-010", "Project Control Procedure", DocumentCategory.PROJECT_MGMT, DocumentStatus.NOT_STARTED),
        DocumentRecord("PMA-011", "Document Control Plan", DocumentCategory.PROJECT_MGMT, DocumentStatus.COMPLETED),
        DocumentRecord("PMA-012", "HAZOP/HAZID Review", DocumentCategory.PROJECT_MGMT, DocumentStatus.IN_PROGRESS),
        DocumentRecord("PMA-013", "Design Review Report", DocumentCategory.PROJECT_MGMT, DocumentStatus.NOT_STARTED),
        DocumentRecord("PMA-014", "Milestone Report", DocumentCategory.PROJECT_MGMT, DocumentStatus.NOT_STARTED),
        DocumentRecord("PMA-015", "Project Close-Out Report", DocumentCategory.PROJECT_MGMT, DocumentStatus.NOT_STARTED),
        DocumentRecord("PMA-016", "Cost Estimation", DocumentCategory.PROJECT_MGMT, DocumentStatus.APPROVED),

        # Technical Safety Documents
        DocumentRecord("TS-001", "HAZOP Terms of Reference", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.COMPLETED),
        DocumentRecord("TS-002", "HAZOP Close Out Report", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.IN_PROGRESS),
        DocumentRecord("TS-003", "HAZOP Study Report", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.UNDER_REVIEW),
        DocumentRecord("TS-004", "HSE Design Philosophy", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.IN_PROGRESS),
        DocumentRecord("TS-005", "Safety Management System", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.NOT_STARTED),
        DocumentRecord("TS-006", "Hazardous Area Classification Schedule", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.NOT_STARTED),
        DocumentRecord("TS-007", "Hazardous Area Classification Drawings", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.NOT_STARTED),
        DocumentRecord("TS-008", "Safety Workshop (HAZID, HAZOP) and design review", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.NOT_STARTED),
        DocumentRecord("TS-009", "Safety Data Sheets (SDS)", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.IN_PROGRESS),
        DocumentRecord("TS-010", "Fire and Gas Detection Philosophy", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.NOT_STARTED),
        DocumentRecord("TS-011", "Emergency Response Plan", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.NOT_STARTED),
        DocumentRecord("TS-012", "Safety Instrumented Systems (SIS) Specifications", DocumentCategory.TECHNICAL_SAFETY, DocumentStatus.NOT_STARTED),

        # Process Documents
        DocumentRecord("PR-001", "Flow Assurance - Slugging Transient Analysis and Report", DocumentCategory.PROCESS, DocumentStatus.IN_PROGRESS),
        DocumentRecord("PR-002", "HYSYS Simulation & Report", DocumentCategory.PROCESS, DocumentStatus.UNDER_REVIEW),
        DocumentRecord("PR-003", "Heat & Material Balance Report", DocumentCategory.PROCESS, DocumentStatus.COMPLETED),
        DocumentRecord("PR-004", "Line Sizing Calculations Note", DocumentCategory.PROCESS, DocumentStatus.NOT_STARTED),
        DocumentRecord("PR-005", "Equipment Sizing Calculations Note", DocumentCategory.PROCESS, DocumentStatus.IN_PROGRESS),
        DocumentRecord("PR-006", "Flare Balance Report", DocumentCategory.PROCESS, DocumentStatus.NOT_STARTED),
        DocumentRecord("PR-007", "Line List", DocumentCategory.PROCESS, DocumentStatus.NOT_STARTED),
        DocumentRecord("PR-008", "GHG Emission Report", DocumentCategory.PROCESS, DocumentStatus.NOT_STARTED),
        DocumentRecord("PR-009", "Process Operating and Control Philosophy", DocumentCategory.PROCESS, DocumentStatus.NOT_STARTED),
        DocumentRecord("PR-010", "Isolation Philosophy", DocumentCategory.PROCESS, DocumentStatus.NOT_STARTED),
        DocumentRecord("PR-011", "Control Valve Sizing Calculation Note", DocumentCategory.PROCESS, DocumentStatus.NOT_STARTED),
        DocumentRecord("PR-012", "Process Flow Diagrams (PFDs)", DocumentCategory.PROCESS, DocumentStatus.APPROVED),
        DocumentRecord("PR-013", "Utility Flow Diagrams", DocumentCategory.PROCESS, DocumentStatus.IN_PROGRESS),
        DocumentRecord("PR-014", "Equipment Data Sheets", DocumentCategory.PROCESS, DocumentStatus.IN_PROGRESS),
        DocumentRecord("PR-015", "Process Description Document", DocumentCategory.PROCESS, DocumentStatus.COMPLETED),
        DocumentRecord("PR-016", "Process Simulation Model", DocumentCategory.PROCESS, DocumentStatus.UNDER_REVIEW),

        # Piping Documents
        DocumentRecord("PI-001", "Piping Specifications", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),
        DocumentRecord("PI-002", "Piping Isometric Drawings", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),
        DocumentRecord("PI-003", "Piping Layout Drawings", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),
        DocumentRecord("PI-004", "Piping Stress Analysis", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),
        DocumentRecord("PI-005", "Piping Material List", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),
        DocumentRecord("PI-006", "Pipe Support Design", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),
        DocumentRecord("PI-007", "Underground Piping Layout", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),
        DocumentRecord("PI-008", "Piping Installation Procedures", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),
        DocumentRecord("PI-009", "Thermal Expansion Analysis", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),
        DocumentRecord("PI-010", "Piping System Pressure Testing", DocumentCategory.PIPING, DocumentStatus.NOT_STARTED),

        # Mechanical Documents
        DocumentRecord("ME-001", "Equipment Specifications", DocumentCategory.MECHANICAL, DocumentStatus.IN_PROGRESS),
        DocumentRecord("ME-002", "Material Requisitions", DocumentCategory.MECHANICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("ME-003", "Equipment Layout Drawings", DocumentCategory.MECHANICAL, DocumentStatus.IN_PROGRESS),
        DocumentRecord("ME-004", "Vessel Design Calculations", DocumentCategory.MECHANICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("ME-005", "Pump Selection and Sizing", DocumentCategory.MECHANICAL, DocumentStatus.IN_PROGRESS),
        DocumentRecord("ME-006", "Compressor Specifications", DocumentCategory.MECHANICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("ME-007", "Heat Exchanger Design Calculations", DocumentCategory.MECHANICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("ME-008", "Equipment Installation Procedures", DocumentCategory.MECHANICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("ME-009", "Rotating Equipment Alignment", DocumentCategory.MECHANICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("ME-010", "Static Equipment Design", DocumentCategory.MECHANICAL, DocumentStatus.NOT_STARTED),

        # Electrical Documents  
        DocumentRecord("EL-001", "Electrical Load List", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("EL-002", "Electrical Single Line Diagrams", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("EL-003", "Motor Control Center Drawings", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("EL-004", "Power Distribution System Design", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("EL-005", "Lighting Design and Layout", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("EL-006", "Grounding System Design", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("EL-007", "Electrical Equipment Specifications", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("EL-008", "Cable Tray Layout Drawings", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("EL-009", "Emergency Power System Design", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("EL-010", "Electrical Installation Procedures", DocumentCategory.ELECTRICAL, DocumentStatus.NOT_STARTED),

        # Instrumentation Documents
        DocumentRecord("IN-001", "Instrument Index", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),
        DocumentRecord("IN-002", "P&ID Drawings", DocumentCategory.INSTRUMENTATION, DocumentStatus.IN_PROGRESS),
        DocumentRecord("IN-003", "Control System Architecture", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),
        DocumentRecord("IN-004", "Instrument Specifications", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),
        DocumentRecord("IN-005", "Control Logic Diagrams", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),
        DocumentRecord("IN-006", "Cause and Effect Diagrams", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),
        DocumentRecord("IN-007", "Instrument Installation Details", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),
        DocumentRecord("IN-008", "Control Panel Layout Drawings", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),
        DocumentRecord("IN-009", "SCADA System Specifications", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),
        DocumentRecord("IN-010", "Instrument Calibration Procedures", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),
        DocumentRecord("IN-011", "DCS Configuration Documentation", DocumentCategory.INSTRUMENTATION, DocumentStatus.NOT_STARTED),

        # Civil & Structural Documents
        DocumentRecord("CS-001", "Plot Plan", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.IN_PROGRESS),
        DocumentRecord("CS-002", "Foundation Drawings", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("CS-003", "Structural Steel Drawings", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("CS-004", "Civil Site Layout", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.APPROVED),
        DocumentRecord("CS-005", "Concrete Specifications", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("CS-006", "Structural Design Calculations", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("CS-007", "Soil Investigation Report", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.COMPLETED),
        DocumentRecord("CS-008", "Drainage System Design", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("CS-009", "Road and Pavement Design", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("CS-010", "Fire Water System Layout", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("CS-011", "Building Architecture Drawings", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.NOT_STARTED),
        DocumentRecord("CS-012", "Site Utilities Plan", DocumentCategory.CIVIL_STRUCTURAL, DocumentStatus.NOT_STARTED),

        # Corrosion Documents
        DocumentRecord("CO-001", "Corrosion Assessment Report", DocumentCategory.CORROSION, DocumentStatus.NOT_STARTED),
        DocumentRecord("CO-002", "Material Selection for Corrosion Resistance", DocumentCategory.CORROSION, DocumentStatus.NOT_STARTED),
        DocumentRecord("CO-003", "Cathodic Protection System Design", DocumentCategory.CORROSION, DocumentStatus.NOT_STARTED),
        DocumentRecord("CO-004", "Corrosion Monitoring Plan", DocumentCategory.CORROSION, DocumentStatus.NOT_STARTED),
        DocumentRecord("CO-005", "Chemical Injection System for Corrosion Control", DocumentCategory.CORROSION, DocumentStatus.NOT_STARTED),
        DocumentRecord("CO-006", "Coating Specifications", DocumentCategory.CORROSION, DocumentStatus.NOT_STARTED),

        # Telecommunications Documents
        DocumentRecord("TC-001", "Telecommunications System Design", DocumentCategory.TELECOMMUNICATIONS, DocumentStatus.NOT_STARTED),
        DocumentRecord("TC-002", "PABX System Specifications", DocumentCategory.TELECOMMUNICATIONS, DocumentStatus.NOT_STARTED),
        DocumentRecord("TC-003", "Data Network Architecture", DocumentCategory.TELECOMMUNICATIONS, DocumentStatus.NOT_STARTED),
        DocumentRecord("TC-004", "CCTV System Design", DocumentCategory.TELECOMMUNICATIONS, DocumentStatus.NOT_STARTED),
        DocumentRecord("TC-005", "Radio Communication System", DocumentCategory.TELECOMMUNICATIONS, DocumentStatus.NOT_STARTED),
        DocumentRecord("TC-006", "Fiber Optic Cable Layout", DocumentCategory.TELECOMMUNICATIONS, DocumentStatus.NOT_STARTED)
    ]


def get_document_count_summary():
    """Get summary of document counts by category"""
    documents = get_demo_documents()
    summary = {}
    
    for category in DocumentCategory:
        count = len([doc for doc in documents if doc.category == category])
        summary[category.value] = count
    
    return summary


def print_demo_summary():
    """Print a summary of the demo data"""
    project_info = get_demo_project_info()
    documents = get_demo_documents()
    summary = get_document_count_summary()
    
    print("=" * 60)
    print("MDR DEMO DATA SUMMARY")
    print("=" * 60)
    print(f"Project: {project_info['project_name']}")
    print(f"Code: {project_info['project_code']}")
    print(f"Client: {project_info['client']}")
    print(f"Total Documents: {len(documents)}")
    print("\nDocuments by Category:")
    print("-" * 30)
    
    for category, count in summary.items():
        print(f"{category}: {count}")
    
    print("\nStatus Distribution:")
    print("-" * 20)
    status_counts = {}
    for doc in documents:
        status = doc.status.value
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        print(f"{status}: {count}")


if __name__ == "__main__":
    print_demo_summary() 