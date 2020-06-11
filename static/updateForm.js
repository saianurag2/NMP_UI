document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#modifyForm').onsubmit = () => {
    	fields = document.getElementById('#modifyForm').elements;
    	console.log("Inside UpdateForm.js");
    	alert("UpdateForm.js in progress");
    	console.log(fields);
    	let mapObj = new Map();
    	for(i=0;i<fields.length;i++){
    		if(fields.index(i).value.length > 0){
    			mapObj.set(fields.index(i).id,fields.index(i).value);
    		}
    	}
    	// Initialize new request
        const request = new XMLHttpRequest();
        jsonObj = JSON.stringify(mapObj);
        console.log(jsonObj);
        request.open('PUT',"https://localhost:9001/device/");
        request.send(jsonObj);

        //after response is received
        request.onload = () =>{
        	const data = JSON.parse(request.responseText);
        	if(data.success){
        		alert("Update Request Success");
        	}
        	else{
        		alert("Request Failed");
        	}
        }
        return false;
    };

});