function check_radio_button() {
    var id_onsite= document.getElementById('id_onsite_0');
    var id_offsite = document.getElementById('id_onsite_1');
    var id_offsite_textfield = document.getElementById('id_offsite');
				
	if (id_onsite.checked == true) {
    		id_offsite_textfield.setAttribute('disabled', 'disabled');
    		id_offsite_textfield.removeAttribute('name');
    	}
    	if (id_offsite.checked == true) {
    		id_offsite_textfield.removeAttribute('disabled', 'disabled');
    		id_offsite_textfield.setAttribute('name', 'offsite');
    		}			
    	}
//eof
