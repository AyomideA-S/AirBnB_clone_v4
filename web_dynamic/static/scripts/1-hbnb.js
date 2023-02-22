$(document).ready(function() {
	const selected = []; 
	$('input:checkbox').change(function() {
		if (this.checked) {
			let selected = selected.push(this.data-id);
		} else {
			if (selected.indexOf(this.data-id) >= 0) {
				selected.splice(selected.indexOf(this.data-id), 1);
			}
		}
		document.getElementById("Amenities-selected").innerHTML = selected.join(", ");;
	});
});
