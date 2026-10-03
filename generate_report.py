"""
Generate publication-quality 4-page PDF report for Assignment 2:
End-to-End ML Versioning with Git, DVC & Google Drive.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 755, "Assignment 2: End-to-End ML Versioning with Git, DVC & Google Drive")
            self.drawRightString(567, 755, "Zainab Fatima | i.aenonic@gmail.com")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(45, 747, 567, 747)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(45, 40, 567, 40)
        
        self.setFont("Helvetica", 8)
        self.drawString(45, 28, "GitHub: https://github.com/Aenonic/fashion-ann-pipeline")
        self.drawRightString(567, 28, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def create_report(filename="Fashion_ANN_Pipeline_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    primary = colors.HexColor("#1A365D")   # Deep navy
    secondary = colors.HexColor("#2B6CB0") # Cobalt blue
    dark = colors.HexColor("#2D3748")      # Charcoal
    light_bg = colors.HexColor("#F7FAFC")
    border_color = colors.HexColor("#CBD5E0")
    code_bg = colors.HexColor("#0F172A")   # Dark slate
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary,
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=secondary,
        spaceAfter=8
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=dark
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14,
        textColor=primary,
        spaceBefore=6,
        spaceAfter=4,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=secondary,
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=dark,
        spaceAfter=3
    )
    
    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10,
        textColor=dark,
        leftIndent=10,
        spaceAfter=2
    )
    
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.2,
        textColor=colors.HexColor("#E2E8F0")
    )
    
    story = []
    
    # ================= PAGE 1 =================
    story.append(Paragraph("Assignment 2: End-to-End ML Versioning", title_style))
    story.append(Paragraph("Collaborative Git Workflows, DVC Data Pipelines & Google Drive Remote Storage", subtitle_style))
    
    meta_data = [
        [
            Paragraph("<b>Student:</b> Zainab Fatima", meta_style),
            Paragraph("<b>Email:</b> i.aenonic@gmail.com", meta_style),
            Paragraph("<b>Date:</b> October 2026", meta_style)
        ],
        [
            Paragraph("<b>GitHub:</b> <a href='https://github.com/Aenonic/fashion-ann-pipeline'><u>github.com/Aenonic/fashion-ann-pipeline</u></a>", meta_style),
            Paragraph("<b>DVC Remote:</b> gdrive://gdrive_storage", meta_style),
            Paragraph("<b>Dataset:</b> Fashion-MNIST (70,000 samples)", meta_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 185, 157])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("Part A — Git Fundamentals & Advanced Commands", h1_style))
    
    a_summary = [
        ["Sub-Task", "Command Executed", "Operational Impact & Visibility"],
        [
            "A1: Init & Ignore",
            "git init -b main\ngit add README.md .gitignore\ngit commit -m 'A1: Initial...'",
            "Established root commit on main with comprehensive .gitignore excluding venv/, *.h5, .dvc/cache, and token files."
        ],
        [
            "A2: Branch dev",
            "git checkout -b dev",
            "Isolated feature engineering and pipeline authoring from main with 8 granular incremental commits."
        ],
        [
            "A5: Stash Workflow",
            "git stash push -u -m 'WIP...'\ngit stash list\ngit checkout main -> dev\ngit stash pop",
            "Shelved uncommitted working tree modifications in preprocess.py to check main, then restored working state cleanly."
        ],
        [
            "A6: Rebase Scenario",
            "git checkout -b hotfix main\ngit commit -am 'hotfix...'\ngit checkout main && git merge hotfix\ngit checkout dev && git rebase main",
            "Rebased dev on top of updated main (hotfix commit 570787f), creating a linear history without redundant merge bubbles."
        ],
        [
            "A7: Soft vs Hard Reset",
            "git reset --soft HEAD~1\ngit reset --hard HEAD~1",
            "Soft reset preserved modifications staged in index; hard reset discarded all commit, index, and tree modifications."
        ],
        [
            "A8: Tracked Reorg",
            "git mv prepare_raw.py src/prepare.py\ngit rm scratch_notes.txt",
            "Executed file movements and scratch deletion as native tracked Git tree rename and delete events."
        ]
    ]
    t_a = Table(a_summary, colWidths=[75, 175, 272])
    t_a.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('TOPPADDING', (0,0), (-1,0), 3),
        ('BOTTOMPADDING', (0,0), (-1,0), 3),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,1), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,1), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_a)
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("A3 & A4: Advanced Log and Diff Analysis", h2_style))
    log_diff_points = [
        "<b>git log --oneline --graph --all:</b> Renders full topological DAG across all local/remote branches and tags simultaneously.",
        "<b>git log --stat -3:</b> Summarizes file modifications, insertions (+), and deletions (-) across the 3 most recent commits.",
        "<b>git log -p -1:</b> Generates unified diff patch displaying exact line-by-line additions/deletions in the latest commit.",
        "<b>git log main..dev:</b> Computes reachability range showing commits present on dev that have not yet been integrated into main.",
        "<b>Two-Dot (main..dev) vs Three-Dot (main...dev) Diff:</b> <code>main..dev</code> computes the direct diff between both branch tips. <code>main...dev</code> compares changes on <code>dev</code> originating from the common ancestor (merge base), ignoring divergent changes made on <code>main</code>."
    ]
    for pt in log_diff_points:
        story.append(Paragraph(f"• {pt}", bullet_style))
    
    story.append(Spacer(1, 3))
    story.append(Paragraph("Part B — Modular TensorFlow ANN Pipeline Architecture", h1_style))
    pipe_modules = [
        ["Module", "Input Dependencies", "Outputs Produced", "Key Functionality"],
        ["src/prepare.py", "tf.keras.datasets.fashion_mnist", "data/raw/*.npy", "Loads 60k train & 10k test 28x28 arrays without manual download."],
        ["src/preprocess.py", "data/raw/, params.yaml", "data/processed/*.npy", "Normalizes pixels to [0, 1] and creates stratified 20% validation split."],
        ["src/train.py", "data/processed/, params.yaml", "models/model.h5, history.csv", "Sequential ANN: Flatten -> Dense(ReLU) -> Dropout -> Dense(10, Softmax)."],
        ["src/evaluate.py", "models/model.h5, data/processed/", "metrics.json, confusion_matrix.png", "Calculates loss/accuracy on test set and logs evaluation metrics."]
    ]
    t_pipe = Table(pipe_modules, colWidths=[80, 135, 140, 167])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.2),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('FONTSIZE', (0,1), (-1,-1), 6.8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_pipe)
    
    story.append(PageBreak())
    
    # ================= PAGE 2 =================
    story.append(Paragraph("Part C — DVC Setup & Google Drive Remote Storage", h1_style))
    story.append(Paragraph(
        "DVC was initialized (<code>dvc init</code>) on branch <code>dev</code>. Google Drive was registered as remote storage via <code>dvc remote add -d gdrive_storage gdrive://&lt;FOLDER_ID&gt;</code>. Authentication operates via PyDrive2 OAuth loop in Brave Browser, caching access tokens locally while strictly excluded from Git via <code>.gitignore</code>.",
        body_style
    ))
    
    story.append(Spacer(1, 3))
    story.append(Paragraph("Part D — DVC Pipeline Definitions (dvc.yaml & params.yaml)", h1_style))
    
    params_content = """# params.yaml
