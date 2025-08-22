function startEdit(taskId) {
    // Hide the task info and show the edit form
    document.getElementById(`title-${taskId}`).style.display = 'none';
    document.getElementById(`edit-form-${taskId}`).style.display = 'flex';
    
    // Focus on the input field
    const input = document.querySelector(`#edit-form-${taskId} input[name="title"]`);
    input.focus();
    input.select();
}

function cancelEdit(taskId) {
    // Show the task info and hide the edit form
    document.getElementById(`title-${taskId}`).style.display = 'flex';
    document.getElementById(`edit-form-${taskId}`).style.display = 'none';
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Escape key cancels all edits
    if (event.key === 'Escape') {
        const editForms = document.querySelectorAll('.edit-form[style*="flex"]');
        editForms.forEach(form => {
            const taskId = form.id.replace('edit-form-', '');
            cancelEdit(taskId);
        });
    }
});