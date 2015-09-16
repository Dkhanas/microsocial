

function initialize() {

 var options = {
  language: 'en',
  types: ['(cities)']

 };

 var input = document.getElementById('address_place');
 var autocomplete = new google.maps.places.Autocomplete(input, options);
}

google.maps.event.addDomListener(window, 'load', initialize);

function initialize2() {

 var options = {
  language: 'en'
 };

 var input = document.getElementById('companyName');
 var autocomplete = new google.maps.places.Autocomplete(input, options);
}

google.maps.event.addDomListener(window, 'load', initialize2);