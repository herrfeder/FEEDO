
function set_form_value(form_key_id,form_type_id,form_parent_id,form_ptype_id,form_url_id) {
	var temp_html = document.getElementById("id_right_click_info").innerHTML;
	var iframe_url = return_iframe_url();

	$(form_key_id).val($("#id_right_click_info").attr("elementattr"));
	$(form_type_id).val($("#id_right_click_info").attr("elementtype"));
	$(form_url_id).val(iframe_url);
	$(form_parent_id).val($("#id_right_click_info").attr("parentattr"));
	$(form_ptype_id).val($("#id_right_click_info").attr("parenttype"));
	

	
	/* var temp_type = document.getElementById(form_type_id);

	for (i=0; i < temp_type.options.length; i++) {
		var regres = temp_html.search('^&lt;'+temp_type.options[i].value);
		if (regres==0) {
			temp_type.value = temp_type.options[i].value;
		}
	
	} */

};

function return_dom_element(element) {
	var result_string = "";
	
	for (i=0; i< element.attributes.length;i++) {
		result_string+= element.attributes[i].localName+" ";
	}

	var dom_element = element.tagName.toLowerCase();

	return [result_string,dom_element];

}


function serialize_class_list(class_list) {
	var i = 0;
	var result_str = "";
	while(class_list[i] != undefined) {
		result_str = result_str + class_list[i] + " ";
		i = i + 1;
	}
	return result_str;
}

function return_dom_parent(element) {
	var result_string = "";
        el_parent = element;
	while ( ( el_parent.attributes.length == 0 ) || ( !el_parent.attributes.class && !el_parent.attributes.id )) {
		console.log("Parent:"+el_parent);
		el_parent = el_parent.parentElement;
	}
	
	if (el_parent.id) {
		result_string += "id:"+el_parent.id+"&";
	}
	if (el_parent.classList[0]) {
		ser_class = serialize_class_list(el_parent.classList);
		result_string += "class:"+ser_class;
	}

	var dom_element = el_parent.tagName.toLowerCase();

	return [result_string,dom_element] ;

}

function return_iframe_url() {
	
	var full_url = document.getElementById("id_iframe_external_site").contentWindow.location.href;
	full_url = full_url.split("http://127.0.0.1:8000/static/")[1].split("no_js")[1].split(".html")[0];
	return full_url;
};

function check_and_return_href(element) {
	var temp_element = element.target;
	console.log("Temp_element_on_first:"+temp_element);
	if (temp_element.href) {

	console.log("Temp_element_first_return:"+temp_element);
		return String(temp_element.href);
	} else {

		console.log("Temp_element_on_first:"+temp_element);
		new_element = element.target;
		while (	!temp_element.href ) {
			temp_element = temp_element.parentElement;

			if ( temp_element.nodeName == "HTML" ) {
				console.log("reached top element, return false")
				return false;
			}
		}
		return String(temp_element.href);
	}
};

