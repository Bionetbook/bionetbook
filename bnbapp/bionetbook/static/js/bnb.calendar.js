//////////////////////////////////////
//                                  //
//      Calendar functionality      //
//                                  //
//////////////////////////////////////
// Todo:
// NOTE: syncEvents() has FAKE length

"use strict";

$(document).ready(function() {
	// var gCalURL = 'https://www.google.com/calendar/feeds/nk1n38oqstjhj5c'+
	//				 'm87f28ljpog%40group.calendar.google.com/public/basic';
	var gCalURL = '';

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
	document.body.onmousedown = (function(){

		return function(e){ 

			var rightClick,
				e = e || window.event;

			// Make sure it's a right click
			if (e.which) rightClick = (e.which == 3);
			else if (e.button) rightClick = (e.button == 2);
			
			// User right clicked -- open menu
			if(rightClick) {
				BNB.calendar.rightClickMenu(e); 
				return false;
			}
		}
	})(window.event);

});
$("footer").remove();
var BNB = BNB || {};

BNB.calendar = (function(){

	var dragContainer = document.getElementById('external-events'),
		experiments = {}, 
		protocolList = {};

	getEvents(dragContainer.getAttribute('data-calendar'));

	// Sync external event Objects with the current calendar
	// Arg: URL string
	function getEvents(url){
		$.getJSON(url)
		.done(function(data){syncEvents(data);})
		.fail(function(){console.log("Failed to get a list of events.")})
	}

	// Get JSON objects from another file, done in getEvents(), and 
	// add the data to the list of draggable events
	// Arg: JSON object
	function syncEvents(p){

		// Make experiment structure from action id strings
		for(var a = 0;  a < p.events.length; a++){

			// Id string: bnb-orgId-expId-protocolId-stepId-actionId
			var expId = p.events[a].id.split("-")[2],
				protocolId = p.events[a].id.split("-")[3],
				stepId = p.events[a].id.split("-")[4],
				exp,
				protocol,
				step;

			// Create an exp object for this action if one doesn't exist with its ID
			if(!experiments[expId]){
				experiments[expId] = { 
					id: expId,
					title: p.events[a].experiment, 
					protocols: [] 
				};
			}
			exp = experiments[expId];

			// Create a Protocol object for this action if one doesn't exist with its ID
			if( !getObjInArr(exp.protocols, 'id', protocolId) ){
				exp.protocols.push({ 
					id: protocolId,
					title: p.events[a].protocol, 
					steps: [] 
				});
			}
			protocol = exp.protocols[exp.protocols.length - 1];

			// Create a step object if it doesn't exist for this step ID
			if( !getObjInArr(protocol.steps, 'id', stepId) ){
				protocol.steps.push({
					id: stepId,
					stepNumber: protocol.steps.length,
					actions: []
				});
				
			}
			var step = getObjInArr(protocol.steps, 'id', stepId);

			// + extra properties
			if(p.meta.descriptions) exp.description = p.meta.descriptions[expId];	// exp descrip
			if(!p.events[a].id) p.events[a].id = p.events[a].objectid;				// action id
			p.events[a].stepNumber = step.actions.length + 1;			       		// stepnumber

			// Add the action to its place in the structure
			step.actions.push(p.events[a]);
		}

		// Show a draggable item for each protocol the user has access to
		for(var e in experiments)
			
			var thisExp = experiments[e];

			// Create draggable node
			var eventNode = document.createElement('div');
			eventNode.className = 'custom-event';
			eventNode.innerHTML = thisExp.title;
			eventNode.setAttribute("data-id", thisExp.id);

			// Protocols in experiment
			for(var b = 0, pLen = thisExp.protocols.length; b < pLen; b++){
				var thisProtocol = thisExp.protocols[b],
					pId = thisExp.protocols[b].id;

			   // Steps in protocol
			   for(var c = 0; c < thisProtocol.steps.length; c++){
			   		var thisStep = thisProtocol.steps[c],
			   			sId = thisProtocol.steps[c].id;

			   		// Actions in step
			   		for(var d = 0; d < thisStep.actions.length; d++){

				   		var thisAction = thisStep.actions[d],
				   			idArr = thisStep.actions[d].id.split("-");
				   		var eId = idArr[2],  // Experiment
				   			pId = idArr[3],  // Protocol
				   			sId = idArr[4],  // Step
				   			aId = idArr[5];  // Action
				   		var domId = 'data-'+ eId +'-'+ pId +'-'+ sId +'-'+ aId + '-';

				   		eventNode.setAttribute(domId + "title", thisAction.title);
				   		eventNode.setAttribute(domId + "verb", thisAction.verb);
				   		eventNode.setAttribute(domId + "step-number", thisAction.stepNumber);
				   		eventNode.setAttribute(domId + "active", thisAction.active);
						eventNode.setAttribute(domId + "notes", thisAction.notes);
						eventNode.setAttribute(domId + "length", /*thisAction.duration*/ 6000);
						eventNode.setAttribute(domId + "event-id", thisAction.id);
						eventNode.setAttribute(domId + "eid", eId);
						eventNode.setAttribute(domId + "pid", pId);
						eventNode.setAttribute(domId + "sid", sId);
						eventNode.setAttribute(domId + "aid", aId);
			   }
			}

			// Add draggable event element to the page
			dragContainer.appendChild(eventNode);
		}

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
	}

	// Add an event to the calendar when it's dropped in place
	// Arg: Date object, bool, reference to this
	function dropEventHandler(date, allDay, that){

		var weekDays = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"],
			timeTracker = date, // calc starting pos of actions on calendar
			thisExp = getObjInObjWithKey(experiments, 'id', that.getAttribute('data-id'));

		// Create a random background color
		// But make sure it's a LIGHT color that can show white text! (ie 5-c hex)
		do{
			instanceId = "xxx".replace(/[x]/g, function(c) {
		    	var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
		    	return v.toString(16);
			});
		} 
		while(parseInt(instanceId[0], 16) < 5 || parseInt(instanceId[0], 16) > 12 ||
			  parseInt(instanceId[1], 16) < 5 || parseInt(instanceId[1], 16) > 12 ||
			  parseInt(instanceId[2], 16) < 5 || parseInt(instanceId[2], 16) > 12 )
		var instanceBgColor = instanceId[0]+''+instanceId[1]+''+instanceId[2];


		// Protocols in experiment
		for(var a = 0, pLen = thisExp.protocols.length; a < pLen; a++){
			var thisProtocol = thisExp.protocols[a];

			// Steps in protocol
			for(var b = 0, sLen = thisProtocol.steps.length; b < sLen; b++){
				var thisStep = thisProtocol.steps[b];

				// Actions in step
				for(var c = 0, aLen = thisStep.actions.length; c < aLen; c++){
					var action = thisStep.actions[c],
				   		idArr = thisStep.actions[c].id.split("-");
			   		var eId = idArr[2],  // Experiment
			   			pId = idArr[3],  // Protocol
			   			sId = idArr[4],  // Step
			   			aId = idArr[5];  // Action
					var domId = 'data-'+ eId +'-'+ pId +'-'+ sId +'-'+ aId + '-';

					// Create an object to add to the calendar
					var eventStep = {};
					eventStep.eventId 			= that.getAttribute(domId + "event-id");
					eventStep.verb 				= that.getAttribute(domId + "verb");
					eventStep.active 			= !!that.getAttribute(domId + "active");
					eventStep.length 			= that.getAttribute(domId + "length");
					eventStep.stepNumber 		= that.getAttribute(domId + "step-number");
					eventStep.allDay 			= false;
					eventStep.locked  			= true;
					eventStep.backgroundColor 	= "#" + instanceBgColor;
					eventStep.textColor			= "#fff";
					eventStep.start 			= (new Date(timeTracker.getTime()));
					eventStep.end 				= (new Date(timeTracker.getTime() + eventStep.length * 1000));
					eventStep.notes = that.getAttribute(domId + "notes").length > 0 ? 
					 				  that.getAttribute(domId + "notes") : 
					 				  'There are no notes for this event.';

					// Use this to decide the next step's .start
					timeTracker = eventStep.end;

					// Send data to database
					saveAction.enqueue(eventStep);

					// Add event to calendar
					$('#calendar').fullCalendar('renderEvent', eventStep, true);
				}
			}
		}

		// Disable draggable node
		$(that).addClass('disabled');
	}

	// The supplied renderer sucks
	// Do Date math and rerender each dragged object
	function renderUpdatedEvents(evObj, dayDelta, minDelta, e){
		var event = event || e;
		evObj._start = evObj.start = new Date(evObj.start.getTime() + minDelta * 60000 + dayDelta * 86400000);
		if(evObj._end) evObj._end = evObj.end = new Date(evObj.end.getTime() + minDelta * 60000 + dayDelta * 86400000);

		$('[data-fc-id='+ evObj._id + ']').attr('data-event-start', evObj.start);
		if(evObj._end) $('[data-fc-id='+ evObj._id + ']').attr('data-event-end', evObj.start);

		var evList = $('#calendar').fullCalendar( 'clientEvents' );

		// Send updated action to server
		saveAction.enqueue(evObj);

		// Update modified event
		$('#calendar').fullCalendar( 'updateEvent', evObj );
	}

	// Display an error at the top of the page
	// If this isn't showing, make sure it's not hidden under the header/footer
	function displayTopError(e){

		// Create nodes if the error isn't already shown
		if(!document.getElementsByClassName("top-error")[0]){
			var error = document.createElement("div");
			error.className = "top-error";
			error.innerHTML = e;
			document.getElementsByTagName("body")[0].appendChild(error);

		} else {

			// If the error is already shown, replace it
			$(document.getElementsByClassName("top-error")[0]).remove();
			displayTopError(e);
			return;
		}	

		// Create an "X" element to close the error message
		var closeError = document.createElement("div");
		closeError.className = "close";
		closeError.innerHTML = "X";
		closeError.onclick = function(){
			document.getElementsByClassName("top-error")[0].parentNode
				.removeChild(document.getElementsByClassName("top-error")[0]);
		}
		error.appendChild(closeError);
		
		// Show error
		$(error).fadeIn(100, "linear");

		// Auto hide error after time limit
		setTimeout(function(){
			// Make sure the element hasn't been closed already
			if(document.getElementsByClassName("top-error")[0]){
				$(document.getElementsByClassName("top-error")[0]).fadeOut(200, function(){
					document.getElementsByClassName("top-error")[0].parentNode
						.removeChild(document.getElementsByClassName("top-error")[0]);
				});
			}
		},10000);
	}

	var protocolLock = (function(){

		function toggleLock(ele){

			var eventId = ele.parentNode.getAttribute("data-event-id"),
				eId = ele.parentNode.getAttribute("data-eid"),
				pId = ele.parentNode.getAttribute("data-pid");

			// Change both the DOM and the actual event data to toggle and track locked status
			if(ele.className == "locked"){

				// Edit DOM - instant data value/not persistant
				$("[data-eid="+eId+"][data-pid="+pId+"]").each(function(){
					if(this.getElementsByClassName("locked")[0])
						this.getElementsByClassName("locked")[0].className = "unlocked";
					this.setAttribute("data-locked", 'false');
				});

				// Directly lock/unlock event data - persistant data value/not instant
				var evList = $('#calendar').fullCalendar( 'clientEvents' );
				for(ev in evList){
					if(evList[ev].eventId.split('-')[3] === pId)
						evList[ev].locked = false;
				}

			} else {

				// Edit DOM - instant data value/not persistant
				$("[data-eid="+eId+"][data-pid="+pId+"]").each(function(){
					if(this.getElementsByClassName("unlocked")[0])
						this.getElementsByClassName("unlocked")[0].className = "locked";
					this.setAttribute("data-locked",'true');
				});

				// Directly lock/unlock event data - persistant data value/not instant
				var evList = $('#calendar').fullCalendar( 'clientEvents' );
				for(ev in evList){
					if(evList[ev].eventId.split('-')[3] === pId)
						evList[ev].locked = true;
				}
			}
		}

		// Show lock icons on protocol step hover
		function show(ele){
			var eventId = ele.parentNode.getAttribute("data-event-id"),
				eId = ele.parentNode.getAttribute("data-eid"),
				pId = ele.parentNode.getAttribute("data-pid");

			var instanceId = ele.parentNode.getAttribute("data-instance-id");
			$("[data-eid="+eId+"][data-pid="+pId+"]").each(function(){
					if(this.getElementsByClassName("locked")[0])
						this.getElementsByClassName("locked")[0].style.display = "block";
					if(this.getElementsByClassName("unlocked")[0])
						this.getElementsByClassName("unlocked")[0].style.display = "block";
			});
		}

		// Hide lock icons when not hovering on protocol step
		function hide(ele){
			var eventId = ele.parentNode.getAttribute("data-event-id"),
				eId = ele.parentNode.getAttribute("data-eid"),
				pId = ele.parentNode.getAttribute("data-pid");
				
			var instanceId = ele.parentNode.getAttribute("data-instance-id");
			$("[data-eid="+eId+"][data-pid="+pId+"]").each(function(){
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
				submitButton =  '<input type="button" class="btn" value="Update" onclick="BNB.calendar.Notes.submitEditNotes(this)">',
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
			saveAction.enqueue( makeJsonFromNode(currentStepNode));

			// Remove popup
			removeEditNotes(popup);
		}

		// Add element's edit notes popup
		// -- Not working cross-browser
		// -- Different behavior depending on screen pos
		// -- Try using a position relative to the PAGE, not viewport
		// -> http://stackoverflow.com/questions/5601659/how-do-you-calculate-the-page-position-of-a-dom-element-when-the-body-can-be-rel
		function addEditNotes(ele, formContainer){

			var loc = ele.parentNode.insertBefore(document.createElement('span'), ele.parentNode.firstChild);
			loc.setAttribute("style", "position:absolute;top:0;left:0;");
			// Appending to node won't accept pointer events!
			document.body.appendChild(formContainer);

			// Reposition the notes popup alongside the current node
			var locPos = $(loc).offset();
			$(loc).remove();

			formContainer.style.top = (locPos.top - 5) + 'px';

			// Switch popup to left side if it's editing a step's notes on friday or saturday
			if($(currentStepNode).hasClass("fri") || $(currentStepNode).hasClass("sat")){
				if($(currentStepNode).hasClass("fri")) formContainer.className += " fri";
				if($(currentStepNode).hasClass("sat")) formContainer.className += " sat";
				formContainer.style.left = (locPos.left - 215) + 'px';
			} else {
				// Sunday - Thursday
				formContainer.style.left = (locPos.left + 115) + 'px';
				//formContainer.style.right = "0";
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

	// Showing right click menu
	// Supress normal right clicks if a day/step is right-clicked on
	function rightClickMenu(e){
		var clickedElement = (e.target || window.event.srcElement),
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

		// Check the element that was clicked on
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

		// Hide browser's right click menu
		document.oncontextmenu = function(){return false;}

		// Place menu at the mouse cursor's position
		menu.style.top = (e.pageY || e.y) + "px";
		menu.style.left = (e.pageX || e.x) + "px";
		menu.id = "right-click-menu";

		paste.innerHTML = "Paste Experiment";
		copy.innerHTML = "Copy Experiment";
		del.innerHTML = "Remove Experiment"
		undo.innerHTML = "Undo";
		cancel.innerHTML = "Cancel";

		// Copy structure of protocol
		copy.onclick = function(){ 
			protocolStructure.copy(targetElement);
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
		// Delete structure of protocol
		del.onclick = function(){ 
			protocolStructure.del(targetElement.getAttribute("data-eid"));
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

	// TODO: Copy/Paste/Undo is broken
	// Copy, Paste, Undo functionality for right click menu
	var protocolStructure = (function (){
		var copiedStructure = [],
			lastDatePastedInto;		// Used for Undo

		function copy(ele){
			var eId = ele.getAttribute("data-eid");
			var selector = "[data-eid="+ eId +"]";

			// Only select the current view's steps
			if(ele.className.indexOf("fc-event-vert") !== -1) selector = ".fc-event-vert" + selector;
			if(ele.className.indexOf("fc-event-hori") !== -1) selector = ".fc-event-hori" + selector;

			// Get each step in the protocol and add it to copiedStructure
			$(selector).each(function(){
				var copiedProtocolStep = makeJsonFromNode(this);

				// TODO: This doesn't work anymore. Experiments have many, many steps with identical numbers.
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
			$("[data-eid="+ id +"]").each(function(){
				$('#calendar').fullCalendar("removeEvents", this.getAttribute("data-fc-id"));
			});
			$("[data-id="+ id +"]").removeClass('disabled');
		}
		
		return { 
			copy : copy,
			paste : paste,
			del : del,
			undo : undo
		}
	})();

	// Arg: JSON action
	// ## Look into cookies to store locally in case user closes window
	// ## Check once a second if queue has items?
	var saveAction = (function(){
		/*
		Server expects this structure
		{
	        'id':"bnb-o1-e1-p1-AXBAGS-FFGGAX",
	        'start':12321311231,
	        'notes':"",
	        'status':"updated"
	    }
		*/
		var queue = [],
			backlog = [],
			hasCallFinished = true,
			csrfToken = $('input[name=csrfmiddlewaretoken]').val(),
			urlComponents = window.location.href.split('/'),
			url = '/api/calendar/';

		// Remove from user view
        $('input[name=csrfmiddlewaretoken]').remove();

		// Add primary key/slug of current calendar to url
		while(urlComponents.shift() != "schedule"){}
		url += urlComponents.shift() + '/';

		// Nessasary for use with CSRF token
		$.ajaxSetup({ 
            beforeSend: function(xhr, settings) {
                function getCookie(name) {
                    var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                break;
                            }
                        }
                    }
                    return cookieValue;
                }
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    // Only send the token to relative URLs
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            csrfmiddlewaretoken: csrfToken
        });

		function enqueue(stepData){
			var s = {
				id: stepData.eventId, 
				start: stepData.start, 
				notes: stepData.notes
			};

			s.notes = s.notes == "There are no notes for this event." ? "" : s.notes;

			if(hasCallFinished){
				queue.push(s);
				sendQueue();
			} else {
				backlog.push(s);
			}
		}
		
		function sendQueue(){

			if(!hasCallFinished || queue.length < 1) return;

			// The data must be passed in as FormData or else 
			// Django will reformat it, rendering it useless
			var fd = new FormData();
			fd.append("events", JSON.stringify(queue));

			// contentType and processData MUST be set to false!
			$.ajax({
				url: url,
                type: "PUT",
				data: fd,
				processData: false,
  				contentType: false,

            	success: function(){
            		// Overwrite queue with deep copy of backlog
            		queue = $.extend(true, [], backlog);
            		hasCallFinished = true;
            	},
            	error: function(){
            		// Deep copy of backlog to concat with queue
					queue = queue.concat($.extend(true, [], backlog));
            	},
            	complete: function(){
            		backlog = [];
					sendQueue();
            	}
			});
		}

		return {
			enqueue : enqueue
		}
	})();

	// Return Json created from scraping DOM node's data
	function makeJsonFromNode(node){
		return {
			verb : node.getAttribute("data-verb"),
			eventId : node.getAttribute("data-event-id"),
			id : node.getAttribute("data-event-id"),   // Just in case
			stepNumber : node.getAttribute("data-step-number"),
			start : node.getAttribute("data-event-start"),
			end : node.getAttribute("data-event-end"),
			notes : node.getAttribute("data-notes"),
			active : node.getAttribute("data-active"),
			bgColor : node.getAttribute("data-bg-color"),
			locked : node.getAttribute("data-locked") || true,
			container : false,
			allDay : false,
			length : (node.getAttribute("data-length") || (new Date(node.getAttribute("data-event-end")).getTime() - 
					new Date(node.getAttribute("data-event-start")).getTime())/1000)
		};
	}

	// Return the HTML needed to display an event(action) on the calendar
	// Args: eventObject, objects + functions from fullCalendar's scope
	function makeHtmlFromJson(event, classes, seg, skinCss, htmlEscape, formatDates, opt){
		var weekDays = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
		var isLocked = (event.locked == "true" || event.locked == true) ? "locked" : "unlocked";

		var html =

			// Classes
			" class='" + classes.join(' ') + " " + 
				weekDays[new Date(event._start).getDay()] + "'" +

			// Identifiers
			" data-event-id='" + event.eventId + "'" +
			" data-eid='" + event.eventId.split("-")[2] + "'" +
			" data-pid='" + event.eventId.split("-")[3] + "'" +
			" data-sid='" + event.eventId.split("-")[4] + "'" +
			" data-aid='" + event.eventId.split("-")[5] + "'" +

			// Data
			" data-step-number='" + event.stepNumber + "'" +
			" data-event-start='" + event._start + "'" +
			" data-event-end='" + event._end + "'" +
			" data-active='" + event.active + "'" +
			" data-verb='" + event.verb + "'" +
			" data-notes='" + event.notes + "'" +
			" data-bg-color='" + event.backgroundColor + "'" +
			" data-fc-id='" + event._id + "'" +
			" data-locked='" + event.locked + "'" +

			// Css positioning
			" style='position:absolute;z-index:8;top:" + seg.top + 
			"px;left:" + seg.left + "px;border-color:"+ event.backgroundColor + ";" + skinCss + "'" +
			">" +

			// Lock + Notes Icon
			"<span class='"+ isLocked +"' onclick='BNB.calendar.protocolLock.toggleLock(this);' "+
				"onmouseover='BNB.calendar.protocolLock.show(this)' " +
				"onmouseout='BNB.calendar.protocolLock.hide(this)'></span>" +
			"<span class='edit-notes' onclick='BNB.calendar.Notes.editNotes(this)'></span>"+

			// Title + Date
			"<div class='fc-event-inner'>" +
			"<div class='fc-event-time'>" +
			htmlEscape(formatDates(event.start, event.end, opt('timeFormat'))) +
			"</div>" +
			"<div class='fc-event-title'>" +
			htmlEscape(event.verb || event.title) +
			"</div>";

		// Add padding to start + end for passive events
		if(event.active == "false" && classes.join(' ').indexOf('vert') != -1){
			html +=
				"<div class='passive-padding-start' style='background-color:" +
					event.backgroundColor + "'></div>" +
				"<div class='passive-padding-end' style='background-color:" +
					event.backgroundColor + "'></div>";
		}

		html +=
			"</div>" + // .fc-event-inner
			"<div class='fc-event-bg'></div>";

		return html;
	}

	// Find 1st object in an array by specifying a value it must have for a key
	function getObjInArr(arr, key, val){
		for (var i = 0, len = arr.length; i < len; i++) {
		    if(arr[i][key] === val) return arr[i];
		}
		return false;
	}

	// Find 1st object in an Object by specifying a value it must have for a key
	function getObjInObjWithKey(obj, key, val){
		for(var i in obj){
		    if(obj[i][key] === val) return obj[i];
		}
		return false;
	}

	function objectLength(o){
		var c = 0;
		for (var k in o) {
		    if (o.hasOwnProperty(k)) {
		       ++c;
		    }
		}
		return c;
	}

	return {
		makeJsonFromNode: makeJsonFromNode,
		makeHtmlFromJson: makeHtmlFromJson,
		displayTopError: displayTopError,
		getEvents: getEvents,
		dropEventHandler: dropEventHandler,
		protocolLock: protocolLock,
		Notes: Notes,
		rightClickMenu: rightClickMenu,
		renderUpdatedEvents: renderUpdatedEvents,
		protocolList: protocolList
	}
})();
		



