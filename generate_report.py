from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
    PageBreak, KeepTogether, Preformatted,
)

ROOT = Path('/Users/avcton/Documents/Sw/fashion-ann-pipeline')
OUT = Path('/Users/avcton/Documents/Codex/2026-10-04/se/outputs/Fashion_ANN_Pipeline_Report_Corrected.pdf')
OUT.parent.mkdir(parents=True, exist_ok=True)
GITHUB_URL = 'https://github.com/Aenonic/fashion-ann-pipeline'
DRIVE_URL = 'https://drive.google.com/drive/u/0/folders/1A4889YAEgPAiFNWejJkhAuGMXrLowjNe'

NAVY = colors.HexColor('#17365D')
BLUE = colors.HexColor('#2E75B6')
PALE = colors.HexColor('#EAF2F8')
GREEN = colors.HexColor('#DFF2E1')
AMBER = colors.HexColor('#FFF2CC')
RED = colors.HexColor('#FCE4D6')
INK = colors.HexColor('#1F2937')
MUTED = colors.HexColor('#526273')

styles = getSampleStyleSheet()
title = ParagraphStyle('Title2', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=18, leading=21, textColor=NAVY, alignment=TA_CENTER, spaceAfter=5)
sub = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=BLUE, spaceAfter=8)
h1 = ParagraphStyle('H1x', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=5, spaceAfter=4)
h2 = ParagraphStyle('H2x', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=BLUE, spaceBefore=3, spaceAfter=2)
body = ParagraphStyle('Bodyx', parent=styles['BodyText'], fontSize=7.2, leading=9.1, textColor=INK, spaceAfter=3)
small = ParagraphStyle('Smallx', parent=body, fontSize=6.3, leading=7.7)
code = ParagraphStyle('Codex', parent=styles['Code'], fontName='Courier', fontSize=5.5, leading=6.8, textColor=colors.HexColor('#172033'), backColor=colors.HexColor('#EEF3F8'), borderColor=colors.HexColor('#B7C5D3'), borderWidth=0.4, borderPadding=6, spaceAfter=4)

def P(txt, style=body):
    return Paragraph(txt, style)

