document.addEventListener('DOMContentLoaded', function() {

    // Feature 1: Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.transition = 'opacity 0.5s ease';
                msg.style.opacity = '0';
                setTimeout(() => msg.style.display = 'none', 500);
            });
        }, 5000);
    }

    // Feature 2: A reusable function for live table filtering
    const setupTableFilter = (inputId, tableId) => {
        const searchInput = document.getElementById(inputId);
        const table = document.getElementById(tableId);
        if (!searchInput || !table) return;

        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toUpperCase();
            const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

            for (let i = 0; i < rows.length; i++) {
                const rowData = rows[i].textContent || rows[i].innerText;
                if (rowData.toUpperCase().indexOf(filter) > -1) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
        });
    };

    // Apply the filter function to all relevant tables
    setupTableFilter('item-search', 'items-table');
    setupTableFilter('stock-search', 'stock-table');
    setupTableFilter('order-search', 'orders-table');

    // Feature 3: Click-to-Edit functionality
    document.body.addEventListener('click', function(event) {
        if (event.target.classList.contains('btn-edit')) {
            const button = event.target;
            const row = button.closest('tr');
            const formId = button.dataset.form;
            const form = document.getElementById(formId);

            if (row && form) {
                // Populate form fields based on data attributes from the table row
                const inputs = form.querySelectorAll('input, select');
                inputs.forEach(input => {
                    const attrName = input.name.toLowerCase();
                    if (row.dataset[attrName] !== undefined) {
                        input.value = row.dataset[attrName];
                    }
                });
                
                // Scroll to the form for better UX
                form.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });

});