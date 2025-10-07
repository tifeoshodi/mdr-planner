"""
MDR Stages Configuration
Defines the standard stages and their structure for MDR generation
"""

# Standard stages in order (IFR → IFH → IFD → IFT → IFP → IFA → IFC → AFC)
STANDARD_STAGES = [
    {
        'code': 'IFR',
        'name': 'Information For Review',
        'has_next_rev': False
    },
    {
        'code': 'IFH',
        'name': 'Information For HAZOP',
        'has_next_rev': True
    },
    {
        'code': 'IFD',
        'name': 'Information For Design',
        'has_next_rev': True
    },
    {
        'code': 'IFT',
        'name': 'Information For Tender',
        'has_next_rev': True
    },
    {
        'code': 'IFP',
        'name': 'Information For Procurement',
        'has_next_rev': True
    },
    {
        'code': 'IFA',
        'name': 'Information For Approval',
        'has_next_rev': True
    },
    {
        'code': 'IFC',
        'name': 'Information For Construction',
        'has_next_rev': True
    },
    {
        'code': 'AFC',
        'name': 'Approved For Construction',
        'has_next_rev': False  # Final stage, no next revision
    }
]

# Column structure for each stage
# Each stage has two sections:
# 1. Submission section (to client)
# 2. Feedback section (from client)

SUBMISSION_COLUMNS = [
    {'name': 'Planned', 'width': 12},
    {'name': 'Actual', 'width': 12},
    {'name': 'TR No.', 'width': 15},
    {'name': 'Date Sent', 'width': 12}
]

FEEDBACK_COLUMNS_BASE = [
    {'name': 'Rev. Status', 'width': 12},
    {'name': 'Issue For', 'width': 15},
    {'name': 'Date Received', 'width': 12},  # Changed from "Date Sent"
    {'name': 'Transmittal Received', 'width': 18}  # NEW: Track transmittal number for client feedback
]

def get_feedback_columns(has_next_rev=True):
    """Get feedback columns, optionally including Next Rev."""
    columns = FEEDBACK_COLUMNS_BASE.copy()
    if has_next_rev:
        columns.append({'name': 'Next Rev.', 'width': 12})
    return columns


def get_stage_column_count(has_next_rev=True):
    """Get total number of columns for a stage"""
    return len(SUBMISSION_COLUMNS) + len(get_feedback_columns(has_next_rev))


def calculate_total_columns():
    """Calculate total number of columns in the MDR"""
    # Basic columns: S/No, Doc Number, Doc Title
    basic_cols = 3
    
    # Current Status: Current Rev, Status, Current Transmittal No
    current_status_cols = 3
    
    # Stages
    stages_cols = sum(get_stage_column_count(stage['has_next_rev']) 
                     for stage in STANDARD_STAGES)
    
    # Remarks
    remarks_cols = 1
    
    return basic_cols + current_status_cols + stages_cols + remarks_cols


# Pre-calculate column positions
def get_column_positions():
    """Get starting column positions for each section"""
    positions = {}
    
    current_col = 1
    
    # Basic info
    positions['s_no'] = current_col
    current_col += 1
    positions['doc_number'] = current_col
    current_col += 1
    positions['doc_title'] = current_col
    current_col += 1
    
    # Current status
    positions['current_status_start'] = current_col
    current_col += 3  # Rev, Status, Transmittal
    
    # Stages
    for stage in STANDARD_STAGES:
        positions[f"{stage['code'].lower()}_start"] = current_col
        current_col += get_stage_column_count(stage['has_next_rev'])
    
    # Remarks
    positions['remarks'] = current_col
    
    return positions


if __name__ == '__main__':
    # Test the configuration
    print(f"Total columns: {calculate_total_columns()}")
    print(f"\nColumn positions:")
    for key, val in get_column_positions().items():
        print(f"  {key}: {val}")

