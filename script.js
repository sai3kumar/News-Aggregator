function toggleFilterOptions() {
    const filterOptions = document.getElementById('filterOptions');
    filterOptions.style.display = filterOptions.style.display === 'block' ? 'none' : 'block';
}

function filterBy(type) {
    alert(`Filtering by ${type}`);
    // Implement filtering logic here
}
