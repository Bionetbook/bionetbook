//////////////////////////////////////
//                                  //
//      Calendar functionality      //
//                                  //
//////////////////////////////////////
// Todo:
// Construct Protocol object by using the .id field supplied with each event object


$(document).ready(function() {
	var gCalURL = 'https://www.google.com/calendar/feeds/nk1n38oqstjhj5cm87f28ljpog%40group.calendar.google.com/public/basic';

	// initialize the draggable events
	$('#external-events div.external-event').each(function() {
	
		var eventObject = {};
		
		// store the Event Object in the DOM element so we can get to it later
		$(this).data('eventObject', eventObject);
		
		// make the event draggable using jQuery UI
		$(this).draggable({
			zIndex: 999,
			revert: true,      // will cause the event to go back to its
			revertDuration: 0  //  original position after the drag
		});
		
	});

	// initialize the calendar
	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,agendaWeek'
		},
		allDaySlot : false,
		events: {
			url: gCalURL,
			backgroundColor : "#bbb",
			textColor : "#666"
			},
		editable: true,
		droppable: true, 
		drop: function(date, allDay) { 
			BNB.calendar.dropEventHandler(date, allDay, this);
		}
	});

	// Set right click event handler for context menu
	document.getElementsByTagName("body")[0].onmousedown = (function(){
		return function(){ 

			var rightClick,
				e = window.event;

			// Make sure it's a right click
			if (e.which) rightClick = (e.which == 3);
			else if (e.button) rightClick = (e.button == 2);
			
			// User right clicked -- open menu
			if(rightClick) {
				BNB.calendar.rightClickMenu(e); 
				return false;
			}
		}
	})();

});

var BNB = BNB || {};