def T(rows, widths, header=True, font=6.1):
    converted = [[c if hasattr(c, 'wrap') else P(str(c), small) for c in row] for row in rows]
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign='LEFT')
    cmds = [('VALIGN',(0,0),(-1,-1),'TOP'), ('GRID',(0,0),(-1,-1),0.35,colors.HexColor('#AAB7C4')), ('LEFTPADDING',(0,0),(-1,-1),3), ('RIGHTPADDING',(0,0),(-1,-1),3), ('TOPPADDING',(0,0),(-1,-1),2), ('BOTTOMPADDING',(0,0),(-1,-1),2)]
    if header:
        cmds += [('BACKGROUND',(0,0),(-1,0),NAVY), ('TEXTCOLOR',(0,0),(-1,0),colors.white), ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold')]
    for i in range(1 if header else 0, len(rows)):
        if i % 2 == 0: cmds.append(('BACKGROUND',(0,i),(-1,i),colors.HexColor('#F5F8FA')))
    t.setStyle(TableStyle(cmds))
    return t

def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#D4DEE8')); canvas.line(36,29,576,29)
    canvas.setFillColor(BLUE); canvas.setFont('Helvetica',6.5)
    footer_text = 'GitHub: github.com/Aenonic/fashion-ann-pipeline'
    canvas.drawString(36,18,footer_text)
    canvas.linkURL(GITHUB_URL, (36,15,36 + canvas.stringWidth(footer_text,'Helvetica',6.5),24), relative=0)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(576,18,f'Page {doc.page} of 4'); canvas.restoreState()

def run_text(path):
    return (ROOT/path).read_text().strip()

params = run_text('params.yaml')
dvc_yaml = run_text('dvc.yaml')

story = [P('Assignment 2: End-to-End ML Versioning', title), P('Evidence-based final report - Git, DVC, Google Drive and Fashion-MNIST ANN', sub)]
story += [T([
    ['Student','Zainab Fatima','Repository',P(f'<link href="{GITHUB_URL}" color="#2E75B6"><u>github.com/Aenonic/fashion-ann-pipeline</u></link>', small)],
    ['Dataset','Fashion-MNIST (70,000 images)','Final model','Dense 256, 10 epochs'],
    ['Final result','Accuracy 87.81% / loss 0.3474','Audit date','4 October 2026'],
], [0.75*inch,1.75*inch,0.8*inch,3.95*inch], header=False)]
story += [P('Part A - Git Fundamentals and Advanced Commands', h1), P('The repository has an unsquashed history. The reflog independently preserves the destructive-history exercises (soft/hard reset) and the completed rebase; the merge commit preserves the Part E conflict resolution.', body)]
story += [T([
    ['Requirement','Verified evidence','Meaning'],
    ['A1-A2','Initial commit d21ef1b on main; dev branch created; 9 incremental Part B-D commits before v2.','Branch isolation and incremental history are present.'],
    ['A3 log variants','<b>--oneline --graph --all</b>: topology; <b>--stat -3</b>: recent file counts; <b>-p -1</b>: exact patch; <b>main..dev</b>: commits reachable only from dev.','Each exposes structure or change detail omitted by plain log.'],
    ['A4 diff variants','<b>git diff</b>: unstaged; <b>--staged</b>: index; <b>main..dev</b>: tip-to-tip; <b>main...dev</b>: merge-base-to-dev.','Two-dot includes both tips; three-dot isolates the dev-side work since divergence.'],
    ['A5 stash','Workflow documented: stash push -u, stash list, branch switch, stash pop.','The report records the required sequence; no stash entry remains after pop.'],
    ['A6 rebase','Reflog: rebase started onto hotfix 570787f and finished with dev at 6e78009.','Dev was replayed on top of updated main.'],
    ['A7 reset','Reflog records soft reset and hard reset on scratch-reset-demo; branch ends at Throwaway commit 1.','Soft retained staged changes; hard discarded commit and worktree changes.'],
    ['A8 mv/rm','Commits 7e2b603 and 6e78009 retain preparation and reorganization events.','Tracked move/removal history is retained.'],
], [0.85*inch,3.15*inch,3.25*inch])]
story += [P('Representative command evidence', h2), Preformatted("""$ git log --oneline --graph --all
* 932d0d5 (HEAD -> main, origin/main) Docs: update report / Drive remote
* f3fe902 Docs: add PDF report and generator
* d76cdaf E5: pipeline reproducible from merged state
*   dcc7948 E5: resolve code and DVC data conflicts
| * c7c77ec (teammate-sim) E1: normalization [-1,1]
* | 49a91eb E2: main Z-score normalization
|/
* b81c629 (tag: v2, dev) D5: dense_units=256, accuracy=0.8781
* faac07e (tag: v1) D3: dense_units=128, accuracy=0.8740

$ git reflog --all | evidence summary
6e78009 rebase (finish) onto 570787f
fa5cd83 -> d5399cf reset HEAD~1 (soft demonstration)
fa9b02b -> d5399cf reset HEAD~1 (hard demonstration)""", code), PageBreak()]

story += [P('Part B - Modular TensorFlow ANN Pipeline', h1)]
story += [T([
    ['Script','Inputs','Outputs / verified behavior'],
    ['src/prepare.py','tf.keras Fashion-MNIST','Four raw .npy arrays; 60k training and 10k test examples.'],
    ['src/preprocess.py','raw arrays, params.yaml','Float32 [0,1] scaling; stratified 20% validation split; six processed arrays.'],
    ['src/train.py','processed arrays, train params','Flatten -> Dense(ReLU) -> Dropout -> Dense(10, Softmax); Adam; model.h5 and history.csv.'],
    ['src/evaluate.py','model + processed test set','Loss/accuracy in metrics.json and labeled confusion matrix PNG.'],
], [1.15*inch,1.75*inch,4.35*inch])]
story += [P('Part D - Reproducible DVC pipeline', h1)]
story += [Table([[P('params.yaml',h2),P('dvc.yaml',h2)],[Preformatted(params,code),Preformatted(dvc_yaml,code)]], colWidths=[2.15*inch,5.1*inch], style=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2)])]
story += [P('D3/D4 execution and caching', h2), P('At v1 (tag faac07e), a clean reproduction created dvc.lock with dense_units=128 and test accuracy 0.8740. For v2 (tag b81c629), only <b>train</b> and downstream <b>evaluate</b> were invalidated by dense_units 128 -> 256; prepare and preprocess remained cached because their dependencies and parameters did not change.', body)]
story += [T([
    ['Version','Dense','Dropout','LR','Epochs','Loss','Accuracy','Target'],
    ['v1','128','0.20','0.001','10','0.3411','87.40%','Met'],
    ['v2','256','0.20','0.001','10','0.3474','87.81%','Met'],
    ['Delta','+128','-','-','-','+0.0063','+0.41 pp','Met'],
], [0.75*inch,0.55*inch,0.65*inch,0.6*inch,0.55*inch,0.65*inch,0.75*inch,0.65*inch])]
story += [P('Current lock-file evidence', h2), Preformatted("""prepare      raw hash 585a7ccf...dir
preprocess   processed hash 673bfbf0...dir (test_size=0.2, seed=42)
train        model hash bf4f29dc... (dense_units=256)
evaluate     metrics hash 94391a7f...; confusion matrix hash 3469b359...
metrics.json test_accuracy=0.87809998, test_loss=0.34735397""", code), PageBreak()]

