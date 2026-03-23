// Frontend file handling and upload logic

document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const formatBtn = document.getElementById('formatBtn');
    const errorMessage = document.getElementById('errorMessage');
    const progressBar = document.getElementById('progressBar');

    let selectedFile = null;

    // Handle file selection via click
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle file selection via input
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    // Handle drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFileSelect(e.dataTransfer.files[0]);
    });

    // Format button click
    formatBtn.addEventListener('click', handleFormat);

    function handleFileSelect(file) {
        // Validate file type
        if (!file || !file.name.endsWith('.docx')) {
            showError('仅支持.docx格式');
            selectedFile = null;
            formatBtn.disabled = true;
            return;
        }

        // Validate file size (50MB)
        const maxSize = 50 * 1024 * 1024;
        if (file.size > maxSize) {
            showError('文件过大，最多50MB');
            selectedFile = null;
            formatBtn.disabled = true;
            return;
        }

        selectedFile = file;
        errorMessage.style.display = 'none';
        formatBtn.disabled = false;

        // Update UI to show file selected
        uploadArea.querySelector('.upload-text').textContent = `已选择：${file.name}`;
        uploadArea.querySelector('.upload-subtext').textContent = `(${(file.size / 1024 / 1024).toFixed(2)} MB)`;
    }

    function handleFormat() {
        if (!selectedFile) {
            showError('请先选择文件');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        formatBtn.disabled = true;
        progressBar.style.display = 'block';
        errorMessage.style.display = 'none';

        fetch('/format', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || '处理失败');
                });
            }
            return response.blob();
        })
        .then(blob => {
            // Create download link
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${selectedFile.name.replace('.docx', '')}_formatted.docx`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            // Show success
            progressBar.style.display = 'none';
            showSuccess(`文件已排版并下载：${a.download}`);
        })
        .catch(error => {
            progressBar.style.display = 'none';
            showError(error.message || '处理失败，请重试');
            formatBtn.disabled = false;
        });
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.style.backgroundColor = '#fee';
        errorMessage.style.borderColor = '#fcc';
        errorMessage.style.color = '#c33';
    }

    function showSuccess(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.style.backgroundColor = '#efe';
        errorMessage.style.borderColor = '#cfc';
        errorMessage.style.color = '#3c3';
        formatBtn.disabled = false;

        // Reset file selection after 3 seconds
        setTimeout(() => {
            selectedFile = null;
            fileInput.value = '';
            uploadArea.querySelector('.upload-text').textContent = '拖拽或点击选择 Word 文件';
            uploadArea.querySelector('.upload-subtext').textContent = '(支持 .docx 格式，最大 50MB)';
            formatBtn.disabled = true;
            errorMessage.style.display = 'none';
        }, 3000);
    }
});
