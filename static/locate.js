function found(position) {
  var xmlhttp;
  if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
  }
  else
  {// code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.open("GET","/location/"+position.coords.latitude+","+position.coords.longitude,true);
  xmlhttp.send();
}

function error(msg){
}

if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(found, error);
}
