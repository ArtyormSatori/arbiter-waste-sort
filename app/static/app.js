document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('file-input');
  const cameraInput = document.getElementById('camera-input');
  const dropzonePrompt = document.getElementById('dropzone-prompt');
  const previewWrapper = document.getElementById('image-preview-wrapper');
  const imagePreview = document.getElementById('image-preview');
  const btnClear = document.getElementById('btn-clear');
  const inferenceStatus = document.getElementById('inference-status');

  const emptyState = document.getElementById('empty-state');
  const resultContent = document.getElementById('result-content');
  const latencyBadge = document.getElementById('latency-badge');

  const categoryBanner = document.getElementById('category-banner');
  const resCategory = document.getElementById('res-category');
  const resDetectedItem = document.getElementById('res-detected-item');
  const resConfidence = document.getElementById('res-confidence');
  const binSwatch = document.getElementById('bin-swatch');
  const resBinName = document.getElementById('res-bin-name');
  const resWhyParagraph = document.getElementById('res-why-paragraph');
  const resPrepList = document.getElementById('res-prep-list');
  const resImpactText = document.getElementById('res-impact-text');
  const probBars = document.getElementById('prob-bars');

  const sampleChips = document.getElementById('sample-chips');
  const benchmarkToggle = document.getElementById('benchmark-toggle');
  const benchmarkDetails = document.getElementById('benchmark-details');
  const benchmarkTbody = document.getElementById('benchmark-tbody');

  // Drag and Drop
  ['dragenter', 'dragover'].forEach(name => {
    dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(name => {
    dropzone.addEventListener(name, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove('dragover');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleImageFile(files[0]);
    }
  });

  // Inputs
  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleImageFile(e.target.files[0]);
    }
  });

  cameraInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleImageFile(e.target.files[0]);
    }
  });

  btnClear.addEventListener('click', (e) => {
    e.stopPropagation();
    resetState();
  });

  // Sample Chips
  sampleChips.addEventListener('click', async (e) => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    const sampleFilename = chip.getAttribute('data-sample');
    if (!sampleFilename) return;

    showStatus("Fetching sample image and running inference...");
    try {
      const response = await fetch(`/api/sample-image/${sampleFilename}`);
      if (!response.ok) throw new Error("Could not fetch sample");
      const blob = await response.blob();
      const file = new File([blob], sampleFilename, { type: 'image/jpeg' });
      handleImageFile(file);
    } catch (err) {
      alert(`Error loading sample: ${err.message}`);
      hideStatus();
    }
  });

  // Benchmark Accordion
  benchmarkToggle.addEventListener('click', () => {
    benchmarkDetails.classList.toggle('hidden');
    if (!benchmarkDetails.classList.contains('hidden') && benchmarkTbody.children.length === 0) {
      loadBenchmarkData();
    }
  });

  // Main file handler
  function handleImageFile(file) {
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file (JPEG, PNG, WebP).');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
      dropzonePrompt.classList.add('hidden');
      previewWrapper.classList.remove('hidden');
    };
    reader.readAsDataURL(file);

    classifyImage(file);
  }

  async function classifyImage(file) {
    showStatus("Extracting visual features via Vision Transformer...");
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/classify', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Server error: ${res.status}`);
      }

      const data = await res.json();
      renderResults(data);
    } catch (err) {
      console.error(err);
      alert(`Classification failed: ${err.message}`);
    } finally {
      hideStatus();
    }
  }

  function renderResults(data) {
    const primary = data.primary_result;

    emptyState.classList.add('hidden');
    resultContent.classList.remove('hidden');
    latencyBadge.classList.remove('hidden');
    latencyBadge.textContent = `Latency: ${data.inference_time_ms.toFixed(0)} ms`;

    // Category banner colors
    const cat = primary.category.toLowerCase();
    let bannerBg = 'linear-gradient(135deg, #1e3a8a, #1d4ed8)';
    let bannerBorder = '#3b82f6';
    if (cat === 'organic') {
      bannerBg = 'linear-gradient(135deg, #065f46, #059669)';
      bannerBorder = '#10b981';
    } else if (cat === 'hazardous') {
      bannerBg = 'linear-gradient(135deg, #991b1b, #dc2626)';
      bannerBorder = '#ef4444';
    } else if (cat === 'non-recyclable') {
      bannerBg = 'linear-gradient(135deg, #374151, #4b5563)';
      bannerBorder = '#6b7280';
    }

    categoryBanner.style.background = bannerBg;
    categoryBanner.style.borderColor = bannerBorder;

    resCategory.textContent = primary.category_display;
    resDetectedItem.textContent = primary.detected_item;
    resConfidence.textContent = `${Math.round(primary.confidence * 100)}%`;

    // Bin Info
    binSwatch.style.backgroundColor = primary.bin_color_code;
    resBinName.textContent = primary.bin_name;

    // Why paragraph
    resWhyParagraph.textContent = primary.why_paragraph;

    // Prep Checklist
    resPrepList.innerHTML = '';
    primary.preparation_tips.forEach(tip => {
      const li = document.createElement('li');
      li.textContent = tip;
      resPrepList.appendChild(li);
    });

    // Environmental Impact
    resImpactText.textContent = primary.environmental_impact;

    // Probability Bars
    probBars.innerHTML = '';
    const alternatives = data.alternative_predictions.slice(0, 4);
    alternatives.forEach(alt => {
      const pct = Math.round(alt.score * 100);
      const row = document.createElement('div');
      row.className = 'prob-row';
      row.innerHTML = `
        <span class="prob-label">${alt.label}</span>
        <div class="prob-track">
          <div class="prob-fill" style="width: ${pct}%; background-color: ${primary.category === alt.category ? primary.bin_color_code : '#64748b'};"></div>
        </div>
        <span class="prob-val">${pct}%</span>
      `;
      probBars.appendChild(row);
    });
  }

  function resetState() {
    fileInput.value = '';
    cameraInput.value = '';
    imagePreview.src = '';
    previewWrapper.classList.add('hidden');
    dropzonePrompt.classList.remove('hidden');
    emptyState.classList.remove('hidden');
    resultContent.classList.add('hidden');
    latencyBadge.classList.add('hidden');
  }

  function showStatus(msg) {
    inferenceStatus.querySelector('span').textContent = msg;
    inferenceStatus.classList.remove('hidden');
  }

  function hideStatus() {
    inferenceStatus.classList.add('hidden');
  }

  async function loadBenchmarkData() {
    try {
      const res = await fetch('/api/benchmark');
      if (!res.ok) return;
      const data = await res.json();
      
      benchmarkTbody.innerHTML = '';
      data.details.forEach(item => {
        const tr = document.createElement('tr');
        const pass = item.category_match;
        tr.innerHTML = `
          <td><code>${item.file}</code></td>
          <td><strong>${item.ground_truth_category}</strong> (${item.ground_truth_label})</td>
          <td>${item.predicted_category}</td>
          <td>${item.predicted_label}</td>
          <td>${Math.round(item.confidence * 100)}%</td>
          <td>
            <span class="${pass ? 'status-badge-pass' : 'status-badge-fail'}">
              ${pass ? '✓ MATCH' : '✗ MISMATCH'}
            </span>
          </td>
        `;
        benchmarkTbody.appendChild(tr);
      });
    } catch (err) {
      console.error("Failed to load benchmark table:", err);
    }
  }

  // Pre-load benchmark on startup
  loadBenchmarkData();
});