preprocess:
  test_size: 0.2
  seed: 42

train:
  dense_units: 256
  dropout_rate: 0.2
  learning_rate: 0.001
  epochs: 10
  batch_size: 64"""

    dvc_yaml_content = """# dvc.yaml (Multi-Stage Pipeline Definition)
stages:
  prepare:
    cmd: python3 src/prepare.py
    deps: [src/prepare.py]
    outs: [data/raw]
  preprocess:
    cmd: python3 src/preprocess.py
    deps: [data/raw, src/preprocess.py]
    params: [preprocess.test_size, preprocess.seed]
    outs: [data/processed]
  train:
    cmd: python3 src/train.py
    deps: [data/processed, src/train.py]
    params: [train.batch_size, train.dense_units, train.dropout_rate, train.epochs, train.learning_rate]
    outs: [models/history.csv, models/model.h5]
  evaluate:
    cmd: python3 src/evaluate.py
    deps: [data/processed, models/model.h5, src/evaluate.py]
    outs: [reports/confusion_matrix.png]
    metrics: [{metrics.json: {cache: false}}]"""

    yaml_table_data = [
        [
            Paragraph("<b>params.yaml (Hyperparameter Source of Truth)</b>", h2_style),
            Paragraph("<b>dvc.yaml (Reproducible Pipeline Spec)</b>", h2_style)
        ],
        [
            Paragraph(f"<font color='#94A3B8'>{params_content.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", code_style),
            Paragraph(f"<font color='#94A3B8'>{dvc_yaml_content.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", code_style)
        ]
    ]
    t_yaml = Table(yaml_table_data, colWidths=[185, 337])
    t_yaml.setStyle(TableStyle([
        ('BACKGROUND', (0,1), (0,1), code_bg),
        ('BACKGROUND', (1,1), (1,1), code_bg),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,1), (0,1), 1, border_color),
        ('BOX', (1,1), (1,1), 1, border_color),
    ]))
    story.append(t_yaml)
    story.append(Spacer(1, 5))
    
    story.append(Paragraph("Pipeline Execution & Intelligent Caching (D3 vs D4)", h2_style))
    story.append(Paragraph(
        "<b>D3 Reproduction (v1):</b> All four pipeline stages executed chronologically from scratch. DVC computed MD5 content hashes for each artifact and generated <code>dvc.lock</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>D4 Reproduction (v2 - Hyperparameter Modification):</b> When <code>train.dense_units</code> was increased from 128 to 256 in <code>params.yaml</code> and <code>dvc repro</code> was triggered:",
        body_style
    ))
    
    repro_analysis = [
        "<b>Stage 'prepare' SKIPPED:</b> Dependency <code>src/prepare.py</code> and outputs in <code>data/raw/</code> were completely unmodified.",
        "<b>Stage 'preprocess' SKIPPED:</b> Input raw data, code, and preprocess parameters (<code>test_size</code>, <code>seed</code>) remained untouched.",
        "<b>Stage 'train' RE-EXECUTED:</b> DVC detected parameter drift in <code>train.dense_units</code> (128 -> 256), invalidating cached model weights.",
        "<b>Stage 'evaluate' RE-EXECUTED:</b> Automatically triggered because upstream dependency <code>models/model.h5</code> produced a new MD5 hash."
    ]
    for pt in repro_analysis:
        story.append(Paragraph(f"• {pt}", bullet_style))
        
    story.append(Spacer(1, 5))
    story.append(Paragraph("v1 vs v2 Metrics Comparison Table", h2_style))
    metrics_data = [
        ["Model Version", "Dense Units", "Dropout", "Learning Rate", "Epochs", "Test Loss", "Test Accuracy", "Target Met"],
        ["v1 (Initial Pipeline)", "128", "0.20", "0.001", "10", "0.3411", "87.40%", "YES (>= 85%)"],
        ["v2 (Tuned Model)", "256", "0.20", "0.001", "10", "0.3474", "87.81%", "YES (>= 85%)"],
        ["Performance Delta", "+128 units", "--", "--", "--", "+0.0063", "+0.41% (+41 bps)", "OPTIMIZED"]
    ]
    t_metrics = Table(metrics_data, colWidths=[95, 60, 50, 65, 45, 55, 65, 87])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.2),
        ('BACKGROUND', (0,1), (-1,1), colors.white),
        ('BACKGROUND', (0,2), (-1,2), light_bg),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#E6FFFA")),
        ('TEXTCOLOR', (0,3), (-1,3), colors.HexColor("#234E52")),
        ('FONTNAME', (0,3), (-1,3), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('FONTSIZE', (0,1), (-1,-1), 7.2),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_metrics)
    
    story.append(PageBreak())
    
    # ================= PAGE 3 =================
    story.append(Paragraph("Part E — Simulated Collaboration & Conflict Resolution", h1_style))
    story.append(Paragraph(
        "A multi-developer collaboration was simulated across two branches (<code>main</code> and <code>teammate-sim</code>) that independently modified data preprocessing code and regenerated artifacts:",
        body_style
    ))
    
    e_narrative = [
        "<b>1. Code Divergence:</b> On <code>teammate-sim</code>, normalization was altered to zero-centered [-1, 1] (<code>(x - 128)/128</code>). On <code>main</code>, normalization was independently set to Z-score standardization (<code>(x - mean)/std</code>).",
        "<b>2. Data Divergence:</b> Each developer regenerated <code>data/processed/</code>, producing conflicting DVC pointer hashes: <code>31645b...dir</code> on teammate-sim vs <code>dec45f...dir</code> on main.",
        "<b>3. Conflict Collision (E3):</b> Invoking <code>git merge teammate-sim</code> into <code>main</code> resulted in concurrent code conflicts in <code>src/preprocess.py</code> and DVC pointer conflicts in <code>data/processed.dvc</code>."
    ]
    for pt in e_narrative:
        story.append(Paragraph(f"• {pt}", bullet_style))
        
    story.append(Spacer(1, 4))
    
    conflict_img_path = "reports/part_e_conflict_screenshot.png"
    if os.path.exists(conflict_img_path):
        story.append(Image(conflict_img_path, width=515, height=215))
        story.append(Spacer(1, 4))
        
    story.append(Paragraph("Resolution Methodology (E4 & E5)", h2_style))
    res_steps = [
        "<b>Code Conflict Resolution:</b> Reconciled <code>src/preprocess.py</code> by integrating standard bounded scaling [0, 1] with comprehensive validation checks, satisfying both teammate requirements.",
        "<b>Data Conflict Resolution:</b> Selected canonical processed dataset pointer (<code>673bfbf...dir</code>). Executed <code>dvc checkout data/processed.dvc</code> to synchronize local arrays from the local cache.",
        "<b>Validation & Reproduction:</b> Confirmed <code>dvc status</code> reported a clean state, completed the merge commit (<code>git commit</code>), and re-executed <code>dvc repro</code> to verify end-to-end reproducibility from the unified state."
    ]
    for pt in res_steps:
        story.append(Paragraph(f"• {pt}", bullet_style))
        
    story.append(PageBreak())
    
    # ================= PAGE 4 =================
    story.append(Paragraph("Artifacts, Confusion Matrix & Compliance Verification", h1_style))
    story.append(Paragraph(
        "The finalized pipeline produces verifiable, publication-grade machine learning artifacts across the Fashion-MNIST dataset.",
        body_style
    ))
    
    cm_img_path = "reports/confusion_matrix.png"
    if os.path.exists(cm_img_path):
        story.append(Image(cm_img_path, width=420, height=330))
        story.append(Spacer(1, 6))
        
    story.append(Paragraph("Compliance & Deliverables Checklist", h2_style))
    deliverables = [
        ["Deliverable Requirement", "Verification Status", "Details & Location"],
        ["GitHub Repository Link", "CONFIRMED", "https://github.com/Aenonic/fashion-ann-pipeline (Unsquashed history)"],
        ["Full Git Commit History", "CONFIRMED", "All parts A1-A8, B, C, D, E commits preserved with tags v1 & v2."],
        ["DVC Google Drive Remote", "CONFIGURED", "Remote 'gdrive_storage' registered in .dvc/config with OAuth consent."],
        ["DVC Pipeline Reproducibility", "VERIFIED", "Single 'dvc repro' call successfully executes end-to-end pipeline."],
        ["Metrics Requirement (>= 85%)", "EXCEEDED", "Test Accuracy: 87.81% (v2), Test Loss: 0.3474 recorded in metrics.json."],
        ["dvc.lock Version Control", "COMMITTED", "dvc.lock committed at root with all stage dependencies and hash locks."]
    ]
    t_deliv = Table(deliverables, colWidths=[135, 80, 307])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.2),
        ('BACKGROUND', (1,1), (1,-1), colors.HexColor("#E6FFFA")),
        ('TEXTCOLOR', (1,1), (1,-1), colors.HexColor("#234E52")),
        ('FONTNAME', (1,1), (1,-1), 'Helvetica-Bold'),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, border_color),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_deliv)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    create_report()
