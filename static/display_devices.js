function ValidateIPaddress(ip)
{
 if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ip))
  {
    alert("Valid IP")
  }
  else{
	alert("You have entered an invalid IP address!")
}
return false;
}

//const bldg = document.getElementById("building");
const ip = document.getElementById("ipaddress");
document.querySelector("#submit-btn").addEventListener("click",ValidateIPaddress(ip));