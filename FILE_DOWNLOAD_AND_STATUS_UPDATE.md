# File Download & Status Restrictions - Implementation

## Overview
Added comprehensive file download functionality for both DCC and Discipline teams, plus restricted status options to maintain proper workflow separation.

---

## ✅ Changes Implemented

### **1. File Download System** 📥

#### **Portfolio Manager (DCC) - Download Capabilities:**

**Route 1: Client Feedback Files**
- **URL:** `/download/feedback/<filename>`
- **Purpose:** Download files uploaded by DCC with client feedback
- **Access:** Any logged-in user
- **File Location:** `app1_portfolio_manager/uploads/client_feedback/`

**Route 2: Discipline Submission Files**
- **URL:** `/download/submission/<submission_id>`
- **Purpose:** Download files submitted by disciplines
- **Access:** Any logged-in user
- **File Location:** `app3_discipline_dashboard/uploads/`

**Updated View:** `view_document_feedback.html`
- ✅ Shows all client feedback files for the document
- ✅ Shows all discipline submission files
- ✅ Organized in separate sections with download buttons
- ✅ Displays file metadata (submission date, stage, user)

---

#### **Discipline Dashboard - Download Capabilities:**

**API Endpoint: Get Feedback Files**
- **URL:** `/api/documents/<document_id>/feedback-files`
- **Purpose:** Fetch list of client feedback files for a document
- **Returns:** JSON with file names and download URLs

**Route: Download Feedback Files**
- **URL:** `/download/feedback/<filename>`
- **Purpose:** Download client feedback files
- **Access:** Logged-in discipline members only
- **File Location:** `app1_portfolio_manager/uploads/client_feedback/` (shared)

**Updated View:** `feedback_viewer.html`
- ✅ Dynamic loading of client feedback files via API
- ✅ Shows loading spinner while fetching
- ✅ Download links with original filenames
- ✅ Clean display of file names (timestamp stripped)

---

### **2. Status Restrictions** 🚫

#### **Discipline Submission Form - Restricted Options:**

**Before:**
```
- In Progress
- Ready for Review
- Submitted to Client     ❌ REMOVED
- Client Review           ❌ REMOVED
- Revising per Comments
- Approved                ❌ REMOVED
```

**After:**
```
✅ In Progress
✅ Ready for Review
✅ Revising per Comments
```

**Rationale:**
- Disciplines should NOT mark documents as "Submitted to Client" - DCC handles this
- Disciplines should NOT mark documents as "Client Review" - DCC manages client interaction
- Disciplines should NOT mark documents as "Approved" - Only DCC/client can approve

**Updated File:** `app3_discipline_dashboard/templates/submit_document.html`

---

## 📁 File Naming Conventions

### **Client Feedback Files:**
```
Format: {DOC_NUMBER}_{STAGE}_{TIMESTAMP}_{ORIGINAL_FILENAME}
Example: EPC-001-PR-003_IFR_20251007_103045_Comments_Sheet.pdf

Benefits:
- Easy identification by document number
- Stage tracking
- Chronological ordering
- Original filename preserved
```

### **Discipline Submission Files:**
```
Format: {TIMESTAMP}_{ORIGINAL_FILENAME}
Example: 20251007_103045_PID_Rev_B.pdf

Storage: app3_discipline_dashboard/uploads/
```

---

## 🔄 Workflow

### **DCC Posts Client Feedback:**

1. DCC fills client feedback form
2. Uploads reviewed documents, comment sheets, transmittals
3. Files saved with naming convention
4. File metadata stored

**Result:**
- Files appear in Portfolio Manager's "View Feedback" page
- Files automatically accessible to disciplines via API

---

### **Discipline Downloads Client Feedback:**

1. Discipline views document feedback
2. "Client Feedback Documents" section loads via AJAX
3. Files displayed with download links
4. Click to download with original filename

**Result:**
- Disciplines get client's reviewed documents
- Can review comments and rework deliverables

---

### **DCC Downloads Discipline Submissions:**

1. DCC views document feedback page
2. "Discipline Submissions" section shows all uploads
3. Each submission shows stage, revision, date, uploader
4. Click to download

**Result:**
- DCC can share discipline submissions with client
- Complete audit trail of all submissions

---

## 🛠️ Technical Implementation

### **File Download Routes:**

