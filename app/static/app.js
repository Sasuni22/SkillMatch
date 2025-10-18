// drag & drop + upload + animated results
const fileSelect = document.getElementById('fileSelect');
const fileElem = document.getElementById('fileElem');
const dropArea = document.getElementById('drop-area');
const fileNameEl = document.getElementById('file-name');
const uploadBtn = document.getElementById('uploadBtn');
const progress = document.getElementById('progress');
const progressBar = document.getElementById('progress-bar');
const resultsPlaceholder = document.getElementById('results-placeholder');

if (fileSelect) fileSelect.addEventListener('click', () => fileElem.click());
if (fileElem) fileElem.addEventListener('change', handleFiles);

['dragenter','dragover','dragleave','drop'].forEach(ev => {
  if(dropArea) dropArea.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); });
});

if(dropArea){
  ['dragenter','dragover'].forEach(ev => dropArea.addEventListener(ev, () => dropArea.classList.add('bg-light')));
  ['dragleave','drop'].forEach(ev => dropArea.addEventListener(ev, () => dropArea.classList.remove('bg-light')));
  dropArea.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if(files.length){ fileElem.files = files; handleFiles(); }
  });
}

function handleFiles(){
  const file = fileElem.files[0];
  if(!file) return;
  fileNameEl.textContent = file.name + ' • ' + Math.round(file.size/1024) + ' KB';
  uploadBtn.disabled = false;
}

if(uploadBtn) uploadBtn.addEventListener('click', uploadFile);

function uploadFile(){
  const file = fileElem.files[0];
  if(!file) { alert('Choose a PDF first'); return; }

  const formData = new FormData();
  formData.append('resume', file);

  progress.style.display = 'block';
  progressBar.style.width = '0%';

  fetch('/upload', { method: 'POST', body: formData, headers: { 'Accept': 'application/json' } })
    .then(resp => {
      if(!resp.ok) throw new Error('Network response not ok');
      return resp.json();
    })
    .then(data => {
      const matches = data.matches || [];
      let html = `<div class="card p-3 mt-3"><h5 class="text-white">Top Matches</h5><div class="list-group">`;

      if(matches.length === 0) html += `<div class="list-group-item text-white">No matches found.</div>`;

      matches.forEach(m => {
        html += `<div class="list-group-item mb-2 hover-card">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <div class="fw-bold" style="color:black;">${m.title}</div>
                    <div class="fw-bold text-accent">${m.score}%</div>
                  </div>
                  <div class="small text-muted mb-1">${m.description}</div>
                  <div class="progress">
                    <div class="match-bar" style="width:0%; background-color:#fedc75;" data-score="${m.score}"></div>
                  </div>
                </div>`;
      });

      html += `</div></div>`;
      resultsPlaceholder.innerHTML = html;

      // Animate bars
      document.querySelectorAll('.match-bar').forEach(bar => {
        const score = bar.getAttribute('data-score');
        setTimeout(() => bar.style.width = score + '%', 100);
      });

      progressBar.style.width = '100%';
      setTimeout(() => progress.style.display='none', 800);
    })
    .catch(err => { 
      console.error(err); 
      alert('Upload failed or server error.'); 
      progress.style.display='none'; 
    });
}
