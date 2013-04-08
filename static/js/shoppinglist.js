// List handling
function showDeleteButton(currentDiv)
{
	var deleteBtn = document.createElement("button");
	deleteBtn.appendChild(document.createTextNode("delete"));
	deleteBtn.className += ("delete-btn btn btn-danger btn-small");
	deleteBtn.style = "btn";
	deleteBtn.style.position = "absolute";
	deleteBtn.style.right = "6px";
	currentDiv.appendChild(deleteBtn);
	deleteBtn.style.top = (currentDiv.clientHeight - deleteBtn.clientHeight) / 2 + "px";
	deleteBtn.style.opacity = 1;
}

function hideDeleteButton(currentDiv)
{
	var deleteBtn = $(currentDiv).children(".delete-btn")[0];
    //deleteBtn.style.opacity = 0;
	//transform(deleteBtn, "translate3d(20px,0,0)"); // use 3d for hardware acceleration
	currentDiv.removeChild(deleteBtn);
}

function transform(deleteBtn, style) {
	deleteBtn.style.transform = style;
	deleteBtn.style.webkitTransform = style;
	deleteBtn.style.mozTransform = style;
	deleteBtn.style.oTransform = style;
	}

$(function() {
    $( "#sortable" ).sortable({
		tolerance: 'pointer',
		handle: '.icon-align-justify',
			axis: 'y',
			delay: 100,
			distance: 10
    });
    $( "#sortable" ).disableSelection();
});

function swipeRight(e) {
	var currentDiv = e.target;
	if (currentDiv.localName != "div") {
		currentDiv = e.target.firstChild;
	}
	var button = $(".delete-btn");
	if (button.length === 0) {
		showDeleteButton(currentDiv);
	} else {
		var buttonDiv = button[0].parentNode;
		hideDeleteButton(buttonDiv);
		if (buttonDiv != currentDiv) {
			showDeleteButton(currentDiv);
		}
	}
}

$(document).ready(function() {
	var listItems = document.getElementById('sortable').getElementsByTagName('li');
	for (var i = 0; i < listItems.length; ++i) {
		Hammer(listItems[i], {
			swipe_velocity : 0.2
		}).on("swiperight", swipeRight);
	}
});

// Form handling
$(function() {
	var modalShown = false;
	$('#modal-list-item').on('shown', function () {
		modalShown = true;
		$('#product-query').focus();
	});
	$('#modal-list-item').on('hidden', function () {
		modalShown = false;
		$('#product-query').val('');
	});
	$('#modal-form').on('submit', function(e) {
		$.ajax({
			url: '/Lists/{{ list_id }}',
			type: 'POST',
			data: {description: $('#product-query').val(), quantity: $('#quantity').val()}
		});
	});
	$('#modal-form-submit').on('click', function(e){
		e.preventDefault();
		$('#modal-form').submit();
	});

	$("#product-query").typeahead({
		minLength: 1,
		source: function(query, process) {
			$.get('/Products', { q: query.toLowerCase() }, function(data) {
				var newData = [];
				$.each(data, function(){
					newData.push(this.name);
				});
				process(newData);
			});
		}
	});

	$(document).keypress(function(e){
		e = window.event || e;
		if (String.fromCharCode(e.charCode) == 'a') {
			$('#modal-list-item').modal();
		}
		if (e.charCode == 13) {
			if (modalShown) {
				$('#modal-form').submit();
				$('#modal-list-item').modal('hide');
			}
		}
	});
});