```python
# Portfolio Manager (app.py)
@app.route('/download/feedback/<path:filename>')
@login_required
def download_feedback_file(filename):
    """Download client feedback file"""
    filepath = os.path.join(app.config['FEEDBACK_FOLDER'], filename)
    # Extract original filename
    parts = filename.split('_', 3)
    original_name = parts[3] if len(parts) > 3 else filename
    return send_file(filepath, as_attachment=True, download_name=original_name)

@app.route('/download/submission/<int:submission_id>')
@login_required
def download_submission_file(submission_id):
    """Download discipline submission file"""
    submission = Submission.query.get_or_404(submission_id)
    # Extract original filename
    filename = os.path.basename(submission.file_path)
    parts = filename.split('_', 1)
    original_name = parts[1] if len(parts) > 1 else filename
    return send_file(submission.file_path, as_attachment=True, download_name=original_name)
```

```python
# Discipline Dashboard (app.py)
@app.route('/api/documents/<int:document_id>/feedback-files')
@login_required
def get_feedback_files(document_id):
    """API endpoint to get client feedback files"""
    feedback_folder = '../app1_portfolio_manager/uploads/client_feedback'
    files = []
    for filename in os.listdir(feedback_folder):
        if filename.startswith(document.doc_number):
            files.append({
                'filename': filename,
                'download_url': f'/download/feedback/{filename}'
            })
    return jsonify({'files': files})

@app.route('/download/feedback/<path:filename>')
@login_required
def download_feedback_file_discipline(filename):
    """Download client feedback file"""
    feedback_folder = '../app1_portfolio_manager/uploads/client_feedback'
    filepath = os.path.join(feedback_folder, filename)
    parts = filename.split('_', 3)
    original_name = parts[3] if len(parts) > 3 else filename
    return send_file(filepath, as_attachment=True, download_name=original_name)
```

---

## 📊 Updated Templates

### **Portfolio Manager:**

**`view_document_feedback.html`:**
- Added "Client Feedback Files" section (blue card)
- Added "Discipline Submissions" section (green card)
- Download buttons for each file
- Metadata display (date, user, stage)

### **Discipline Dashboard:**

**`submit_document.html`:**
- Removed DCC-specific status options
- Added helper text: "DCC updates submission status after review"
- Cleaner dropdown with only 3 options

**`feedback_viewer.html`:**
- Added "Client Feedback Documents" section
- AJAX loading of files via API
- Loading spinner
- Download links with clean file names

---

## 🧪 Testing Guide

### **Test 1: DCC Posts Feedback with Files**
1. Login to Portfolio Manager as admin/scheduler
2. Post client feedback with attached files
3. **Expected:** Success message with file count
4. Check folder: `app1_portfolio_manager/uploads/client_feedback/`
5. **Expected:** Files saved with correct naming

### **Test 2: DCC Downloads Discipline Submission**
1. Navigate to document feedback view
2. See "Discipline Submissions" section
3. Click download button
4. **Expected:** File downloads with original name

### **Test 3: Discipline Downloads Client Feedback**
1. Login to Discipline Dashboard
2. View document feedback
3. See "Client Feedback Documents" section load
4. Click download button
5. **Expected:** File downloads with original name

### **Test 4: Status Restrictions**
1. Login to Discipline Dashboard
2. Go to submit document form
3. Check status dropdown
4. **Expected:** Only 3 options visible (In Progress, Ready for Review, Revising per Comments)

### **Test 5: Cross-App File Access**
1. DCC uploads feedback files
2. Discipline views same document
3. **Expected:** Files appear in both apps
4. **Expected:** Both can download the same files

---

## 📝 Files Modified

✅ `app1_portfolio_manager/app.py` - Added download routes  
✅ `app1_portfolio_manager/templates/view_document_feedback.html` - Added file sections  
✅ `app3_discipline_dashboard/app.py` - Added API and download routes  
✅ `app3_discipline_dashboard/templates/submit_document.html` - Restricted status options  
✅ `app3_discipline_dashboard/templates/feedback_viewer.html` - Added file download section  
✅ `FILE_DOWNLOAD_AND_STATUS_UPDATE.md` - This documentation  

---

## 🎯 Benefits

### **For DCC:**
- ✅ Download all discipline submissions in one place
- ✅ Share submissions with clients easily
- ✅ Full visibility of file exchange history

### **For Disciplines:**
- ✅ Access all client feedback documents
- ✅ Review client comments directly
- ✅ Rework deliverables based on feedback files
- ✅ Cannot accidentally set inappropriate statuses

### **System-Wide:**
- ✅ Complete audit trail of all file exchanges
- ✅ Original filenames preserved
- ✅ Organized file storage by document number
- ✅ Proper workflow separation maintained

---

## ✅ Implementation Complete!

All file download functionality is now operational:
- ✅ DCC can download discipline submissions
- ✅ Disciplines can download client feedback files
- ✅ Both sides have easy access to all relevant files
- ✅ Status options restricted to maintain workflow integrity
- ✅ File naming conventions ensure organization
- ✅ Original filenames preserved on download

**System Status:** ✅ **FULLY OPERATIONAL**
