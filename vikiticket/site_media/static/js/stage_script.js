var v_pl_num = 0;
var v_pl_cont = ',';

function v_handle_place() {

	// Free seats are handeled
	$('.f').click(function() {
		var place_id = $(this).attr('id');
		place_id = place_id.replace('seat_', '');

		// If text already in v_pl_cont
		if (v_pl_cont.indexOf(place_id) != -1) {
			v_pl_cont = v_pl_cont.replace(',' + place_id + ',', ',');
			v_pl_num = v_pl_num - 1;
			$(this).attr('class', 'seat f');
			title = $(this).attr('title');
			$(this).attr('title', '');
		}
		else {
			if (v_pl_num < 5) {
				v_pl_cont = v_pl_cont + place_id + ',';
				v_pl_num = v_pl_num + 1;
				$(this).attr('class', 'seat o');
				title = $(this).attr('title');
				if (title != undefined) {
					$(this).attr('title', title + '. Выбран для заказа.');
				}
				else {
					$(this).attr('title', 'Выбран для заказа.');
				}
			}
		}
		if (v_pl_cont == ',') {
			$('#id_seats').val('');
		}
		else {
			// Update form field value
			$('#id_seats').val(v_pl_cont);
		}
	});
}

function v_init_places() {
	places = $('#id_seats').val();
	if (places.length > 0) {
			var pl_list = places.split(',');
			
			for (i=1;i<places.length - 1;i++) {
				var seat = $('#seat_' + pl_list[i]);
				var seat_class = seat.attr('class');
				if ((seat_class == 'seat f') || (seat_class == 'seat o')) {
					$('#seat_' + pl_list[i]).trigger('click');
				}
				else {
					places = places.replace(',' + pl_list[i] + ',', ',');
					// Update form field value
					if (places == ',') {
						$('#id_seats').val('');
					}
					else {
						$('#id_seats').val(places);
					}
				}
			}
	}
}

$(document).ready(function() {
	v_handle_place();
	v_init_places();
	// Tooltip initialization
    l_tooltip(".seat","tooltip");
});