function load_proxy_site(siteurl,clicked_element) {
	console.log("Clicked Element"+clicked_element)
	if (clicked_element != undefined) {
	       clicked_html =  clicked_element.outerHTML;
	} else {
		clicked_html = "0";
	};
	set_status("Init proxy for getting website");
	$.ajax({
		type: 'POST',
		url: '/rss/createfeed/ajax/loadproxysite/',
		data: {siteurl:siteurl,
		       clicked_html:clicked_html,
		       csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
		datatype: 'json',
		success: function(data) {
			if (data.filename) {

				$("#id_iframe_external_site").attr('src', '/static/'+data.filename); 
				set_status("Loaded sucessfully");
				$("#id_iframe_history").html(parse_dict_to_html(data.click_dict));
				$("#id_feed_link").val = data.siteurl;
				console.log(data.filename);

			}
		}		
	})
};

function set_status(status_string) {
	$("#id_status_ajax_load").val( $("#id_status_ajax_load").val() + "\n" + status_string);
};

function parse_dict_to_html(click_history) {
	click_object_array = "";
	var i = 0;

	var table$ = $('<table id="id_history_table" />');

	var click_object = eval(click_history);
	click_object_array = $.map(click_object, function(value, index) {
			return [value];
	});
	console.log("Evaluated_Click_object:"+click_object);
	while (click_object[i] != undefined) {
		var row$ = $('<tr/>');
		row$.append($('<td/>').html('<a href="" id="id_history_'+i+'" ><li>'+i+'</li></a>'));
		for (j=0; j < 1; j++) {
			row$.append($('<td/>').html(click_object[i][j]));
		}
		i++;
		table$.append(row$);
	}
	size_history_table = i;
	
	return table$
};

function delete_click_object_elements(index) {
	var i = index;
	while (click_object[i] == undefined ) {
		delete click_object[i];
		i++;
	}
};

$(document).ready( function() {

	size_history_table = 0;	
	for (i=0;i<=size_history_table;i++) {
		$("#id_history_"+i).click(function(e) {
			e.preventDefault();
			console.log("Click_history:"+e.target);
			delete_click_object_elements(i);
			parse_dict_to_html(click_object);
			$("#id_iframe_external_site").attr('src', '/static/'+click_object[i][1]);
		})
	};

	$("#id_add_title").click(function() {
		set_form_value("#id_title_dom_key","#id_title_dom_type","#id_title_dom_parent","#id_title_dom_ptype","#id_title_dom_url");
	});

	$("#id_add_desc").click(function() {
		console.log("Clicked desc");
		set_form_value("#id_desc_dom_key","#id_desc_dom_type","#id_desc_dom_parent","#id_desc_dom_ptype","#id_desc_dom_url");
	});

	$("#id_add_link").click(function() {
		set_form_value("#id_link_dom_key","#id_link_dom_type","#id_link_dom_parent","#id_link_dom_ptype","#id_link_dom_url");
	});

	$("#id_add_img").click(function() {
		console.log("Clicked img");
		set_form_value("#id_img_dom_key","#id_img_dom_type","#id_img_dom_parent","#id_img_dom_ptype","#id_img_dom_url");
	});

	$("#id_load_website_inp").change(function () {
			siteurl = $(this).val();
			console.log(siteurl);
	});

	$("#id_load_website_btn").click(function () {
		load_proxy_site(siteurl);				
	});
	$("#id_iframe_external_site").on('load', function() {
		console.log("is_loaded");
		$("#id_iframe_external_site").contents().find("body").click(function(e) {
			e.preventDefault();

			console.log("Iframe_clicked:"+e.target);
		        event_element = e;	
			var temp_url = check_and_return_href(e);
			console.log("Found_url:"+temp_url);
			if (temp_url.match(/127.0.0.1:8000\/static\//g)) {
			
				temp_url = click_object_array[click_object_array.length-1]+e.target.href.split("127.0.0.1:8000/static")[1];
				console.log("Temp_url:"+temp_url);
				};
			load_proxy_site(temp_url, e.target);
		});

		$("#id_iframe_external_site").contents().find("body").contextmenu(function(e) {				
			e.preventDefault();
			console.log("e.target.outerHTML:"+e.target.outerHTML);
			$("#id_right_click_info").text(e.target.outerHTML);
			
			ownvalue = e.target;
			var parentvalue = return_dom_parent(e.target);
			var elementvalue = return_dom_element(e.target);
			$("#id_right_click_info").attr("parentattr",parentvalue[0]);
			$("#id_right_click_info").attr("parenttype",parentvalue[1]);
			$("#id_right_click_info").attr("elementattr",elementvalue[0]);
			$("#id_right_click_info").attr("elementtype",elementvalue[1]);


			var menu = $('.menu'); 
			       //hide menu if already shown
			       menu.hide(); 
			       
			       //get x and y values of the click event
			       var pageX = e.pageX;
			       var pageY = e.pageY;

			       //position menu div near mouse cliked area


			       var mwidth = menu.width();
			       var mheight = menu.height();
			       var screenWidth = $("#id_iframe_external_site").width();
			       var screenHeight = $("#id_iframe_external_site").height();

			       //if window is scrolled
			       var scrTop = $(window).scrollTop();


			       //finally show the menu
			       $("#id_iframe_output").append(menu);
				menu.show(); 
			
			});
		$("#id_iframe_external_site").on("click", function(){
				$(".menu").hide();
			});
	});
	
});
