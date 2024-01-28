$(document).ready(function() {
	$('.salonsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  infinite: true,
	  prevArrow: $('.salons .leftArrow'),
	  nextArrow: $('.salons .rightArrow'),
	  responsive: [
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});
	$('.servicesSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.services .leftArrow'),
	  nextArrow: $('.services .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        
	      	centerMode: true,
  			//centerPadding: '60px',
	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.mastersSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.masters .leftArrow'),
	  nextArrow: $('.masters .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	$('.reviewsSlider').slick({
		arrows: true,
	  slidesToShow: 4,
	  prevArrow: $('.reviews .leftArrow'),
	  nextArrow: $('.reviews .rightArrow'),
	  responsive: [
	  	{
	      breakpoint: 1199,
	      settings: {
	        

	        slidesToShow: 3
	      }
	    },
	    {
	      breakpoint: 991,
	      settings: {
	        

	        slidesToShow: 2
	      }
	    },
	    {
	      breakpoint: 575,
	      settings: {
	        slidesToShow: 1
	      }
	    }
	  ]
	});

	// menu
	$('.header__mobMenu').click(function() {
		$('#mobMenu').show()
	})
	$('.mobMenuClose').click(function() {
		$('#mobMenu').hide()
	})

	startdate = new Date();
	lastdate = new Date(startdate);
	lastdate.setDate(lastdate.getDate()+14);
	date_picker = new AirDatepicker('#datepickerHere', {
				minDate: startdate,
				maxDate: lastdate,
				inline: true,
				dateFormat: 'yyyy-MM-dd',
				onSelect({date, formattedDate, datepicker}){
					get_timeslots();
				}
	});

	var acc = document.getElementsByClassName("accordion");
	var i;

	for (i = 0; i < acc.length; i++) {
	  acc[i].addEventListener("click", function(e) {
	  	e.preventDefault()
	    this.classList.toggle("active");
	    var panel = $(this).next()
	    panel.hasClass('active') ?  
	    	 panel.removeClass('active')
	    	: 
	    	 panel.addClass('active')
	  });
	}


	$('.accordion__block_item').click(function(e) {
		let thisName,thisAddress;
		thisName = $(this).find('> .accordion__block_item_intro').text()
		thisAddress = $(this).find('> .accordion__block_item_address').text()
		$(this).parent().parent().parent().parent().find('> button.active').addClass('selected').text(thisName + '  ' +thisAddress)
		// $(this).parent().parent().parent().parent().find('> button.active').click()
		// $(this).parent().parent().parent().addClass('hide')
		setTimeout(() => {
			$(this).parent().parent().parent().parent().find('> button.active').click()
		}, 200)
	})



	// 	console.log($('.service__masters > .panel').attr('data-masters'))
	// if($('.service__salons .accordion.selected').text() === "BeautyCity Пушкинская  ул. Пушкинская, д. 78А") {
	// }


	$(document).on('click', '.service__masters .accordion__block', function(e) {
		let clone = $(this).clone()
		console.log(clone)
		$(this).parent().parent().find('> button.active').html(clone)
	})

	// $('.accordion__block_item').click(function(e) {
	// 	const thisName = $(this).find('.accordion__block_item_intro').text()
	// 	const thisAddress = $(this).find('.accordion__block_item_address').text()
	// 	console.log($(this).parent().parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().find('button.active').addClass('selected').text(thisName + '  ' +thisAddress)
	// })



	// $('.accordion__block_item').click(function(e) {
	// 	const thisChildName = $(this).text()
	// 	console.log(thisChildName)
	// 	console.log($(this).parent().parent().parent())
	// 	$(this).parent().parent().parent().parent().parent().find('button.active').addClass('selected').text(thisChildName)

	// })
	// $('.accordion.selected').click(function() {
	// 	$(this).parent().find('.panel').hasClass('selected') ? 
	// 	 $(this).parent().find('.panel').removeClass('selected')
	// 		:
	// 	$(this).parent().find('.panel').addClass('selected')
	// })


	//popup
	$('.header__block_auth').click(function(e) {
		e.preventDefault()
		$('#authModal').arcticmodal();
		// $('#confirmModal').arcticmodal();

	})

	$('.rewiewPopupOpen').click(function(e) {
		e.preventDefault()
		$('#reviewModal').arcticmodal();
	})
	$('.payPopupOpen').click(function(e) {
		e.preventDefault()
		$('#paymentModal').arcticmodal();
	})
	$('.tipsPopupOpen').click(function(e) {
		e.preventDefault()
		$('#tipsModal').arcticmodal();
	})
	
	$('.authPopup__form').submit(function() {
		$('#confirmModal').arcticmodal();
		return false
	})

	//service
	$('.time__items .time__elems_elem .time__elems_btn').click(function(e) {
		e.preventDefault()
		$('.time__elems_btn').removeClass('active')
		$(this).addClass('active')
		// $(this).hasClass('active') ? $(this).removeClass('active') : $(this).addClass('active')
	})

/*	$(document).on('click', '.servicePage', function() {
		if($('.time__items .time__elems_elem .time__elems_btn').hasClass('active') && $('.service__form_block > button').hasClass('selected')) {
			$('.time__btns_next').addClass('active')
		}
	})
*/
	// BeautyCity team features

	function is_service_data_valid(){
		return ($('#shop_selector').val() 
			&& $('#service_selector').val()
			&& $('#shop_selector').val()
			&& $('#shop_selector').val()
			&& $('#datepickerHere').val()
			&& $('#datepickerHere').val()
			&& $('.time__elems_btn.active').text())
	}


	// Hide/show datetime picker section
	$(document).on('click', '.servicePage', function() {
		if ($('#specialist_selector').val()) {
			$('#time').show();
		} else {
			$('#time').hide();
		}
		if (is_service_data_valid()) {
			$('.time__btns_next').addClass('active')
		} else {
			$('.time__btns_next').removeClass('active')
		}
	});


	// Button "Далее" on service.html
	$('form#orderform').on('submit',  function(evt){
		if (!is_service_data_valid()) {
			alert('Заполните все поля необходимые для заказа!')
			evt.preventDefault();
		} else {
			$('#timefields').val($('.time__elems_btn.active').text());
		}
	})


	$(document).on('click', '.time__btns_home', function(){
		window.location.href = '/';
	});


	function populate_select(select_id, select_data) {
		let select_tag = $(select_id);
		let new_html = ''
		$(select_id+' option:not([selected])').remove()
		select_data.forEach(pair => {
			new_html += "<option value='" + pair[0] + "' >" + pair[1] + "</option>";
		});
		select_tag.append(new_html);
	}

	$('#shop_selector').on('change', function() {
		id = $('#service_selector').val(),
		data = {
			'shop': $(this).val(),
			'service': id,
		};
		if (id) {
			$.ajax({
				url: 'api/specialists',         /* Куда пойдет запрос */
				method: 'get',             /* Метод передачи (post или get) */
				dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
				data: data,     /* Параметры передаваемые в запросе. */
				success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
					populate_select('#specialist_selector', data.specialists);            /* В переменной data содержится ответ от index.php. */
				}
			});
		}
		
	});

	$('#service_type_selector').on('change', function() {
		id = $(this).val();
		data = {
			'shop': $('#shop_selector').val(),
			'service_type': id,
		};
		if (id) {
			$.ajax({
				url: 'api/services',         /* Куда пойдет запрос */
				method: 'get',             /* Метод передачи (post или get) */
				dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
				data: data,     /* Параметры передаваемые в запросе. */
				success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
					populate_select('#service_selector', data.services);   /* В переменной data содержится ответ от index.php. */
				}
			});
		}
	});

	$('#service_selector').on('change', function() {
		id = $(this).val();
		data = {
			'shop': $('#shop_selector').val(),
			'service': id,
		};
		if (id) {
			$.ajax({
				url: 'api/specialists',         /* Куда пойдет запрос */
				method: 'get',             /* Метод передачи (post или get) */
				dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
				data: data,     /* Параметры передаваемые в запросе. */
				success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
					populate_select('#specialist_selector', data.specialists);   /* В переменной data содержится ответ от index.php. */
				}
			});
		}
	});


	function get_timeslots() {
		date = $('#datepickerHere').val();
		data = {
			'shop': $('#shop_selector').val(),
			'service': $('#service_selector').val(),
			'specialist': $('#specialist_selector').val(),
			'date': date,
		};
		if (date) {
			$.ajax({
				url: 'api/timeslots',         /* Куда пойдет запрос */
				method: 'get',             /* Метод передачи (post или get) */
				dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
				data: data,     /* Параметры передаваемые в запросе. */
				success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
					//alert(data.morning);   /* В переменной data содержится ответ от index.php. */
					elements = $('div.time__elems_elem');
					elements.empty();
					day_parts = ['morning', 'afternoon', 'evening'];
					day_parts.forEach((value, index) => {
						data[value].forEach(slot=> {
							new_timeslot = '<button type="button" class="time__elems_btn">'+slot.slice(0,-3)+'</button>';
							elements.eq(index).append(new_timeslot);
						});
					});
					$('.time__elems_btn').click(function(e) {
						e.preventDefault();
						$('.time__elems_btn').removeClass('active');
						$(this).addClass('active');
					});
				}
			});
		}
	}


})