BNB.calendar = (function(){

	// Sync external event Objects with the current calendar
	// Arg: URL string
	function getEvents(url){
		$.getJSON(url)
		.done(function(data){syncEvents(data);})
		.fail(function(){console.log("Failed to get a list of events.")})
	}

	// Get JSON objects from another file (done in getEvents()) and 
	// add the data to the list of draggable events
	// Arg: JSON object
	function syncEvents(protocol){
		var dragContainer = document.getElementById('external-events'),
			protocolList = {};

		// Construct a structure that's easy to use for the calendar
		// protocolList = [  protocolID: {},  ]
		// protocolID = {  steps : [  {verb:mix, id:id},  {verb:mix, id:id}  ]  }
		for(var a = 0;  a < protocol.events.length; a++){
			// Id string: bnb-orgId-expId-protocolId-stepId-actionId
			var protocolId = protocol.events[a].id.split("-")[3];

			// Create a Protocol object for this step/action if one doesn't exist with its ID
			if(!protocolList[protocolId]) protocolList[protocolId] = { steps: [] };

			// Add .stepNumber property to action
			protocol.events[a].stepNumber = protocolList[protocolId].steps.length + 1;

			// Add the action to its place in the structure
			protocolList[protocolId].steps.push(protocol.events[a]);
		}

		console.log(protocolList)

		// Create the draggable event node
		var eventNode = document.createElement('div');
		eventNode.className = 'custom-event';

		// Populate DOM data-* with JSON properties
		eventNode.innerHTML = protocol.title;
		eventNode.setAttribute('description', protocol.steps[i].description);

		// Iterate over each Step in the protocol
		for(var i = 0; i < protocol.steps.length; i++){ 	// Iterate over steps

		   // Add properties of Actions to the DOM
		   for(var k = 0; k < protocol.steps[i].actions.length; k++){

		   		eventNode.setAttribute("data-step"+i+"-action"+k+"-title", protocol.steps[i].actions[k].title);
		   		eventNode.setAttribute("data-step"+i+"-action"+k+"-verb", protocol.steps[i].actions[k].verb);
		   		eventNode.setAttribute("data-step"+i+"-action"+k+"-event-id", protocol.steps[i].actions[k].id);
		   		eventNode.setAttribute("data-step"+i+"-action"+k+"-step-number", protocol.steps[i].actions[k].stepNumber);
		   		eventNode.setAttribute("data-step"+i+"-action"+k+"-active", protocol.steps[i].actions[k].active);
				eventNode.setAttribute("data-step"+i+"-action"+k+"-length", protocol.steps[i].actions[k].duration);  // Data says duration!
				eventNode.setAttribute("data-step"+i+"-action"+k+"-notes", protocol.steps[i].actions[k].notes);
		   }
		}

		// Add draggable event element to the page
		dragContainer.appendChild(eventNode);

		// Make them draggable
		$('#external-events div.custom-event').each(function() {

			var eventObject = {
				title: $.trim($(this).text()),
				backgroundColor : this.style.backgroundColor,
				allDay : false,
		   		length : this.getAttribute("data-length")
			};
			
			// store the Event Object in the DOM element so we can get to it later
			$(this).data('eventObject', eventObject);
			
			// make the event draggable using jQuery UI
			$(this).draggable({
				zIndex: 999,
				revert: true,      // will cause the event to go back to its
				revertDuration: 0  //  original position after the drag
			});
			
		});
		var syncButton = document.getElementById('sync-events');
		syncButton.parentNode.removeChild(syncButton);
	}

	// Add an event to the calendar when it's dropped in place
	// Arg: Date object, bool, reference to this
	function dropEventHandler(date, allDay, that){

		var weekDays = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];

		// Create a unique ID for the steps of the protocol to share
		var instanceId;

		// Create a background color based on unique ID
		// But make sure it's a LIGHT color that can show white text! (ie 5-c hex)
		do{
			instanceId = "xxxxxx".replace(/[x]/g, function(c) {
		    	var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
		    	return v.toString(16);
			});
		} 
		while(parseInt(instanceId[0], 16) < 5 || parseInt(instanceId[0], 16) > 12 ||
			  parseInt(instanceId[2], 16) < 5 || parseInt(instanceId[2], 16) > 12 ||
			  parseInt(instanceId[4], 16) < 5 || parseInt(instanceId[4], 16) > 12 )
		
		var instanceBgColor = instanceId[0].toString() + 
							  instanceId[2].toString() + 
							  instanceId[4].toString();

		
		// retrieve the dropped element's stored Event Object
		var originalEventObject = $(that).data('eventObject');
		var timeTracker = date;
		var i = 1, k = 1;

		// Get each item in the container and add them to the calendar
		while(that.getAttribute("data-step"+i+"-action1-verb")){			// Go through steps
			while(that.getAttribute("data-step"+i+"-action"+k+"-verb")){	// Go through actions of the step
				// Create an object to add to the calendar
				var eventStep = {};
				eventStep.eventId 			= that.getAttribute("data-step"+i+"-action"+k+"-event-id");
				eventStep.instanceId		= instanceId;
				eventStep.verb 				= that.getAttribute("data-step"+i+"-action"+k+"-verb");
				eventStep.allDay 			= false;
				eventStep.locked  			= true;
				eventStep.active 			= that.getAttribute("data-step"+i+"-action"+k+"-active");
				eventStep.length 			= that.getAttribute("data-step"+i+"-action"+k+"-length");
				eventStep.stepNumber 		= that.getAttribute("data-step"+i+"-action"+k+"-step-number");
				eventStep.backgroundColor 	= "#" + instanceBgColor;
				eventStep.textColor			= "#fff";
				eventStep.start 			= (new Date(timeTracker.getTime()));
				eventStep.end 				= (new Date(timeTracker.getTime() + eventStep.length * 1000));
				eventStep.notes = that.getAttribute("data-step"+i+"-action"+k+"-notes").length > 0 ? 
								  that.getAttribute("data-step"+i+"-action"+k+"-notes") : 'There are no notes for this event.';

				// Use this to decide the next step's .start
				timeTracker = eventStep.end;

				// Send data to database
				modifyProtocolStep.enqueue(eventStep, "add");

				// Add event to calendar
				$('#calendar').fullCalendar('renderEvent', eventStep, true);
				k++;
			}
			i++;
		}
	}

	// The supplied renderer sucks
	// Do Date math and rerender each dragged object
	function renderUpdatedEvents(evObj, dayDelta, minDelta){

		evObj._start = evObj.start = new Date(evObj.start.getTime() + minDelta * 60000 + dayDelta * 86400000);
		evObj._end = evObj.end = new Date(evObj.end.getTime() + minDelta * 60000 + dayDelta * 86400000);

		console.log(evObj.verb + " edited")
		// Update modified event
		$('#calendar').fullCalendar( 'updateEvent', event );
	}

	// Display an error at the top of the page
	function displayTopError(e){

		// Create nodes if the error isn't already shown
		if(!document.getElementsByClassName("top-error")[0]){

			var error = document.createElement("div");
			error.className = "top-error";
			error.innerHTML = e;
			document.getElementsByTagName("body")[0].appendChild(error);

		} else {

			// If the error is already shown, simply change the text inside
			var error = document.getElementsByClassName("top-error")[0];
			error.innerHTML = e;

		}	

		// Create an "X" element to close the error message
		var closeError = document.createElement("div");
		closeError.className = "close";
		closeError.innerHTML = "X";
		closeError.onclick = removeTopError;
		error.appendChild(closeError);
		
		// Show error
		$(error).fadeIn(100, "linear");

		// Auto hide error after time limit
		setTimeout(function(){
			// Make sure the element hasn't been closed already
			if(document.getElementsByClassName("top-error")[0]){
				removeTopError(true);
			}
		},10000);
	}

	// Remove the error at the top of the page. No easing for user-closed error, only auto-close
	function removeTopError(easing){
		easing = easing || false;

		// remove element without fading effects
		if(!easing){
			document.getElementsByClassName("top-error")[0].parentNode.removeChild(document.getElementsByClassName("top-error")[0]);
		} else {
			// fade out and remove element
			$(document.getElementsByClassName("top-error")[0]).fadeOut(200, function(){
				document.getElementsByClassName("top-error")[0].parentNode.removeChild(document.getElementsByClassName("top-error")[0]);
			});
		}
	}

	// Functions for editing and saving notes for selected steps
	var Notes = (function(){

		var currentStepNode;

		// This functions assumes that an element without notes 
		// has a data-notes value of "There are no notes for this event."
		function editNotes(ele){
			var formContainer = document.createElement("div"),
				formContent = '',
				header = '<h3>Edit Notes</h3>',
				inputArea = '<textarea placeholder="Jot down some notes" autofocus></textarea>',
				submitButton =  '<input type="button" value="Update" onclick="BNB.calendar.Notes.submitEditNotes(this)">',
				closeButton = '<span class="close" onclick="BNB.calendar.Notes.removeEditNotes(this.parentNode);">X</span>';

			// If a dialog is already open, close it
			if(document.getElementsByClassName("edit-notes-form")[0]){
				removeEditNotes(document.getElementsByClassName("edit-notes-form")[0]);
			}

			// Track the clicked element
			currentStepNode = ele.parentNode;

			// Add notes to the textarea if notes exist
			if(currentStepNode.getAttribute("data-notes") != "There are no notes for this event."){
				inputArea = '<textarea autofocus>' + 
				currentStepNode.getAttribute("data-notes") + 
				'</textarea>';
			}

			// Assemble Notes dialog box
			formContent = header + inputArea + submitButton + closeButton;

			// Add a new "Edit Notes" dialog box to the page
			formContainer.className = "edit-notes-form";
			formContainer.innerHTML = formContent;
			addEditNotes(ele, formContainer);
		}

		// Recieve edited notes and save them
		function submitEditNotes(ele){
			var popup = document.getElementsByClassName("edit-notes-form")[0],
				updatedNotes = ele.parentNode.getElementsByTagName("textarea")[0].value;

			if(!updatedNotes) updatedNotes = "There are no notes for this event."

			// Update notes
			currentStepNode.setAttribute("data-notes", updatedNotes);

			// Save notes to database
			modifyProtocolStep.enqueue( makeJsonFromNode(currentStepNode), "edit" );

			// Remove popup
			removeEditNotes(popup);
		}

		// Add element's edit notes popup
		function addEditNotes(ele, formContainer){
			document.getElementsByTagName("body")[0].appendChild(formContainer);

			// Reposition the notes popup alongside the current node
			var stepPos = currentStepNode.getBoundingClientRect();

			formContainer.style.top = stepPos.top - 8 + "px";

			// Switch popup to left side if it's editing a step on friday or saturday
			if($(currentStepNode).hasClass("fri") || $(currentStepNode).hasClass("sat")){
				formContainer.style.left = stepPos.left + 10 + "px";
				if($(currentStepNode).hasClass("fri")) formContainer.className += " fri";
				if($(currentStepNode).hasClass("sat")) formContainer.className += " sat";
			} else{
				formContainer.style.left = stepPos.left + 390 + "px";
			}

			// Show notes form
			$(formContainer).fadeIn(100);
			
			// Set editing attribute
			currentStepNode.setAttribute("data-editing", "true");
		}

		// Remove element's edit notes popup
		function removeEditNotes(ele){

			// Hide notes form
			$(ele).fadeOut(100, function(){
				ele.parentNode.removeChild(ele);
			});

			// Unset editing attribute
			currentStepNode.setAttribute("data-editing", "false");

			// Clear reference
			currentStepNode = null;
		}

		return{
			editNotes : editNotes,
			submitEditNotes : submitEditNotes,
			addEditNotes : addEditNotes,
			removeEditNotes : removeEditNotes
		}
	})();

	var protocolLock = (function(){
		function toggleLock(ele){
			var instanceId = ele.parentNode.getAttribute("data-instance-id");

			// Change both the DOM and the actual event data to toggle and track locked status
			if(ele.className == "locked"){

				// Edit DOM - instant data value/not persistant
				$("[data-instance-id="+instanceId+"]").each(function(){
					if(this.getElementsByClassName("locked")[0])
						this.getElementsByClassName("locked")[0].className = "unlocked";
					this.setAttribute("data-locked", 'false');
				});

				// Directly lock/unlock event data - persistant data value/not instant
				var evList = $('#calendar').fullCalendar( 'clientEvents' );
				for(ev in evList){
					if(evList[ev].instanceId === instanceId)
						evList[ev].locked = false;
				}

			} else {

				// Edit DOM - instant data value/not persistant
				$("[data-instance-id="+ele.parentNode.getAttribute("data-instance-id")+"]").each(function(){
					if(this.getElementsByClassName("unlocked")[0])
						this.getElementsByClassName("unlocked")[0].className = "locked";
					this.setAttribute("data-locked",'true');
				});

				// Directly lock/unlock event data - persistant data value/not instant
				var evList = $('#calendar').fullCalendar( 'clientEvents' );
				for(ev in evList){
					if(evList[ev].instanceId === instanceId)
						evList[ev].locked = true;
				}
			}
			
		}

		// Show lock icons on protocol step hover
		function show(ele){
			var instanceId = ele.parentNode.getAttribute("data-instance-id");
			$("[data-instance-id="+instanceId+"]").each(function(){
					if(this.getElementsByClassName("locked")[0])
						this.getElementsByClassName("locked")[0].style.display = "block";
					if(this.getElementsByClassName("unlocked")[0])
						this.getElementsByClassName("unlocked")[0].style.display = "block";
			});
		}

		// Hide lock icons when not hovering on protocol step
		function hide(ele){
			var instanceId = ele.parentNode.getAttribute("data-instance-id");
			$("[data-instance-id="+instanceId+"]").each(function(){
				if(this == ele) return
					if(this.getElementsByClassName("locked")[0])
						this.getElementsByClassName("locked")[0].style.display = "";
					if(this.getElementsByClassName("unlocked")[0])
						this.getElementsByClassName("unlocked")[0].style.display = "";
			});
		}

		return {
			toggleLock : toggleLock,
			show : show,
			hide : hide
		}
	})();

	// Showing right click menu
	function rightClickMenu(e){
		var clickedElement = window.event.srcElement,
			targetElement, 	// The element to get information from
			menuToShow,
			body = document.getElementsByTagName("body")[0],
			menu = document.createElement("div"),
			copy = document.createElement("p"),
			paste = document.createElement("p"),
			undo = document.createElement("p"),
			del = document.createElement("p"),
			cancel = document.createElement("p");
			
		// Clear the right click menu if it's already showing
		if(document.getElementById("right-click-menu")){
			var oldMenu = document.getElementById("right-click-menu");
			oldMenu.parentNode.removeChild(oldMenu);
			oldMenu = null;
		}

		//----------------------------------------------------------------//
		// Supress normal right clicks if a day/step is right-clicked on  //
		//----------------------------------------------------------------// 

		// A STEP was clicked on
		if (clickedElement.className == "fc-event-inner" || clickedElement.className == "edit-notes"){
			targetElement = clickedElement.parentNode;
			menuToShow = "copy";
		} 
		else if(clickedElement.className == "fc-event-time" || clickedElement.className == "fc-event-title"){
			targetElement = clickedElement.parentNode.parentNode;
			menuToShow = "copy";
		} 

		// A DAY was clicked on
		else if( $(clickedElement).hasClass("fc-day")){
			targetElement = clickedElement;
			menuToShow = "paste";
		}
		else if( $(clickedElement).hasClass("fc-day-content") ){
			targetElement = clickedElement.parentNode.parentNode;
			menuToShow = "paste";
		}
		else if( $(clickedElement.parentNode).hasClass("fc-day-content") && 
				clickedElement.parentNode.parentNode.parentNode.className.indexOf("fc-col") == -1){
			targetElement = clickedElement.parentNode.parentNode.parentNode;
			menuToShow = "paste";
		}
		else if( $(clickedElement.parentNode).hasClass("fc-day")){
			targetElement = clickedElement.parentNode;
			menuToShow = "paste";
		}

		// An HOUR was clicked on
		else if( clickedElement.className.indexOf("week-day") !== -1){
			targetElement = clickedElement; 
			menuToShow = "paste";
		}

		// Nothing of interest was clicked on
		else {
			// Show normal right click
			document.oncontextmenu = function(){return true;}
			return;
		}

		// Hide right click menu
		document.oncontextmenu = function(){return false;}

		// Place menu at the mouse cursor's position
		menu.style.top = e.y + "px";
		menu.style.left = e.x + "px";
		menu.id = "right-click-menu";

		paste.innerHTML = "Paste Protocol";
		copy.innerHTML = "Copy Protocol";
		del.innerHTML = "Delete Protocol"
		undo.innerHTML = "Undo";
		cancel.innerHTML = "Cancel";

		// Copy structure of protocol
		copy.onclick = function(){ 
			protocolStructure.copy(targetElement);
			body.removeChild(menu);
			body.onclick=""; 
		};
		// Delete structure of protocol
		del.onclick = function(){ 
			protocolStructure.del(targetElement.getAttribute("data-instance-id"));
			body.removeChild(menu);
			body.onclick=""; 
		};
		// Paste structure of protocol
		paste.onclick = function(){ 
			protocolStructure.paste(targetElement, null);
			body.removeChild(menu);
			body.onclick=""; 
		};
		// Paste structure of protocol
		undo.onclick = function(){ 
			protocolStructure.undo(targetElement);
			body.removeChild(menu);
			body.onclick=""; 
		};
		// Clear right click menu -- this also handles clicking "Cancel"
		body.onclick = function(){ 
			body.removeChild(menu); 
			body.onclick=""; 
		};

		if(menuToShow == "copy") menu.appendChild(copy);
		if(menuToShow == "copy") menu.appendChild(del);
		if(menuToShow == "paste") menu.appendChild(paste);
		if(menuToShow == "paste") menu.appendChild(undo);
		menu.appendChild(cancel);
		body.appendChild(menu)
	}

	// Copy, Paste, Undo functionality for right click menu
	var protocolStructure = (function (){
		var copiedStructure = [],
			lastDatePastedInto;		// Used for Undo

		function copy(ele){
			var instanceId = ele.getAttribute("data-instance-id");
			var selector = "[data-instance-id="+ instanceId +"]";

			// Only select the current view's steps
			if(ele.className.indexOf("fc-event-vert") !== -1) selector = ".fc-event-vert" + selector;
			if(ele.className.indexOf("fc-event-hori") !== -1) selector = ".fc-event-hori" + selector;

			// Get each step in the protocol and add it to copiedStructure
			$(selector).each(function(){
				var copiedProtocolStep = {
					verb: this.getElementsByClassName("fc-event-title")[0].innerHTML,
					backgroundColor: this.getAttribute("data-bg-color"),
					allDay: false,
					start: this.getAttribute("data-event-start"),
					active: this.getAttribute("data-active"),
					end: this.getAttribute("data-event-end"),
					container: false,
					eventId: this.getAttribute("data-event-id"),
				   	stepNumber: this.getAttribute("data-step-number"),
					notes: this.getAttribute("data-notes")
				};

				// Add copied step to the copied protocol structure
				copiedStructure[copiedProtocolStep.stepNumber] = copiedProtocolStep;
			});
		}

		// Paste structure of a protocol to another date
		function paste(clickedEle, dateReference){
			var clickedDate = new Date(clickedEle.getAttribute("data-date"));
			var originalStartDates = [];

			// Used for Undo functionality -- without this line the Undo will increment
			// the Paste's date position by a day each call
			if(dateReference) clickedDate = new Date(dateReference.setDate(dateReference.getDate() - 1));
			
			// Record each element's start date since they're overwrittern
			// in the next parts
			
			for(var i = 1; i < copiedStructure.length; i++){
				originalStartDates[i] = new Date(copiedStructure[i].start).getTime();
			}

			// The date returned from clicking on an empty element
			// returns an unfavorable time, set it to the start
			// of the first step
			// Month view
			if(clickedEle.className.indexOf("fc-day") !== -1){
				clickedDate.setDate(clickedDate.getDate() + 1);
				clickedDate.setHours(new Date(copiedStructure[1].start).getHours());
				clickedDate.setMinutes(new Date(copiedStructure[1].start).getMinutes());
			}
			// Week view
			else if(clickedEle.className.indexOf("week-day") !== -1){
				clickedDate.setDate(clickedDate.getDate());
			}

			// Remember the date in case the user uses Undo
			lastDatePastedInto = new Date(clickedDate);

			// Create an instance Id for the new protocol
			var instanceId;

			// Create a background color based on unique ID
			// But make sure it's a LIGHT color that can show white text! (ie 5-c hex)
			do{
				instanceId = "xxxxxx".replace(/[x]/g, function(c) {
			    	var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
			    	return v.toString(16);
				});
			} 
			while(parseInt(instanceId[0], 16) < 5 || parseInt(instanceId[0], 16) > 12 ||
				  parseInt(instanceId[2], 16) < 5 || parseInt(instanceId[2], 16) > 12 ||
				  parseInt(instanceId[4], 16) < 5 || parseInt(instanceId[4], 16) > 12 )
			
			var instanceBgColor = instanceId[0].toString() + 
								  instanceId[2].toString() + 
								  instanceId[4].toString();

			// Set each step's start and end dates
			for(i = 1; i < copiedStructure.length; i++){
				
				if(i == 1){   // First step
					copiedStructure[i].start = clickedDate;
					copiedStructure[i].end = 
						new Date(
							clickedDate.getTime() + 
							new Date(copiedStructure[i].end).getTime() - 
							originalStartDates[i]
						);

				} else {   // Not the first step

					copiedStructure[i].start = 
						new Date(
							new Date(copiedStructure[i].start).getTime() -	// Time Between
							originalStartDates[i-1] +						// this ele and last
							copiedStructure[i-1].start.getTime()
						);
					
					copiedStructure[i].end = 
						new Date(
							copiedStructure[i].start.getTime() + 
							new Date(copiedStructure[i].end).getTime() - 
							originalStartDates[i]
						);
				}

				// Set values common to the protocol
				copiedStructure[i].instanceId = instanceId;
				copiedStructure[i].textColor = "#fff";
				copiedStructure[i].backgroundColor = "#" + instanceBgColor;

				// Add elements to the calendar
				$('#calendar').fullCalendar('renderEvent', copiedStructure[i], true);

			}
		}

		// Undo protocol paste/delete that was last used
		function undo(ele){
			var instanceId = copiedStructure[1].instanceId;

			if($("[data-instance-id="+ instanceId +"]").length > 0){
				protocolStructure.del(instanceId);
			} else {
				paste(ele, lastDatePastedInto);
			}
		}

		// Remove protocol that was last added
		function del(id){
			$("[data-instance-id="+ id +"]").each(function(){
				$('#calendar').fullCalendar("removeEvents", this.getAttribute("data-fc-id"));
			});
		}
		
		return { 
			copy : copy,
			paste : paste,
			del : del,
			undo : undo
		}
	})();

	// Add / Edit / Remove protocol steps by using Ajax calls
	// Args: JSON Event object, Action string: add edit remove
	// ## Look into cookies to store locally in case user closes window
	// ## Check once a second if queue has items?
	var modifyProtocolStep = (function(){
		var queue = [],
			hasCallFinished = true;

		function enqueue(stepData){
			queue.push(stepData);
		}
		
		function send(){
			// Nothing to do
			if(!hasCallFinished || queue.length < 1) return;

			// when done, call send() again
		}

		return {
			enqueue : enqueue,
			send : send
		}
	})();

	function makeJsonFromNode(node){
		return {
			verb : node.getElementsByClassName("fc-event-title")[0].innerHTML,
			eventId : node.getAttribute("data-event-id"),
			instanceId : node.getAttribute("data-instance-id"),
			stepNumber : node.getAttribute("data-step-number"),
			start : node.getAttribute("data-event-start"),
			end : node.getAttribute("data-event-end"),
			notes : node.getAttribute("data-notes"),
			active : node.getAttribute("data-active"),
			bgColor : node.getAttribute("data-bg-color"),
			locked : node.getAttribute("data-locked") || true,
			container : false,
			allDay : false,
			length : (new Date(node.getAttribute("data-event-end")).getTime() - 
					new Date(node.getAttribute("data-event-start")).getTime())/1000
		};
	}

	return {
		makeJsonFromNode : makeJsonFromNode,
		displayTopError : displayTopError,
		removeTopError : removeTopError,
		getEvents : getEvents,
		dropEventHandler : dropEventHandler,
		protocolLock : protocolLock,
		Notes : Notes,
		rightClickMenu : rightClickMenu,
		renderUpdatedEvents : renderUpdatedEvents,
		syncEvents: syncEvents
	}
})();
		



