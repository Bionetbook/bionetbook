//////////////////////////////////////
//                                  //
//      Protocol functionality      //
//        adding / editing          //
//                                  //
//////////////////////////////////////

"use strict";
var Protocol = {steps:[]};
var BNB = BNB || {};

BNB.dataInput = (function(){

    // Is this editing or making a new protocol?
    var createMode = false;

    var verbList = [ "Select a verb" ];

    init();

    function init(){

        // Protocol global object creation
        if(typeof Protocol == 'undefined'){
            window.Protocol = {
                steps: []
            };
            createMode = true;
        }

        // Populate verb list
        $.ajax({
            url: apiUrlPrefix + 'action/types/',
            dataType: 'json',
            success: function(e){
                for(var i =0; i < e.data.length; i++){
                    verbList.push( e.data[i].name );
                }
                // If there were actions made before the verbList was made
                // go back and populate them
                $('.verb-list').each(function(){
                    var thisVerb = this.getAttribute('data-default');
                    this.innerHTML = '';

                    for(var i = 0, len = verbList.length; i < len; i++){
                        var verb = document.createElement('option');
                        verb.innerHTML = verbList[i];
                        if(thisVerb === verbList[i]) verb.setAttribute('selected');
                        this.appendChild(verb);
                    }

                });
            },
            error: function(e){console.log("Failed to get Verb List.")}
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
            getExistingProtocol();
    }

    // Hero unit overlay + blurred out text
    function intro(){ 
        var userInput = document.getElementById('protocol-intro').getElementsByTagName('input')[0],
            submitBtn = document.getElementById('intro-submit');

        // Check for "Enter" keypress in the hero unit
        userInput.addEventListener("keydown", function(e) {
            if (!e) { var e = window.event; }
            if (e.keyCode == 13) { submitBtn.click(); }
        }, false);
    }

    function parseExistingProtocol(){

        var title = document.getElementById("protocol-title"),
            desc = document.getElementById("protocol-description");
        // Remove intro text
        $('#protocol-intro').fadeOut("fast");
        $(document.getElementById("nav-tabs")).removeClass("blur-text");

        // Let title + desc be editible
        fieldEditingFunctionality(title, "protocol name", "Name this protocol", Protocol, "title");
        fieldEditingFunctionality(desc, "description", "add a description", Protocol, "description");

        title.innerHTML = Protocol.title;
        desc.innerHTML = Protocol.description;

        for(var i = 0, len = Protocol.steps.length; i < len; i++){
            // Conform fields from API to what input form uses
            if( !Protocol.steps[i].title ) Protocol.steps[i].title = Protocol.steps[i].name;
            if( !Protocol.steps[i].id ) Protocol.steps[i].id = Protocol.steps[i].objectid;
            addNewTab( Protocol.steps[i] );
        }

        // HIDE all tabs/panes
        $(".tab-pane").removeClass('active');
        $(".step-tab").removeClass('active');
        // SHOW first tab/pane
        $(".step-tab:first-child").addClass('active');
        $('.tab-pane:first-child').addClass('active');
    }

    function addNewTab(existingStep){
        var tabContainer = document.getElementById('protocol-tabs'),
            newTab = document.createElement("li"),
            newLink = document.createElement("a"),
            tabNum = document.getElementById("protocol-tabs").getElementsByTagName("li").length;

        // Set up a new step
        if(!existingStep){

            // Create new step in Protocol
            Protocol.steps.push({
                actions: []
            });

            newLink.innerHTML = '<input type="text" placeholder="step name" autofocus>';
        } else {
            newLink.innerHTML = existingStep.title;
        }

        // Add attributes
        newTab.className += " step-tab active";
        newLink.href = "#tabContent" + tabNum;
        if(existingStep) newLink.setAttribute('value', existingStep.title)
        fieldEditingFunctionality(
            newLink,                        // Edit functionality
            "step name",                    // Placeholder text
            "Name this step",               // Empty submit message
            Protocol.steps[tabNum-1],       // Reference to js object
            "title"                         // Property of object to link this field to
        );

        // Construct tab content and append it to the tab content container
        if(!existingStep) 
            createTabContent( tabNum, Protocol.steps[tabNum-1] );
        else 
            createTabContent( tabNum, Protocol.steps[tabNum-1], existingStep.actions ); 

        // Add new tab to the tab list
        newTab.appendChild(newLink);
        tabContainer.insertBefore(newTab, document.getElementsByClassName('add-new-step')[0]);


        // Switch active tabs
        $('.tab-pane').removeClass('active');
        $("#tabContent" + tabNum).addClass('active');

        // Because it's clicked, it recieves the .active class
        $(".add-new-step").removeClass('active');

        // Tabbing functionality - click to show
        // The creation of a new element leaves it without an event listener,
        // so the current ones must be stripped and reapplied(reapplies to new element)
        // REMOVE
        $('#nav-tabs li.step-tab a').off('click.showTab');
        $('#nav-tabs li.add-new-step a').off('click.newTab');
        // ADD
        $('#nav-tabs li.step-tab a').on('click.showTab', function (e) {
            e.preventDefault();
            $(this).tab('show');

            // show actions underneath tab
            var nextTab = this.parentNode.nextSibling;
            while( $(nextTab).hasClass('action-tab')){
                $(nextTab).addClass('active');
                nextTab = nextTab.nextSibling;
            }
        });
        // Add new tab when the "add new tab" is clicked
        $('#nav-tabs li.add-new-step a').on('click.newTab', function (e) {
            e.preventDefault();
            addNewTab();
        });
    }

    function createTabContent(tabNum, stepObj, existingActions){
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
        headerH2Edit.innerHTML = existingActions ? stepObj.description : "add a description";
        headerH2Edit.className = "step-description";
        // Step description editing
        fieldEditingFunctionality(headerH2Edit, 'description', 'add a description', stepObj, "description");

        headerH2Small.appendChild(headerH2Edit);
        headerH2.appendChild(headerH2Small);
        header.appendChild(headerH2);
        tabContent.appendChild(header);

        tabContent.className = "tab-pane";
        tabContent.id = "tabContent" + tabNum;

        addAction.className = "add-new-action";
        addAction.innerHTML='<h4>&plus; add new action</h4>';
        tabContent.appendChild(addAction);
        
        // Create action from existing data
        if(existingActions){
            for(var i = 0, len = existingActions.length; i < len; i++){

                // Conform API fields to what is in use
                if(!existingActions[i].title) existingActions[i].title = existingActions[i].name;
                if(!existingActions[i].id) existingActions[i].id = existingActions[i].objectid;

                // Create action
                var el = createNewAction(stepObj, existingActions[i]);
                addAction.parentNode.insertBefore(el, addAction);
                $(el).hide().fadeIn();
            }
        }

        // Add another action
        addAction.onclick = function(){

            // Add action to containing Step
            stepObj.actions.push({});

            // Create action
            var newAction = createNewAction(stepObj);

            // show action
            newAction.style.display = "none";
            this.parentNode.insertBefore(newAction, this);
            $(newAction).fadeIn();


            // Add action link to tabs
            /*var tabs = document.getElementById('protocol-tabs');
            var activeTab = tabs.getElementsByClassName('active')[0],
                nextTab = activeTab.nextSibling;
            while( !$(nextTab).hasClass('step-tab') && !$(nextTab).hasClass('add-new-step') ){
                nextTab = nextTab.nextSibling;
            } 
            var actionTab = document.createElement('li');
            actionTab.className = 'action-tab active';
            actionTab.innerHTML = 'new action';
            tabs.insertBefore( actionTab, nextTab );*/

            // TODO: 
            // View action on action-tab click in tab contents area
            // On action name change, change tab name as well
            // Get indexOf() action-tab
            // $().hide() all others in the .active tab-pane
        }

        document.getElementsByClassName("tab-content")[0].appendChild(tabContent);

        // Show tabs on click
        $('#nav-tabs li a').on('click.showTab', function (e) {
            e.preventDefault();
            $(this).tab('show'); 
            $('#protocol-tabs .action-tab').removeClass('active'); 
        });
    }

    function createNewAction(stepObj, existingAction){
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

        action.className = "table table-bordered action-container";

        var thisAction = stepObj.actions[ stepObj.actions.length - 1 ];
        

        //------------------------------------
        //   Action header (naming action)
        //------------------------------------
        // Verb
        innerHeaderh4.innerHTML = existingAction ? existingAction.title : "Name this action";
        innerHeaderTd.setAttribute("colspan", "2");
        innerHeaderTd.appendChild(innerHeaderh4);
        innerHeaderTd.appendChild(isActiveToggle);
        header.className = "action-header";
        header.appendChild(innerHeaderTd);

        // is active
        isActive.setAttribute("type", "checkbox");
        if(existingAction){
            if(existingAction.isActive){
                isActive.setAttribute('checked');
            }
        } 
        isActiveLabel.appendChild(isActive);
        isActiveLabel.onclick = function(){
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

        innerVerbSelect.className = "verb-list";

        // Add verbs to select node
        for(var i = 0; i < verbList.length; i++){

            var verbOption = document.createElement("option");

            // Check if verbList has been populated yet
            if(verbList.length > 1){
                verbOption.innerHTML = verbList[i];
                verbOption.value = verbList[i];

                // Display existing action's verb as default
                if(existingAction){
                    if(existingAction.verb === verbOption.value){
                        verbOption.setAttribute('selected', 'selected');
                    }
                }
            }else{
                // Create one <option>Loading...</option>
                // first ajax call for verbList will populate all verblists
                verbOption.innerHTML = '<option>Loading verbs...</option>';

                // Store the default verb so the ajax call can show it when finished
                if(existingAction){
                    innerVerbSelect.setAttribute('data-default', existingAction.verb.toLowerCase());
                }
            }
            innerVerbSelect.appendChild(verbOption);
        }

        // Add event handler for verb selection
        innerVerbSelect.onchange = function(data){

            // We don't want event data
            if(data == event) data = false;

            // Clear previous verb selection
            // Lots of .parentNode so here's a respresentation of the structure:
            // tbody -> tr.verb -> td -> select(this) -> option
            if(!data){
                while(this.parentNode.parentNode.nextSibling){
                    this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.nextSibling);
                }
                thisAction.verb = "";
            }

            // Create form elements
            // Arg: object, property of data to look in for values
            function createFormControlGroup(verbData){

                var controlGroup = document.createElement("div");
                controlGroup.className = 'control-group';

                var label = controlGroup.appendChild(document.createElement("label"));
                label.innerHTML = verbData.label;
                label.className = 'control-label';

                var controls = controlGroup.appendChild(document.createElement("div"));
                controls.className = verbData.addon ? 'controls input-append' : 'controls';

                var userInput = controls.appendChild(document.createElement("input"));
                userInput.setAttribute( 'type', 'text' );
                userInput.setAttribute( 'placeholder', (verbData.placeholder || '') );

                // Populate value if the action already exists
                if(data.hasOwnProperty(verbData.propertyReference))
                    userInput.value = data[verbData.propertyReference];
                // Check in sub-objects for containers like machineFields
                if(data.hasOwnProperty(verbData.inputCreationFor))
                    userInput.value = data[verbData.inputCreationFor][verbData.propertyReference];

                // Save user input data to js object
                userInput.onblur = function(){
                    verbData.objectReference[verbData.propertyReference] = this.value;
                }

                if(verbData.addon){
                    var addon = controls.appendChild(document.createElement("span"));
                    addon.className = 'add-on';
                    addon.innerHTML = verbData.addon;
                }

                if(verbData.help){
                    var help = controls.appendChild(document.createElement("span"));
                    help.className = 'help-block';
                    help.innerHTML = verbData.help;
                }

                if(verbData.comments){
                    var comments = controls.appendChild(document.createElement("textarea"));
                    comments.className = 'comments';
                    comments.innerHTML = verbData.comments;
                }

                return controlGroup;
            }

            // Fields used from just the verb
            function makeActionStoreVerbFields(e){

                // if verb has fields specific to it, add them to the form
                if(e.visible_fields){

                    var verbTr = document.createElement("tr"),
                        verbTd = document.createElement("td"),
                        verbForm = document.createElement("form");

                    verbForm.className = "form-horizontal";

                    for(var i = 0; i < e.visible_fields.length; i++){
                        verbForm.appendChild( 
                            createFormControlGroup({
                                label : e.visible_fields[i].name,
                                help : e.visible_fields[i].help_text,
                                inputType : e.visible_fields[i].input_type,
                                isRequired : e.visible_fields[i].is_required,
                                isHidden : e.visible_fields[i].is_hidden,
                                objectReference: thisAction.verbFormFieldValues,
                                propertyReference: e.visible_fields[i].name,
                                inputCreationFor: 'verbFormFieldValues'
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
            function makeActionStoreComponents(){
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
                            this.parentNode.getElementsByClassName("properties")[0]
                                .getElementsByTagName("th").length,
                            thisAction.componentFields
                        ),    
                        this 
                    );
                }
                addComponentRow.addEventListener("focus", function(){
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

                // Populate component fields from existing data
                if(data){

                    // Check for existing component data
                    for(var i = 0, len = data.componentFields.length; i < len; i++){
                        addComponentRow.parentNode.insertBefore(
                            createNewComponent(
                                addComponentRow.parentNode.getElementsByClassName("properties")[0]
                                    .getElementsByTagName("th").length,
                                thisAction.componentFields,
                                data.componentFields[i].title
                            ),
                            addComponentRow
                        );
                    }

                    // Check for existing component Property data
                    // Some components have fields that aren't set, so it won't work
                    // to use a single component to get every property in use
                    var propList = [];
                    for(var a = 0, len = thisAction.componentFields.length; a < len; a++){
                        // Go through each property in each component
                        for(var p in thisAction.componentFields[a]){
                            // Make sure it's a user-defined property
                            if(thisAction.componentFields[a].hasOwnProperty(p)){
                                var inPropList = false;
                                // Does propList already have it?
                                for(var b = 0, len = propList.length; b < len; b++){
                                    if(p == propList[b]) inPropList = true;
                                }
                                if(!inPropList && p != 'title') propList.push(p);
                                inPropList = undefined;
                            }
                        }
                    }
                    // Make properties
                    for(var a = 0, len = propList.length; a < len; a++){
                        createNewProperty(addProperty, thisAction.componentFields, propList[a])
                    }
                }
            }

            //------------------------------------
            //   Machine Module
            //------------------------------------
            function makeActionStoreMachine(){
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
                        propertyReference: "name",
                        inputCreationFor: 'machineFields'
                    })
                );

                // Model
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Model',
                        objectReference: objReference,
                        propertyReference: "model",
                        inputCreationFor: 'machineFields'
                    })
                );

                // Time (in seconds)
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Time', 
                        placeholder: 'ex: 1:30:00 or 30:00-1:00:00',
                        help: "hr:min:sec",
                        objectReference: objReference,
                        propertyReference: "time",
                        inputCreationFor: 'machineFields'
                    })
                );
                
                // Temperature
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Temperature', 
                        placeholder: 'ex: 22 or 18-25', 
                        addon: '&deg;C',
                        objectReference: objReference,
                        propertyReference: "temp",
                        inputCreationFor: 'machineFields'
                    })
                );
                
                // Speed (in rpm)
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Speed', 
                        placeholder: 'ex: 22 or 18-25', 
                        addon: 'rpm',
                        objectReference: objReference,
                        propertyReference: "speed",
                        inputCreationFor: 'machineFields'
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
            function makeActionStoreThermocycler(){
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
                        propertyReference: "temp",
                        inputCreationFor: 'thermocyclerFields'
                    })
                );

                // Time (in seconds)
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Time', 
                        placeholder: 'ex: 1:30:00 or 30:00-1:00:00', 
                        help: "hr:min:sec",
                        objectReference: objReference,
                        propertyReference: "time",
                        inputCreationFor: 'thermocyclerFields'
                    })
                );
                
                // Cycles
                inputForm.appendChild(
                    createFormControlGroup({
                        label: 'Cycles',
                        objectReference: objReference,
                        propertyReference: "cycles",
                        inputCreationFor: 'thermocyclerFields'
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
            var verbForUrl = data ? data.verb.toLowerCase() : this.value.toLowerCase();
            $.ajax({
                url: apiUrlPrefix + 'action/fields/' + verbForUrl,
                dataType: 'json',
                success: function(e){

                    // Update data
                    if(!data) thisAction.verb = e.name;
                    if(!data) thisAction.isActive = e.isActive;

                    // Show fields
                    if(!data) thisAction.verbFormFieldValues = {};
                    makeActionStoreVerbFields(e);

                    if(e.has_components){
                        if(!data) thisAction.componentFields = [];
                        makeActionStoreComponents(); 
                    } else {
                        thisAction.componentFields = false;
                    }

                    if(e.has_machine){
                        if(!data) thisAction.machineFields = {};
                        makeActionStoreMachine();
                    } else {
                        thisAction.machineFields = false;
                    }

                    if(e.has_thermocycler){
                        if(!data) thisAction.thermocyclerFields = {};
                        makeActionStoreThermocycler();
                    } else {
                        thisAction.thermocyclerFields = false;
                    }
                },
                error: function(e){console.log("Ajax request failed. (Verb Components for "+ (data.verb.toLowerCase() || this.url) +")")}
            });
        }

        // Trigger loading the fields if this action already exists
        // This will allow the fields to populate with the action data
        if(existingAction) innerVerbSelect.onchange(existingAction);

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

    // -- Typeahead not working! -- //
    // Well... it is, but the value is never added to input field on enter/click
    // Also does not support minLength = 0
    // --------
    // Arg: element to insertBefore(), js object containing all components, 
    //      property for an existing action
    function createNewProperty(that, objReference, prop){
        var newProperty = document.createElement("th"),
            addComponentTr = that.parentNode.parentNode.parentNode.getElementsByClassName("add-new-component")[0].getElementsByTagName("td")[0],
            components = that.parentNode.parentNode.parentNode.getElementsByClassName('component');

        // Increase colspan so the element stays 100% wide
        addComponentTr.setAttribute('colspan', parseInt(addComponentTr.getAttribute("colspan")) + 1);

        // Add td elements to each component that already exists
        if(components){
            for(var i = 0; i < components.length; i++){
                var newComponentProperty = document.createElement("td");
                newComponentProperty.className = 'component-property';

                // Set the component's field to the saved value for the property
                newComponentProperty.innerHTML = 
                    prop ? "<a href='javascript:void(0);'>"+ objReference[i][prop] +"</a>" :
                           "<a href='javascript:void(0);'>amount</a>";

                componentEditingFunctionality(newComponentProperty, objReference);
                if(components[i].children.length > 1){
                    components[i].insertBefore(newComponentProperty, components[i].children[1]);
                } else {
                    components[i].appendChild(newComponentProperty);
                }
            }
        }

        // If property isn't supplied, create an input field
        newProperty.innerHTML = 
            prop ? '<a href="javascript:void(0)">'+ prop +'</a>' :
            '<input type="text" id="property-input" data-provide="typeahead" ' +
            'autocomplete="off" placeholder="mass, volume, etc" autofocus>';

        // Add editing functionality
        propertyEditingFunctionality(newProperty, objReference);

        // the editing functionality sets this when the user enters data but
        // since the data is already supplied this must be set here
        if(prop) newProperty.setAttribute("data-value", prop);

        // Add this property to DOM
        that.parentNode.parentNode.insertBefore(newProperty, that.parentNode.nextSibling);
        $("#property-input").hide().fadeIn("fast", function(){
            // Add typeahead options
            $(this).typeahead({
                name: "property",
                items : 3,
                source : ["Mass","Density","Concentration"]
            });
        });
    }

    function createNewComponent(numOfProperties, objReference, existingVal){
        var componentRow = document.createElement("tr"),
            componentName = document.createElement("td");
        
        componentRow.className = "component";
        componentName.innerHTML = existingVal ? 
            '<a href="javascript:void(0)">'+ existingVal +'</a>' :
            '<input type="text" placeholder="component name" autofocus>';
        componentName.setAttribute("data-editing", true);
        componentEditingFunctionality(componentName, objReference);   // Add editing functionality
        componentRow.appendChild(componentName);

        // Add a property field for each available property (in the labels)
        for(var i = 0; i < numOfProperties - 1; i++){
            var newComponentProperty = document.createElement("td");

            newComponentProperty.innerHTML = "<a href='javascript:void(0);'>amount</a>";

            componentEditingFunctionality(newComponentProperty, objReference)
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
            if(this == this.parentNode.firstChild)
                $(this.getElementsByTagName("input")[0]).animate({width:'15em'}, 200);
            else
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
            if(this == this.parentNode.firstChild)
                $(this.getElementsByTagName("input")[0]).animate({width:'15em'}, 200);
            else
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
                    objReference[getIndexOf(this.parentNode) - 1].title = 
                        htmlEntities( this.getElementsByTagName("input")[0].value );
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
                // Animate input to get skinnier
                $(this.getElementsByTagName("input")[0]).animate({width:'0'}, 200, "linear", function(){
                    that.innerHTML = '<a href="javascript:void(0)">' + 
                                     (htmlEntities( that.getElementsByTagName("input")[0].value ) || "quantity") + 
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
            // Animate input to get skinnier
            $(this.getElementsByTagName("input")[0]).animate({width:'0'}, 200, "linear", function(){
                that.innerHTML = '<a href="javascript:void(0)">' + 
                                 (htmlEntities( that.getElementsByTagName("input")[0].value ) || "quantity") + 
                                 '</a>';
            });
        }, true);
    }

    // Editing functionality for PROPERTY NAMES
    // objReference = array of component objects
    function propertyEditingFunctionality(ele, objReference){
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
        // if empty: REMOVE everything that was just added! colspan, tds, etc
        ele.addEventListener("keydown", function(e) {
            if (!e) { var e = window.event; }
            if (e.keyCode == 13) {
                if(!this.getElementsByTagName("input")[0]) return;

                // Delete node if there is no component name
                if(!this.getElementsByTagName("input")[0].value) {
                    var component = this.parentNode.parentNode.getElementsByClassName("component"),
                        propNum = $(this).index();

                    // Remove properties of the action when user deletes property
                    for(var i = 0; i < objReference.length; i++){
                        delete objReference[i][this.getAttribute("data-value")];
                    }

                    // Delete the property field for each component
                    for(var i = 0; i < component.length; i++){
                        // Remove the fields directly under the property that was removed with index()
                        var propToRemove = component[i].getElementsByTagName("td")[propNum];
                        propToRemove.parentNode.removeChild(propToRemove);
                    }

                    this.parentNode.removeChild(this);
                    return;
                }

                // Modify properties of the action to reflect new property name - on edit
                for(var i = 0; i < objReference.length; i++){
                    if(this.getElementsByTagName("input")[0].value != this.getAttribute("data-value")){
                        objReference[i][htmlEntities( this.getElementsByTagName("input")[0].value )] = 
                            objReference[i][this.getAttribute("data-value")];
                        delete objReference[i][this.getAttribute("data-value")];
                    }
                }

                this.setAttribute("data-editing", false);

                // Track the value just before current change. Helps with property name changes + deletion
                this.setAttribute("data-value", htmlEntities( this.getElementsByTagName("input")[0].value ));

                // Show user the new name
                this.innerHTML = '<a href="javascript:void(0)">' + 
                    htmlEntities( this.getElementsByTagName("input")[0].value ) + '</a>';
            }
        }, true);
        // if empty: REMOVE everything that was just added! colspan, tds, etc
        ele.addEventListener("blur", function(){
            if(!this.getElementsByTagName("input")[0]) return;

            // Delete node if there is no component name
            if(!this.getElementsByTagName("input")[0].value) {
                var component = this.parentNode.parentNode.getElementsByClassName("component"),
                    propNum = $(this).index();

                // Remove properties of the action when user deletes property
                for(var i = 0; i < objReference.length; i++){
                    delete objReference[i][this.getAttribute("data-value")];
                }

                // Delete the property field for each component
                for(var i = 0; i < component.length; i++){
                    // Remove the fields directly under the property that was removed with index()
                    var propToRemove = component[i].getElementsByTagName("td")[propNum];
                    propToRemove.parentNode.removeChild(propToRemove);
                }

                this.parentNode.removeChild(this);
                return;
            }

            // Modify properties of the action to reflect new property name - on edit
            for(var i = 0; i < objReference.length; i++){
                if(this.getElementsByTagName("input")[0].value != this.getAttribute("data-value")){
                    objReference[i][htmlEntities( this.getElementsByTagName("input")[0].value )] = 
                        objReference[i][this.getAttribute("data-value")];
                    delete objReference[i][this.getAttribute("data-value")];
                }
            }

            this.setAttribute("data-editing", false);

            // Track the value just before current change. Helps with property name changes + deletion
            this.setAttribute("data-value", htmlEntities( this.getElementsByTagName("input")[0].value ));

            // Show user the new name
            this.innerHTML = '<a href="javascript:void(0)">' + 
                htmlEntities( this.getElementsByTagName("input")[0].value ) + '</a>';
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

    function htmlEntities(str) {
        return String(str).replace(/&amp;/g, '&').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // Edit an existing Protocol
    function getExistingProtocol(){
        // Get slug
        var a = window.location.href.split('/');
        while(a[a.length-1] == 'edit' || a[a.length -1] == 'test' || a[a.length -1] == false) a.pop();
        var slug = a[a.length-1];

        $.ajax({
            url: apiUrlPrefix + 'protocol/' + slug,
            dataType: 'json',
            success: function(e){
                // Construct Protocol structure
                var p = e.data.data,
                    d = e.data;
                p.id = d.id;
                p.description = d.description;
                p.title = d.name;
                p.slug = d.slug;
                window.Protocol = p;
                parseExistingProtocol();
            },
            error: function(e){console.log("Failed to recieve existing Protocol)")}
        });

        /*window.Protocol = //    TESTING ONLY
        {"id":"p1","steps":[{"id":"temp1378421980279","actions":[{"id":"temp1378421983864",
        "verb":"Measure","isActive":true,"verbFormFieldValues":{"what_are_you_measuring":"I'm measuring stuff",
        "measurement_value":"10","measurement_units":"ml","device":"Scale","file_of_measurement":""},
        "componentFields":false,"machineFields":{"name":"Dat Machine","model":"mx2","time":"3:00:00-5:00:00",
        "temp":"20-23","speed":"22-30"},"thermocyclerFields":false,"title":"Named, yo."}],"title":"First Step",
        "description":"Descripsioso"},{"id":"temp1378422063483","actions":[{"id":"temp1378422092884",
        "title":"Deez actions","verb":"Add","verbFormFieldValues":{"conditional_statement":"Nahh... nah."},
        "componentFields":[{"title":"Comp1","Prop2":"10ml","Prop1":"2ml"},{"title":"component2","Prop2":"8",
        "Prop1":"7"}],"machineFields":false,"thermocyclerFields":false}],"title":"Second Step Name",
        "description":"Second descrip"}],"title":"Dat Protocol","description":"I'll tell you hwat"};*/

        parseExistingProtocol();
    }

    var sendToServer = (function(){
        var saveButton = document.getElementById('save-protocol'),
            createProtocolBtn = document.getElementById('intro-submit'),
            csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        // Remove from user view
        $('input[name=csrfmiddlewaretoken]').remove();

        // Add functionality to the buttons
        document.getElementById('save-protocol').onclick = 
            createMode ? create : save;
        createProtocolBtn.onclick = create;


        // Automatically remove alert
        function removeAlert(){
            setTimeout(function(){
                var saveAlert = document.getElementsByClassName('save-alert')[0];
                if(saveAlert){
                    $(saveAlert).fadeOut(200, function(){
                        $(saveAlert).remove();
                    });
                }
            }, 10000);
        }

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

        function save(){
            // Protocol's URL identifier - remove preceding 'p' in ID
            var pSlug = Protocol.id[0] === 'p' ? Protocol.id.slice(1) : Protocol.id;

            // Send Protocol object to server
            $.ajax({
                url: apiUrlPrefix + 'protocol/' + pSlug + '/',
                contentType: 'application/json',
                type: "PUT",
                data: JSON.stringify(Protocol),
                success: function(e){ 

                    // Assumed location of Protocol object
                    var newP = e.data;

                    // Update Protocol id
                    if(!Protocol.hasOwnProperty('id') && !Protocol.hasOwnProperty('objectid'))
                        Protocol.id = newP.id;

                    // Update all step/action ids
                    for(var a = 0, sLen = Protocol.steps.length, pSteps = Protocol.steps; a < sLen; a++){

                        // Check for step id
                        if(!pSteps[a].hasOwnProperty('id') && !pSteps[a].hasOwnProperty('objectid'))
                            pSteps[a].id = newP.steps[a].id;

                        for(var b = 0, aLen = pSteps.actions.length, pActions = pSteps[a].actions; b < aLen; b++){

                            // Check for action id
                            if(!pActions[b].hasOwnProperty('id') && !pActions[b].hasOwnProperty('objectid'))
                                pActions[b].id = newP.steps[b].id;
                        }
                    }

                    if(document.getElementsByClassName('save-alert')[0])
                        $('.save-alert').remove();

                    // Show success message
                    var message = saveButton.parentNode.appendChild(document.createElement("div"));
                    message.className = 'alert alert-error save-alert';
                    message.innerHTML = '<button type="button" class="close" data-dismiss="alert">×</button>';
                    message.innerHTML += '<strong>Success!</strong> ';
                    message.innerHTML += 'This protocol has been saved.';
                    $(message).hide().fadeIn(200);

                    removeAlert(); // Waits 10s then auto removes
                },
                error: function(e){ 
                    if(document.getElementsByClassName('save-alert')[0])
                        $('.save-alert').remove();

                    var message = saveButton.parentNode.appendChild(document.createElement("div"));
                    message.className = 'alert alert-error save-alert';
                    message.innerHTML = '<button type="button" class="close" data-dismiss="alert">×</button>';
                    message.innerHTML += '<strong>Whoops!</strong> ';
                    message.innerHTML += 'Could not connect to the server; try again in just a second.';
                    $(message).hide().fadeIn(200);

                    removeAlert(); // Waits 10s then auto removes
                }
            });
        }

        function create(){

            var userInput = document.getElementById('protocol-intro').getElementsByTagName('input')[0],
                btn = $(this);

            // Make sure they typed in a name or fire an error
            if(userInput.value.length < 2){
                var errorNode = document.createElement('div');
                errorNode.className = "alert alert-error";
                errorNode.innerHTML = '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                                      "You have to name the protocol before you can continue!";
                userInput.parentNode.parentNode.insertBefore(errorNode, userInput.parentNode)
                return;
            }

            // Show loading icon
            btn.css('width', '4em').button('loading');

            // Send Protocol object to server
            $.ajax({
                url: apiUrlPrefix + 'protocol/create',
                contentType: 'application/json',
                type: "POST",
                data: Protocol,
                success: function(e){ 

                    Protocol = e.data;
                    if(!Protocol.steps) Protocol.steps = [];

                    // Change icon from loading to OK
                    btn.get(0).getElementsByTagName('i')[0].className = 'icon-ok icon-white';

                    // Add title to protocol object
                    Protocol.title = userInput.value;

                    // Change Title
                    document.getElementById("protocol-title").innerHTML = userInput.value;

                    // Remove overlay
                    $(document.getElementById('protocol-intro')).fadeOut("fast");

                    // Remove blurred text
                    $(document.getElementById("nav-tabs")).removeClass("blur-text");

                    // Add first Step
                    addNewTab();

                    // Let title + desc be editible
                    fieldEditingFunctionality(document.getElementById("protocol-title"), 
                        "protocol name", "Name this protocol", Protocol, "title");
                    fieldEditingFunctionality(document.getElementById("protocol-description"), 
                        "description", "add a description", Protocol, "description");
                },
                error: function(e){ 

                    var userInput = document.getElementById('protocol-intro').getElementsByTagName('input')[0];

                    // Stop Hero Unit from being removed

                    // Change icon from loading to refresh
                    btn.get(0).getElementsByTagName('i')[0].className = 'icon-refresh icon-white';
                    btn.button('refresh');
                   
                    if(document.getElementsByClassName('save-alert')[0])
                        $('.save-alert').remove();

                    // Display error message (could not connect to server)
                    var message = userInput.parentNode.appendChild(document.createElement("div"));
                    message.className = 'alert alert-error save-alert';
                    message.style.marginTop = '1em';
                    message.innerHTML = '<button type="button" class="close" data-dismiss="alert">×</button>';
                    message.innerHTML += '<strong>Whoops!</strong> ';
                    message.innerHTML += 'Could not connect to the server; try again in just a second.';
                    $(message).hide().fadeIn(200);

                    removeAlert(); // Waits 10s then auto removes
                }
            });
            // When Protocol creation returns successful
            document.getElementById('save-protocol').onclick = save;
        }
    })();

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



