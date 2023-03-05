"use strict";

let menuVisibility = false;

function toogleShow(item, classAddition){
	item.classList.toggle(classAddition);
}


function menuDropDown() {
	let menu = document.getElementById("nav-menu");
	let contentDiv = document.getElementById("content-div");
	
	if (menuVisibility == false) {
	toogleShow(menu, "show-menu");
	menu.style.animation = 'dropdown-on 0.7s';
	contentDiv.style.animation = 'content-div-thin 0.7s';
	toogleShow(contentDiv, "move-content");
	menuVisibility = true;
	}
	else {
	menu.style.animation = 'dropdown-off 0.7s';
	setTimeout(toogleShow, 450, menu, "show-menu");
	toogleShow(contentDiv, "move-content");
	menuVisibility = false;
	}
}




