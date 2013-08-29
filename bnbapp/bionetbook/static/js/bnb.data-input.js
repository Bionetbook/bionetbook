"use strict";

// Creating a new Protocol - as opposed to editing an existing one
var createMode = false;

// Protocol global object creation
if(typeof Protocol == 'undefined'){
    var Protocol = {
        id: "p1",
        steps: []
    };
    createMode = true;
}

var BNB = BNB || {};

BNB.dataInput = (function(){

    var verbList = [ "Select a verb" ];

    init();

    function init(){
        // Populate verb list
        $.ajax({
            url: apiUrlPrefix + 'action/types/',
            dataType: 'json',
            success: function(e){
                for(var i =0; i < e.data.length; i++){
                    verbList.push( e.data[i].name );
                }
            },
            error: function(e){console.log("Ajax request failed. (Verb List)")}
        });

        // Add new tab when the "add new tab" is clicked
        $('#nav-tabs li.add-new-step a').on('click.newTab', function (e) {
            e.preventDefault();
            addNewTab();
        });

        // Decide what to do first
        if(createMode) 
            intro();
        else
            parseExistingProtocol();

        // Add functionality to the save button
        document.getElementById('save-protocol').onclick = function(){
            $.ajax({
                url: apiUrlPrefix + 'save-protocol',
                dataType: 'json',
                type: "POST",
                data: Protocol,
                success: function(e){ 
                    var message = document.getElementById('save-protocol').parentNode
                        .appendChild( document.createElement("div") );
                    message.className = 'alert alert-error save-alert';
                    message.innerHTML = '<button type="button" class="close" data-dismiss="alert">×</button>';
                    message.innerHTML += '<strong>Success!</strong> ';
                    message.innerHTML += 'This protocol has been saved.';
                    $(message).hide().fadeIn(200);

                    // Automatically remove alert
                    setTimeout(function(){
                        if(document.getElementsByClassName('save-alert')[0]){
                            $(document.getElementsByClassName('save-alert')[0]).fadeOut(200, function(){
                                $(document.getElementsByClassName('save-alert')[0]).remove();
                            });
                            message = null;
                        }
                    }, 10000);
                },
                error: function(e){ 
                    var message = document.getElementById('save-protocol').parentNode
                        .appendChild( document.createElement("div") );
                    message.className = 'alert alert-error save-alert';
                    message.innerHTML = '<button type="button" class="close" data-dismiss="alert">×</button>';
                    message.innerHTML += '<strong>Whoops!</strong> ';
                    message.innerHTML += 'Could not connect to the server; try again in just a second.';
                    $(message).hide().fadeIn(200);

                    // Automatically remove alert
                    setTimeout(function(){
                        if(document.getElementsByClassName('save-alert')[0]){
                            $(document.getElementsByClassName('save-alert')[0]).fadeOut(200, function(){
                                $(document.getElementsByClassName('save-alert')[0]).remove();
                            });
                            message = null;
                        }
                    }, 10000);
                }
            });
        }
    }

    // Hero unit overlay + blurred out text
    function intro(){ 
        var introUnit = document.getElementById('protocol-intro'),
            userInput = document.getElementById('protocol-intro').getElementsByTagName('input')[0],
            submitBtn = document.getElementById('intro-submit'),
            errorNode = document.createElement("div");

        // Check for "Enter" keypress
        userInput.addEventListener("keydown", function(e) {
            if (!e) { var e = window.event; }
            if (e.keyCode == 13) { submitBtn.click(); }
        }, false);

        submitBtn.onclick = function(){

            // Make sure they typed in a name or fire an error
            if(userInput.value.length < 2){
                errorNode.className = "alert alert-error";
                errorNode.innerHTML = '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                                      "You have to name the protocol before you can continue!";
                userInput.parentNode.parentNode.insertBefore(errorNode, userInput.parentNode)
                return;
            }

            // Add title to protocol object
            Protocol.title = userInput.value;

            // Change Title
            document.getElementById("protocol-title").innerHTML = userInput.value;

            // Let title + desc be editible
            fieldEditingFunctionality(document.getElementById("protocol-title"), "protocol name", "Name this protocol", Protocol, "title");
            fieldEditingFunctionality(document.getElementById("protocol-description"), "description", "add a description", Protocol, "description");

            // Remove overlay
            $(introUnit).fadeOut("fast");

            // Remove blurred text
            $(document.getElementById("nav-tabs")).removeClass("blur-text");

            // Add first Step
            addNewTab();
        }
    }

    function parseExistingProtocol(){
        for(var i = 0; i < Protocol.steps.length; i++){
            addNewTab( Protocol.steps[i] );
        }
    }

    function addNewTab(existingStep){
        var tabContainer = document.getElementById('protocol-tabs'),
            newTab = document.createElement("li"),
            newLink = document.createElement("a"),
            tabNum = document.getElementById("protocol-tabs").getElementsByTagName("li").length;

        // Create new step in Protocol
        var tempId = new Date().getTime();
        Protocol.steps.push({
            id: tempId,
            actions: []
        });
        newTab.setAttribute("data-id", tempId);

        // get real id from server and replace the tempId
        $.ajax({
            url: 'api/createStep',
            dataType: 'json',
            success: function(e){

                // Check for the step with the temporary id we just created and 
                // give it the real id from the server
                for(var step in Protocol.steps){
                    if(step.id == tempId){
                        step.id = e.data.id; 
                        newTab.setAttribute("data-id", e.data.id);
                        break;
                    }
                }

            },
            error: function(e){console.log("Ajax request failed. (Step Creation)")}
        });

        // Add attributes
        newTab.className = "active";
        newLink.href = "#tabContent" + tabNum;
        newLink.innerHTML = '<input type="text" placeholder="step name" autofocus>';

        createTabContent(tabNum, tempId);

        // Construct node heirarchy
        newTab.appendChild(newLink);
        tabContainer.insertBefore(newTab, document.getElementsByClassName('add-new-step')[0]);



        // Adding editing functionality to the tab onclick
        var numTabs = document.getElementById("protocol-tabs").children.length - 2;
        if(numTabs < 0) numTabs = 0;
        fieldEditingFunctionality(newLink, "step name", "Name this step", Protocol.steps[numTabs], "title");

        // Switch active tabs
        $('.tab-pane').removeClass('active');
        $("#tabContent" + tabNum).addClass('active');
        $(".add-new-step").removeClass('active');

        // Reset event listeners
        $('#nav-tabs li a').off('click.showTab');
        $('#nav-tabs li.add-new-step a').off('click.newTab');

        // Add listeners back
        // Clicking a tab shows it
        $('#nav-tabs li a').on('click.showTab', function (e) {
            e.preventDefault();
            $(this).tab('show');
        });
        // Add new tab when the "add new tab" is clicked
        $('#nav-tabs li.add-new-step a').on('click.newTab', function (e) {
            e.preventDefault();
            addNewTab();
        });
    }

    function createTabContent(tabNum, containerTempId){
        var tabContent = document.createElement("div"),
            addAction = document.createElement("div"),
            header = document.createElement("div"),
                headerH2 = document.createElement("h2"),
                    headerH2Small = document.createElement("small"),
                        headerH2Edit = document.createElement("span");

        header.className = "page-header";
        // Step description label
        headerH2Small.innerHTML = "Step description: "
        // Step description
        headerH2Edit.innerHTML = "add a descrription";
        headerH2Edit.className = "step-description";
        // Step description editing
        fieldEditingFunctionality(headerH2Edit, 'description', 'add a description', getStep(containerTempId), "description");
        
        headerH2Small.appendChild(headerH2Edit);
        headerH2.appendChild(headerH2Small);
        header.appendChild(headerH2);
        tabContent.appendChild(header);

        tabContent.className = "tab-pane";
        tabContent.id = "tabContent" + tabNum;
        tabContent.setAttribute("data-id", containerTempId);

        addAction.className = "add-new-action";
        addAction.innerHTML='<h4>&plus; add new action</h4>';
        tabContent.appendChild(addAction);
        
        // Add another action
        addAction.onclick = function(){
            var tempId = new Date().getTime();

            // Add action to containing Step
            var stepToAddActionTo = getStep($("[href=#tabContent"+ tabNum +"]").parent().attr("data-id"));
            stepToAddActionTo.actions.push({
                id: tempId
            });

            // Create action
            var newAction = createNewAction(this.parentNode.getAttribute("data-id"));

            // get real id from server and replace the tempId
            $.ajax({
                url: 'api/createStep',
                dataType: 'json',
                success: function(e){

                    // Find this action
                    for(var i = 0; i < stepToAddActionTo.actions.length; i++){
                        // Update to real id
                        if(stepToAddActionTo.actions[i].id == tempId)
                            stepToAddActionTo.actions[i].id = e.data.id;
                    }

                },
                error: function(e){console.log("Ajax request failed. (Action ID Creation)")}
            });

            // show action
            newAction.style.display = "none";
            this.parentNode.insertBefore(newAction, this);
            $(newAction).fadeIn();
        }

        document.getElementsByClassName("tab-content")[0].appendChild(tabContent);

        $('#nav-tabs li a').click(function (e) {
            e.preventDefault();
            $(this).tab('show');
        });
    }

    function createNewAction(containerId){
        var action = document.createElement("table"),
            tbody = document.createElement("tbody"),
            header = document.createElement("tr"),
                innerHeaderTd = document.createElement("td"),
                innerHeaderh4 = document.createElement("h4"),
                isActiveToggle = document.createElement("fieldset"),
                    isActiveLabel = document.createElement("label"),
                    isActive = document.createElement("input"),
            verb = document.createElement("tr"),
                innerVerbTd = document.createElement("td"),
                innerVerbSelect = document.createElement("select");

        var parentStep = getStep(containerId);
        var thisAction = parentStep.actions[ parentStep.actions.length -1 ];
        var tempId = new Date().getTime();

        // get real id from server and replace the tempId
        $.ajax({
            url: 'api/createAction',
            dataType: 'json',
            success: function(e){
                // e.data.id
            },
            error: function(e){console.log("Ajax request failed. (Action Creation)")}
        });
 
        action.className = "table table-bordered action-container";
        action.setAttribute("data-id", tempId)

        //------------------------------------
        //   Action header (naming action)
        //------------------------------------
        // Verb
        innerHeaderh4.innerHTML = "Name this action";
        innerHeaderTd.setAttribute("colspan", "2");
        innerHeaderTd.appendChild(innerHeaderh4);
        innerHeaderTd.appendChild(isActiveToggle);
        header.className = "action-header";
        header.appendChild(innerHeaderTd);

        // is active
        isActive.setAttribute("type", "checkbox");
        isActiveLabel.appendChild(isActive);
        isActiveLabel.onclick = function(){
            console.log(this, thisAction)
            thisAction.isActive = !!this.getElementsByTagName('input')[0].checked;
        };
        isActiveLabel.innerHTML += 'Is this action active?';
        isActiveToggle.className = 'isactive-toggle';
        isActiveToggle.appendChild(isActiveLabel);

        // Editing capabilities
        fieldEditingFunctionality( innerHeaderh4, "action name", "Name this action", thisAction, "title");

        // Add section to container
        tbody.appendChild(header);

        //------------------------------------
        //   Verb Selection (defining verb)
        //------------------------------------

        // Add verbs to select node
        for(var i = 0; i < verbList.length; i++){

            var verbOption = document.createElement("option");

            verbOption.innerHTML = verbList[i];
            verbOption.value = verbList[i];
            innerVerbSelect.appendChild(verbOption);
        }

        // Add event handler for verb selection
        innerVerbSelect.onchange = function(){

            var container = this.parentNode.parentNode.parentNode;

            // Clear previous verb selection
            // Lots of .parentNode so here's a respresentation of the structure:
            // tbody -> tr.verb -> td -> select(this) -> option
            while(this.parentNode.parentNode.nextSibling){
                this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.nextSibling);
            }

            // Clear data from last selection(useful if the ajax request fails)
            thisAction.verb = "";

            // Create form elements
            // Arg: object
            function createFormControlGroup(data){

                var controlGroup = document.createElement("div");
                controlGroup.className = 'control-group';

                var label = controlGroup.appendChild(document.createElement("label"));
                label.innerHTML = data.label;
                label.className = 'control-label';

                var controls = controlGroup.appendChild(document.createElement("div"));
                controls.className = data.addon ? 'controls input-append' : 'controls';

                var userInput = controls.appendChild(document.createElement("input"));
                userInput.setAttribute( 'type', 'text' );
                userInput.setAttribute( 'placeholder', (data.placeholder || '') );
                userInput.onblur = function(){
                    data.objectReference[data.propertyReference] = this.value;
                }

                if(data.addon){
                    var addon = controls.appendChild(document.createElement("span"));
                    addon.className = 'add-on';
                    addon.innerHTML = data.addon;
                }

                if(data.help){
                    var help = controls.appendChild(document.createElement("span"));
                    help.className = 'help-block';
                    help.innerHTML = data.help;
                }

                if(data.comments){
                    var comments = controls.appendChild(document.createElement("textarea"));
                    comments.className = 'comments';
                    comments.innerHTML = data.comments;
                }

                return controlGroup;
            }

            // Fields used from just the verb
            function makeActionStoreVerbFields(e){

                // if verb has fields specific to it, add them to the form
                if(e.data.visible_fields){

                    var verbTr = document.createElement("tr"),
                        verbTd = document.createElement("td"),
                        verbForm = document.createElement("form");

                    verbForm.className = "form-horizontal";

                    for(var i = 0; i < e.data.visible_fields.length; i++){
                         
                        verbForm.appendChild( 
                            createFormControlGroup({
                                label : e.data.visible_fields[i].name,
                                help : e.data.visible_fields[i].help_text,
                                inputType : e.data.visible_fields[i].input_type,
                                isRequired : e.data.visible_fields[i].is_required,
                                isHidden : e.data.visible_fields[i].is_hidden,
                                objectReference: thisAction.verbFormFieldValues,
                                propertyReference: e.data.visible_fields[i].name
                            })
                        );
                    }
                    verbTd.appendChild(verbForm);
                    verbTr.appendChild(verbTd);
                    tbody.appendChild(verbTr);
                }
            }

            //------------------------------------
            //   Component Module
            //------------------------------------
            function makeActionStoreComponents(data){
                var title = document.createElement("div"),
                    componentsRow = document.createElement("tr"),
                    componentsTd = document.createElement("td"),
                        componentsTable = document.createElement("table"),
                            labels = document.createElement("tr"),
                                spacer = document.createElement("th"),
                                addProperty = document.createElement("span"),
                            addComponentRow = document.createElement("tr"),
                                addComponentName = document.createElement("td");

                componentsRow.className = "components-info";

                // Title
                title.className = "module-title";
                title.innerHTML = "Components";
                componentsTd.appendChild(title);

                // Outer table
                componentsTable.style.width = "100%";
                componentsTable.className = "table table-bordered";

                // Properties
                labels.className = "properties";
                spacer.className = "add-property";
                addProperty.innerHTML = "&plus; add property";
                spacer.appendChild(addProperty);
                labels.appendChild(spacer);

                addProperty.onclick = function(){ createNewProperty(this, thisAction.componentFields) };

                addComponentRow.className = "add-new-component";
                addComponentName.innerHTML = '<a href="javascript:void(0);">&plus; add new component</a>';
                addComponentName.setAttribute("colspan", "2");

                // Add new component to this action
                addComponentRow.onclick = function(){
                    this.parentNode.insertBefore(
                        createNewComponent(
                            this.parentNode.getElementsByClassName("properties")[0].getElementsByTagName("th").length,
                            thisAction.componentFields
                        ),    
                        this 
                    );
                }
                addComponentRow.addEventListener("focus", function(){
                    console.log(thisAction.componentFields)
                    this.parentNode.insertBefore(
                        createNewComponent(
                            this.parentNode.getElementsByClassName("properties")[0].getElementsByTagName("th").length,
                            thisAction.componentFields
                        ),    
                        this 
                    );
                }, true);

                addComponentRow.appendChild(addComponentName);

                // Add +properties and +components to the action
                componentsTable.appendChild(labels);
                componentsTable.appendChild(addComponentRow);
                componentsTd.appendChild(componentsTable);
                componentsRow.appendChild(componentsTd);
                tbody.appendChild(componentsRow);
            }

            //------------------------------------
            //   Machine Module
            //------------------------------------
            function makeActionStoreMachine(data){
                var machineRow = document.createElement("tr"),
                    machineTd = document.createElement("td"),
                    title = document.createElement("div"),
                    inputForm = document.createElement("form"),
                    objReference = thisAction.machineFields;

                machineRow.className = "machine-info";
                machineRow.colspan = "100";
                title.className = "module-title";
                title.innerHTML = "Machine";
                inputForm.className = "form-horizontal";

                // Name
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Name',
                        objectReference: objReference,
                        propertyReference: "name"
                    })
                );

                // Model
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Model',
                        objectReference: objReference,
                        propertyReference: "model"
                    })
                );

                // Time (in seconds)
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Time', 
                        placeholder: 'ex: 1:30:00 or 30:00-1:00:00',
                        help: "hr:min:sec",
                        objectReference: objReference,
                        propertyReference: "time"
                    })
                );
                
                // Temperature
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Temperature', 
                        placeholder: 'ex: 22 or 18-25', 
                        addon: '&deg;C',
                        objectReference: objReference,
                        propertyReference: "temp"
                    })
                );
                
                // Speed (in rpm)
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Speed', 
                        placeholder: 'ex: 22 or 18-25', 
                        addon: 'rpm',
                        objectReference: objReference,
                        propertyReference: "speed"
                    })
                );

                machineTd.appendChild(title);
                machineTd.appendChild(inputForm);
                machineRow.appendChild(machineTd);
                tbody.appendChild(machineRow);
            }

            //------------------------------------
            //   Thermocycler Module
            //------------------------------------
            function makeActionStoreThermocycler(data){
                var thermocyclerRow = document.createElement("tr"),
                    thermocyclerTd = document.createElement("td"),
                    title = document.createElement("div"),
                    inputForm = document.createElement("form"),
                    objReference = thisAction.thermocyclerFields;

                thermocyclerRow.className = "thermocycler-info";
                thermocyclerRow.colspan = "100";
                title.className = "module-title";
                title.innerHTML = "Thermocycler";
                inputForm.className = "form-horizontal";

                // Temperature
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Temperature', 
                        placeholder: 'ex: 22 or 18-25', 
                        addon: '&deg;C',
                        objectReference: objReference,
                        propertyReference: "temp"
                    })
                );

                // Time (in seconds)
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Time', 
                        placeholder: 'ex: 1:30:00 or 30:00-1:00:00', 
                        help: "hr:min:sec",
                        objectReference: objReference,
                        propertyReference: "time"
                    })
                );
                
                // Cycles
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Cycles',
                        objectReference: objReference,
                        propertyReference: "cycles"
                    })
                );

                // ...wat?
                // phase_list= [('','no cycle back')]
                // phase_list.extend([(x,x) for x in range(1,10)])
                // cycle_back_to

                machineTd.appendChild(title);
                machineTd.appendChild(inputForm);
                machineRow.appendChild(machineTd);
                tbody.appendChild(machineRow);
            }

            // Get data for each verb!
            // -----------------------
            $.ajax({
                url: apiUrlPrefix + 'action/fields/' + this.value.toLowerCase(),
                dataType: 'json',
                success: function(e){

                    // Update data
                    thisAction.verb = e.data.name;
                    thisAction.isActive = e.data.isActive;

                    // Show fields
                    thisAction.verbFormFieldValues = {};
                    makeActionStoreVerbFields(e);

                    if(e.data.has_components){
                        thisAction.componentFields = [];
                        makeActionStoreComponents(e); 
                    } else {
                        thisAction.componentFields = false;
                    }

                    if(e.data.has_machine){
                        thisAction.machineFields = {};
                        makeActionStoreMachine(e);
                    } else {
                        thisAction.machineFields = false;
                    }

                    if(e.data.has_thermocycler){
                        thisAction.thermocyclerFields = {};
                        makeActionStoreThermocycler(e);
                    } else {
                        thisAction.thermocyclerFields = false;
                    }
                },
                error: function(e){console.log("Ajax request failed. (Verb Components for "+ this.url +")")}
            });

        }

        innerVerbTd.setAttribute("colspan", "2");
        innerVerbTd.appendChild(innerVerbSelect);
        verb.className = "verb";
        verb.appendChild(innerVerbTd);
        // Add section to container
        tbody.appendChild(verb);

        
        // Add the collection of elements to the table
        action.appendChild(tbody);

        return action;
    }

    // Typeahead not working!
    function createNewProperty(that, objReference){
        var newProperty = document.createElement("th"),
            addComponentTr = that.parentNode.parentNode.parentNode.getElementsByClassName("add-new-component")[0].getElementsByTagName("td")[0],
            components = that.parentNode.parentNode.parentNode.getElementsByClassName('component');

        // Increase colspan so element stay 100% wide
        addComponentTr.setAttribute('colspan', parseInt(addComponentTr.getAttribute("colspan")) + 1);

        // Add td elements to each component that already exists
        if(components){
            for(var i = 0; i < components.length; i++){
                var newComponentProperty = document.createElement("td");
                newComponentProperty.className = 'component-property';
                newComponentProperty.innerHTML = "<a href='javascript:void(0);'>amount</a>";
                componentEditingFunctionality(newComponentProperty, objReference);
                if(components[i].children.length > 1){
                    components[i].insertBefore(newComponentProperty, components[i].children[1]);
                } else {
                    components[i].appendChild(newComponentProperty);
                }
            }
        }

        newProperty.innerHTML = '<input type="text" id="property-input" data-provide="typeahead" ' +
            'autocomplete="off" placeholder="mass, volume, etc" autofocus>';

        // Add editing functionality
        propertyEditingFunctionality(newProperty);

        // Add this property to DOM
        that.parentNode.parentNode.insertBefore(newProperty, that.parentNode.nextSibling);
        $("#property-input").hide();
        $("#property-input").fadeIn("fast", function(){
            // Add typeahead options
            $(this).typeahead({
                name: "property",
                items : 3,
                source : ["Mass","Density","Concentration"]
            });
        });
    }

    function createNewComponent(numOfProperties, objReference){
        var componentRow = document.createElement("tr"),
            componentName = document.createElement("td");
        
        componentRow.className = "component";
        componentName.innerHTML = '<input type="text" placeholder="component name" autofocus>';
        componentName.setAttribute("data-editing", true);
        componentEditingFunctionality(componentName, objReference);   // Add editing functionality
        componentRow.appendChild(componentName);

        // Add a property field for each available property (in the labels)
        for(var i = 0; i < numOfProperties - 1; i++){
            var newComponentProperty = document.createElement("td");
            // Set default value
            newComponentProperty.innerHTML = "<a href='javascript:void(0);'>amount</a>";
            // Add editing capabilities
            componentEditingFunctionality(newComponentProperty, objReference);
            // Add to row
            componentRow.appendChild(newComponentProperty);
        }

        return componentRow;
    }

    // Editing functionality for COMPONENT NAMES
    function componentEditingFunctionality(ele, objReference){

        ele.onclick = function(){
            if(this.getElementsByTagName("input")[0]) return;
            if(!this.getAttribute("data-editing") || this.getAttribute("data-editing") == "false"){
                this.setAttribute("data-editing", true);
                var inputValue = this.getElementsByTagName('a')[0].innerHTML == "amount" ? "" : this.getElementsByTagName('a')[0].innerHTML;
                this.innerHTML = '<input type="text" style="width:0;" placeholder="amount" value="' +  inputValue + '" autofocus>';
            }
            // Animate input to get wider
            $(this.getElementsByTagName("input")[0]).animate({width:'5em'}, 200);
        }
        ele.addEventListener("focus", function(){
            if(this.getElementsByTagName("input")[0]) return;
            if(!this.getAttribute("data-editing") || this.getAttribute("data-editing") == "false"){
                this.setAttribute("data-editing", true);
                var inputValue = this.getElementsByTagName('a')[0].innerHTML == "amount" ? "" : this.getElementsByTagName('a')[0].innerHTML;
                this.innerHTML = '<input type="text" style="width:0;" placeholder="amount" value="' +  inputValue + '" autofocus>';
            }
            // Animate input to get wider
            $(this.getElementsByTagName("input")[0]).animate({width:'5em'}, 200);
        }, true);

        // Check for "Enter" keypress
        ele.addEventListener("keydown", function(e) {
            if (!e) { var e = window.event; }
            if (e.keyCode == 13) {
                
                e.preventDefault();
                if(!this.getElementsByTagName("input")[0]) return;

                // Delete node if there is no component name
                if(!this.getElementsByTagName("input")[0].value && this == this.parentNode.firstChild) { 

                    // delete from data structure
                    // -1 of getIndexOf() due to the '+ add property' field being the first field
                    if(objReference[getIndexOf(this.parentNode) - 1]) delete objReference[getIndexOf(this.parentNode) - 1];

                    // restructure component array
                    restructureComponentArray(objReference, getIndexOf(this.parentNode) - 1);

                    // Remove element from DOM
                    this.parentNode.parentNode.removeChild(this.parentNode);
                    return;
                }

                // Coponent Name Field
                // Update the component object's title - or create the object if it doesn't exist
                if(this == this.parentNode.firstChild){
                    objReference[getIndexOf(this.parentNode) - 1] = objReference[getIndexOf(this.parentNode) - 1] || {};
                    objReference[getIndexOf(this.parentNode) - 1].title = this.getElementsByTagName("input")[0].value;
                }

                // Coponent Property Field
                else{
                    // Get the property name
                    //              td      tr       tbody    properties     same column as mod prop     <a>     prop value
                    var propName = this.parentNode.parentNode.firstChild.children[ getIndexOf(this) ].firstChild.innerHTML;
                    objReference[getIndexOf(this.parentNode) - 1][propName] = this.getElementsByTagName("input")[0].value;
                }

                // Set element back to original state of displaying the clickable value
                this.setAttribute("data-editing", false);
                var that = this;
                console.log(that, that.outerHTML)
                // Animate input to get skinnier
                $(this.getElementsByTagName("input")[0]).animate({width:'0'}, 200, "linear", function(){
                    that.innerHTML = '<a href="javascript:void(0)">' + 
                                     (that.getElementsByTagName("input")[0].value || "quantity") + 
                                     '</a>';
                });
            }
        }, true);

        // onblur event listener
        ele.addEventListener("blur", function(){

            // Make sure there's an input field before trying to act on it
            if(!this.getElementsByTagName("input")[0]) return;

            // Delete node if there is no component name - don't delete on empty component value
            if(!this.getElementsByTagName("input")[0].value && this == this.parentNode.firstChild) { 

                // delete from data structure
                // -1 of getIndexOf() due to the '+ add property' field being the first field
                if(objReference[getIndexOf(this.parentNode) - 1]) delete objReference[getIndexOf(this.parentNode) - 1];

                // restructure component array
                restructureComponentArray(objReference, getIndexOf(this.parentNode) - 1);

                // Remove element from DOM
                this.parentNode.parentNode.removeChild(this.parentNode);
                return;
            }

            // Coponent Name Field
            // Update the component object's title - or create the object if it doesn't exist
            if(this == this.parentNode.firstChild){
                objReference[getIndexOf(this.parentNode) - 1] = objReference[getIndexOf(this.parentNode) - 1] || {};
                objReference[getIndexOf(this.parentNode) - 1].title = this.getElementsByTagName("input")[0].value;
            }

            // Coponent Property Field
            else{
                // Get the property name
                //              td      tr       tbody    properties     same column as mod prop     <a>     prop value
                var propName = this.parentNode.parentNode.firstChild.children[ getIndexOf(this) ].firstChild.innerHTML;
                objReference[getIndexOf(this.parentNode) - 1][propName] = this.getElementsByTagName("input")[0].value;
            }

            // Set element back to original state of displaying the clickable value
            this.setAttribute("data-editing", false);
            var that = this;
            console.log(that, that.outerHTML)
            // Animate input to get skinnier
            $(this.getElementsByTagName("input")[0]).animate({width:'0'}, 200, "linear", function(){
                that.innerHTML = '<a href="javascript:void(0)">' + 
                                 (that.getElementsByTagName("input")[0].value || "quantity") + 
                                 '</a>';
            });
        }, true);
    }

    function propertyEditingFunctionality(ele){
        ele.onclick = function(){
            if(this.getElementsByTagName("input")[0]) return;
            if(!this.getAttribute("data-editing") || this.getAttribute("data-editing") == "false"){
                this.setAttribute("data-editing", true);
                this.innerHTML = '<input id="property-input" type="text" value="' + 
                    this.getElementsByTagName('a')[0].innerHTML + '" autofocus>';
                $(this.getElementsByTagName("input")[0]).focus();
            }
        }
        ele.addEventListener("focus", function(){
            if(this.getElementsByTagName("input")[0]) return;
            if(!this.getAttribute("data-editing") || this.getAttribute("data-editing") == "false"){
                this.setAttribute("data-editing", true);
                this.innerHTML = '<input id="property-input" type="text" value="' + 
                    this.getElementsByTagName('a')[0].innerHTML + '" autofocus>';
                $(this.getElementsByTagName("input")[0]).focus();
            }
        }, true);

        // Check for "Enter" keypress
        // REMOVE everything that was just added! colspan, tds, etc if empty
        ele.addEventListener("keydown", function(e) {
            if (!e) { var e = window.event; }
            if (e.keyCode == 13) {
                if(!this.getElementsByTagName("input")[0]) return;

                // Delete node if there is no component name
                if(!this.getElementsByTagName("input")[0].value) {
                    var component = this.parentNode.parentNode.getElementsByClassName("component"),
                        propNum = $(this).index();

                    // Delete the property field for each component
                    for(var i = 0; i < component.length; i++){
                        // Remove the fields directly under the property that was removed with index()
                        var propToRemove = component[i].getElementsByTagName("td")[propNum];
                        propToRemove.parentNode.removeChild(propToRemove);
                    }

                    this.parentNode.removeChild(this);
                    return;
                }

                this.setAttribute("data-editing", false);
                this.innerHTML = '<a href="javascript:void(0)">' + 
                    this.getElementsByTagName("input")[0].value + '</a>';
            }
        }, true);
        // REMOVE everything that was just added! colspan, tds, etc if empty
        ele.addEventListener("blur", function(){
            if(!this.getElementsByTagName("input")[0]) return;

            // Delete node if there is no component name
            if(!this.getElementsByTagName("input")[0].value) {
                var component = this.parentNode.parentNode.getElementsByClassName("component"),
                    propNum = $(this).index();

                // Delete the property field for each component
                for(var i = 0; i < component.length; i++){
                    // Remove the fields directly under the property that was removed with index()
                    var propToRemove = component[i].getElementsByTagName("td")[propNum];
                    propToRemove.parentNode.removeChild(propToRemove);
                }

                this.parentNode.removeChild(this);
                return;
            }

            this.setAttribute("data-editing", false);
            this.innerHTML = '<a href="javascript:void(0)">' + 
                this.getElementsByTagName("input")[0].value + '</a>';
        }, true);
    }

    function actionEditingFunctionality(ele){
    }

    // Generic editing capabilities for title, desc, and tabs
    function fieldEditingFunctionality(ele, placeholderText, messageOnEmpty, objReference, protocolProperty){
        ele.onclick = function(){

            // Exit if element already has an input field in it (it's already being edited)
            if(this.getElementsByTagName("input")[0]) return;

            // If the messageOnEmpty is being shown, delete it so the user is editing an empty field
            var editableName = this.innerHTML == messageOnEmpty ? "" : this.innerHTML; 

            // add input field for renaming
            this.setAttribute("data-editing", true);
            this.innerHTML = '<input type="text" placeholder="'+ placeholderText +'" value="' + editableName + '" autofocus>';
            $(this.getElementsByTagName("input")[0]).focus();
            
        }

        // Tabbing accessible
        ele.addEventListener("focus", function(){
            if(this.getElementsByTagName("input")[0]) return;

            // If the messageOnEmpty is being shown, delete it so the user is editing an empty field
            var editableName = this.innerHTML == messageOnEmpty ? "" : this.innerHTML; 

            this.setAttribute("data-editing", true);
            this.innerHTML = '<input type="text" placeholder="'+ placeholderText +'" value="' + editableName + '" autofocus>';
            $(this.getElementsByTagName("input")[0]).focus();

        }, true);

        // Check for "Enter" keypress
        ele.addEventListener("keydown", function(e) {
            if (!e) { var e = window.event; }
            if (e.keyCode == 13) {
                if(!this.getElementsByTagName("input")[0]) return;

                objReference[protocolProperty] = this.getElementsByTagName("input")[0].value || "";
                this.setAttribute("data-editing", false);
                this.innerHTML = (this.getElementsByTagName("input")[0].value || messageOnEmpty);
            }
        }, true);

        ele.addEventListener("blur", function(){
            if(!this.getElementsByTagName("input")[0]) return;

            objReference[protocolProperty] = this.getElementsByTagName("input")[0].value || "";
            this.setAttribute("data-editing", false);
            this.innerHTML = (this.getElementsByTagName("input")[0].value || messageOnEmpty);
        }, true);
    }

    // Find the step with the matching id
    function getStep(id){
        for(var i = 0; i < Protocol.steps.length; i++){
            if(Protocol.steps[i].id == id){
                return Protocol.steps[i];
            }
        }
    }

    // Get the position of a node in relation to its siblings
    // a a b a      // b == 2
    function getIndexOf(el){
        var k=-1, e=el;
        while (e) {
            if ( "previousSibling" in e ) {
                e = e.previousSibling;
                k = k + 1;
            } else {
                k= -1;
                break;
            }
        }
        return k;
    }

    function restructureComponentArray(array, index){

        // Make sure array needs restructuring (in case of multiple calls)
        // if something exists at the starting index it's already restructured
        if(array[index]) return;

        for(var i = index; i < array.length; i++){

            // Delete this property
            // At init it's empty anyway, after the first loop it's a duplicate
            if( array[i] ) delete array[i];

            // check if next property exists
            if(array[i + 1]){

                // move the next property into this slot
                array[i] = array[i + 1];

            } else {
                return;
            }
        }
    }

    return {
        verbList: verbList
    }

})();


// Sample data structure to send to server
/*

http://127.0.0.1:8000/api/action/fields/mix/
http://127.0.0.1:8000/api/action/types/

Protocol = {

    id: recievedFromServerOnPageLoad,
    title: userInputName,
    description, userInputDescription,

    steps: [
        {
            id: id,
            name: name,
            description: description,

            actions: [{
                id: tempUntilRecievedFromServer,
                step: Protocol.steps[id],
                name: userGivenName,
                active: activeValue,
                verb: verbName,
                verbFormFieldValues: {
                    time: time,
                    temp: temp
                },
                thermocyclerFields: false,
                componentFields: false,
                machineFields: {
                    name: name,
                    model: model,
                    time: time
                }
            
            },{

                id: tempUntilRecievedFromServer

            }]
        },
        {   
            id: id,
            name: name,
            description: description
        }
    ]
}
*/



