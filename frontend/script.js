document.getElementById('process-text').addEventListener('click', function() {
    const inputText = document.getElementById('input-text').value;
    const addErrors = document.getElementById('add-errors').checked;
    const keepProfessional = document.getElementById('keep-professional').checked;
    const vocabularyLevel = document.getElementById('vocabulary-level').value;

    if (!inputText.trim()) {
        alert('Please enter some text to process.');
        return;
    }

    const requestData = {
        text: inputText,
        options: {
            addErrors,
            keepProfessional,
            vocabularyLevel
        }
    };

    // Show loading indicator
    document.getElementById('output-text').value = 'Processing...';

    fetch('http://localhost:5000/api/process-text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading indicator and show the processed text
        document.getElementById('output-text').value = data.modifiedText;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('output-text').value = 'An error occurred while processing the text.';
    });
});