story += [P('Part C - DVC Setup and Google Drive Remote', h1), P(f'DVC is initialized and the default remote is configured as <b>gdrive_storage</b>. <link href="{DRIVE_URL}" color="#2E75B6"><u>Open the Google Drive DVC folder</u></link> (folder ID: <b>1A4889YAEgPAiFNWejJkhAuGMXrLowjNe</b>). A dedicated Google Cloud desktop OAuth client was authorized without committing credentials to Git. The final <b>dvc push</b> uploaded 14 files, <b>dvc status -c</b> reported the cache and remote in sync, and the supplied Drive folder visibly contains the DVC <b>files</b> directory.', body)]
story += [T([
    ['Check','Status','Evidence / required action'],
    ['DVC initialized','Verified','.dvc exists and dvc version identifies the repository.'],
    ['Default Drive remote','Verified','.dvc/config points to the supplied Drive folder ID.'],
    ['Credentials excluded','Verified','.gitignore excludes credentials.json, client_secrets.json, token.json and token patterns.'],
    ['dvc push','Verified','Completed successfully: 14 files pushed.'],
    ['Drive contents','Verified','Google Drive shows the DVC files directory; remote status is in sync.'],
    ['Instructor sharing','User action required','Share the folder with the instructor account if it is not already shared.'],
], [1.45*inch,1.15*inch,4.65*inch])]
story += [P('Part E - Simulated Collaboration and Conflict Resolution', h1), P('The conflict is genuine: teammate-sim used zero-centered [-1,1] scaling while main independently used Z-score normalization. Both branches regenerated data/processed, yielding different DVC hashes. Merge commit dcc7948 reconciled the code to canonical [0,1] scaling and selected regenerated processed hash 673bfbf0...dir; d76cdaf then recorded the reproducible final state.', body)]
conf = ROOT/'reports/part_e_conflict_screenshot.png'
if conf.exists(): story += [Image(str(conf), width=7.05*inch, height=2.55*inch)]
story += [P('Conflict evidence: Git markers are visible in both src/preprocess.py and data/processed.dvc. The final merge commit has two parents (49a91eb and c7c77ec), and the working source no longer contains conflict markers.', small), PageBreak()]

story += [P('Final Artifacts and Compliance Audit', h1)]
cm = ROOT/'reports/confusion_matrix.png'
if cm.exists(): story += [Image(str(cm), width=4.8*inch, height=3.84*inch)]
story += [P('The confusion matrix corresponds to the v2 test accuracy of 87.81%. The weakest class separation is Shirt versus visually similar upper-body categories; this is expected for a fully connected ANN and does not affect the assignment threshold.', small)]
story += [P('Submission checklist', h2), T([
    ['Deliverable','Status','Notes'],
    ['GitHub repository + unsquashed history','Verified','origin/main is synchronized; v1/v2 and collaboration branches exist remotely.'],
    ['Four standalone pipeline scripts','Verified','All required scripts and model architecture are present.'],
    ['params.yaml + dvc.yaml + dvc.lock','Verified','Four stages are wired; final lock is committed.'],
    ['Accuracy >= 85%','Verified','v2 accuracy 87.81%.'],
    ['Google Drive DVC objects','Verified','14 files pushed; cache and gdrive_storage are in sync.'],
    ['Instructor Drive access','User action required','Share the Drive folder with the instructor account.'],
    ['Report accuracy','Corrected','Repository, metrics, upload, and Drive evidence were cross-checked.'],
], [2.15*inch,1.25*inch,3.85*inch])]
story += [Spacer(1,5), P('<b>Final conclusion.</b> The Git history, ANN implementation, DVC pipeline definition, lock file, metrics, tags, conflict-resolution history, Google Drive upload, and remote synchronization meet the technical requirements. The only remaining submission-side check is to ensure the supplied Drive folder is shared with the instructor account.', body)]

doc = SimpleDocTemplate(str(OUT), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=34, bottomMargin=36, title='Assignment 2 - Fashion ANN Pipeline Report', author='Zainab Fatima')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
