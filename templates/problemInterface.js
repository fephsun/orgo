
    
        var jq = jQuery.noConflict();
        
        jq(document).ready(function() {
            //For making molecules and reactions draggable
            $( ".molecule" ).draggable({helper: "clone", revert:true, revertDuration: 100});
            $( ".reaction" ).draggable({helper: "clone", revert:true, revertDuration: 100});
            
            $(".molecule").droppable({
                drop: function(event, ui) {
                    $.ajax({
                        type: "POST",
                        url: "/orgo/homeMoleculeChanger/",
                        data: {'random': 'blah'},
                        success: function(data) {
                            $(".molecule").html(data);
                        },
                    });
                    alert(ui.draggable.html());
                }
            });
            
            //
            
            
            //For typing in autocompleted reagents
            //Update this line by parsing the value of [item for sublist in [REAGENTS[x][1] for x in range(len(REAGENTS)+1) if not x==0] for item in sublist]   in synthProblem.py
            var typeableReagents = ['H2', 'Hydrogen', 'Pd C catalyst', 'Pd/C catalyst', 'Pd|C catalyst', 'PdC catalyst', 'Palladium on carbon', 'EtOH', 'Ethanol', 'Ethyl alcohol', 'C2H5OH', 'HF', 'Hydrogen fluoride', 'Hydrofluoric acid', 'HBr', 'Hydrogen bromide', 'Hydrobromic acid', 'HCl', 'Hydrogen chloride', 'Hydrochloric acid', 'HI', 'Hydrogen iodide', 'Hydroiodic acid', 'CH2Cl2', 'Dichloromethane', 'Fluorine', 'F2', 'Bromine', 'Br2', 'Chlorine', 'Cl2', 'Iodine', 'I2', 'ROOR', 'tBuOOtBu', 'Peroxide', 'Tert-butyl peroxide', 'Di-tert-butyl peroxide', 'mCPBA', 'PhCO3H', 'RCO3H', 'H2SO4', 'Sulfuric acid', 'H2O', 'Water', 'Dihydrogen monoxide', 'HOH', 'HgSO4', 'Hg2+', 'Mercury sulfate', 'BH3', 'Borane', 'THF', 'Tetrahydrofuran', 'NaOH', 'Sodium hydroxide', 'Hydroxide', 'OH-', 'H2O2', 'Hydrogen Peroxide', 'OsO4', 'Osmium tetroxide', 'Osmium oxide', 'NMO', 'NMMO', 'N-Methylmorpholine N-oxide', 'Acetone', 'Propanone', '(CH3)2CO', 'Ozone', 'O3', 'Dimethyl sulfide', 'Methylthiomethane', 'Me2S', 'Zn', 'Zinc', 'Lindlar catalyst', 'Sodium', 'Na', 'NH3', 'Ammonia', 'Sodium amide', 'Sodamide', 'NaNH2', 'Amide', '1 equivalent', 'One equivalent', 'Heat', 'Hot', 'Warm', 'hv', 'Light'];
            //For having an autocomplete box which can take in multiple values
            function split( val ) {
                return val.split( /,\s*/ );
            }
            function extractLast( term ) {
                return split( term ).pop();
            }
            //Autocomplete box for reagents. Borrowed from jquery.
            $( "#reagentTyperBox" ).bind( "keydown", function( event ) {
                if ( event.keyCode === $.ui.keyCode.TAB && $( this ).data( "autocomplete" ).menu.active ) {
                    event.preventDefault();
                }
            })
            .autocomplete({
                minLength: 0,
                source: function( request, response ) {
                    response( $.ui.autocomplete.filter(typeableReagents, extractLast( request.term ) ) );
                },
                focus: function() {
                    return false;
                },
                select: function( event, ui ) {
                    var terms = split( this.value );
                    terms.pop();
                    terms.push( ui.item.value );
                    terms.push( "" );
                    this.value = terms.join( ", " );
                    return false;
                }
            });
              
            
            
            //For reagents in the sidebar
            $( "#reagentsHere" ).sortable();
            $( "#reagentsHere" ).disableSelection();

            
            
            
            updateReagents = function() {
                //Don't need to send anything back!
                //Update the reagents present in the sidebar with a new reagent.
                //Keep data about that reagent in currentReagents.
                var reagentString = $("#reagentTyperBox").val();
                

                var reagentHTML = reagentStringToHtml(reagentString);    
                if (reagentHTML != "") {
                    $("#reagentsHere").append(reagentHTML);
                }
                //Store the reagents.
                currentReagents[currentReagents.length] = reagentString;
            }
            
        
        //Create a sidebar reagent with the user input.
        //Javascriptified from the parseReagentsString method of synthProblem.py
        function reagentStringToHtml(reagentString) {    
            REAGENTS = [
                ["H<sub>2</sub>",["H2", "Hydrogen"]],
                ["Pd|C", ["PdC", "Pd/C", "Pd|C", "Pd C", "palladium"]],
                ["EtOH", ["EtOH", "Ethanol", "Ethyl alcohol", "C2H5OH"]],
                ["HF", ["HF", "Hydrogen fluoride", "Hydrofluoric acid"]],
                ["HBr", ["HBr", "Hydrogen bromide", "Hydrobromic acid"]],
                ["HCl", ["HCl", "Hydrogen chloride", "Hydrochloric acid"]],
                ["HI", ["HI", "Hydrogen iodide", "Hydroiodic acid"]],
                ["CH<sub>2</sub>Cl<sub>2</sub>", ["CH2Cl2", "Dichloromethane"]],
                ["F<sub>2</sub>", ["Fluorine", "F2"]],
                ["Br<sub>2</sub>", ["Bromine", "Br2"]],
                ["Cl<sub>2</sub>", ["Chlorine", "Cl2"]],
                ["I<sub>2</sub>", ["Iodine", "I2"]],
                ["ROOR", ["ROOR", "tBuOOtBu", "Peroxide", "Tert-butyl peroxide", "Di-tert-butyl peroxide"]],
                ["RCO<sub>3</sub>H",["mCPBA", "PhCO3H", "RCO3H"]],
                ["H<sub>2</sub>SO<sub>4</sub>", ["H2SO4", "Sulfuric acid"]],
                ["H<sub>2</sub>O", ["H2O", "Water", "Dihydrogen monoxide", "HOH", "H20"]],
                ["HgSO<sub>4</sub> accels.", ["HgSO4", "Hg2+", "Mercury sulfate"]],
                ["BH<sub>3</sub>", ["BH3", "Borane"]],
                ["THF", ["THF", "Tetrahydrofuran"]],
                ["NaOH", ["NaOH", "Sodium hydroxide", "Hydroxide", "OH-"]],
                ["H<sub>2</sub>O<sub>2</sub>", ["H2O2", "Hydrogen peroxide"]],
                ["OsO<sub>4</sub>", ["oso4", "osmium tetroxide", "osmium oxide"]],
                ["NMO", ["NMO", "NMMO", "N-Methylmorpholine N-oxide"]],
                ["Acetone", ["Acetone", "Propanone", "[CH3)2CO"]],
                ["O<sub>3</sub>", ["Ozone", "O3"]],
                ["Me<sub>2</sub>S", ["Dimethyl sulfide", "Methylthiomethane", "Me2S"]],
                ["Zn", ["Zn", "Zinc"]],
                ["cat. Lindlar", ["Lindlar",]],
                ["Na", ["Sodium", "Na"]],
                ["NH<sub>3 (L)</sub>", ["NH3", "Ammonia"]],
                ["NaNH<sub>2</sub>", ["Sodium amide", "Sodamide", "NaNH2", "Amide"]],
                ["1 equiv.", ["1", "eq", "one"]],
                ["Heat", ["heat", "delta", "hot", "warm"]],
                ["Light", ["hv", "light", "bright", "nu", "v", "hnu"]]
                ];
            
            string = reagentString.toLowerCase();
            dictionary = {};
            if (string == "") return "";
            
                
            var html = "";
            
            for (var i=0; i<REAGENTS.length; i++) {
                dictionary[REAGENTS[i][0]] = false;
                for (var j=0; j<REAGENTS[i][1].length; j++) {
                    var spelling = REAGENTS[i][1][j];
                    if (string.indexOf(spelling.toLowerCase()) != -1)
                        dictionary[REAGENTS[i][0]] = true;
                }
            }

            //hacky
            //Make sure you don't count substrings if you're counting things they're part of.
            if (dictionary["CH<sub>2</sub>Cl<sub>2</sub>"]) {
                if ((string.match(/h2/g).length - string.match(/ch2cl2/g).length) == 0)
                    dictionary["H<sub>2</sub>"] = false;
                if ((string.match(/cl2/g).length - string.match(/ch2cl2/g).length) == 0)
                    dictionary["Cl<sub>2</sub>"] = false;
            }
            if (dictionary["NaNH<sub>2</sub>"]) {
                if ((string.match(/na/g).length - string.match(/nanh2/g).length) == 0)
                    dictionary["Na"] = false;
            }
            if (dictionary["NaOH"]) {
                if ((string.match(/na/g).length - string.match(/naoh/g).length) == 0)
                    dictionary["Na"] = false;
            }
            if (dictionary["HF"]) {
                if ((string.match(/hydrogen fluoride/g).length - string.match(/hydrogen/g).length) == 0)
                    dictionary["H<sub>2</sub>"] = false;
            }
            if (dictionary["HCl"]) {
                if ((string.match(/hydrogen chloride/g).length - string.match(/hydrogen/g).length) == 0)
                    dictionary["H<sub>2</sub>"] = false;
            }
            if (dictionary["HI"]) {
                if ((string.match(/hydrogen iodide/g).length - string.match(/hydrogen/g).length) == 0)
                    dictionary["H<sub>2</sub>"] = false;
            }
            if (dictionary["HBr"]) {
                if ((string.match(/hydrogen bromide/g).length - string.match(/hydrogen/g).length) == 0)
                    dictionary["H<sub>2</sub>"] = false;
            }
            if (dictionary["H<sub>2</sub>O"]) {
                if ((string.match(/h2o/g).length + string.match(/h20/g).length - string.match(/h2/g).length) == 0)
                    dictionary["Na"] = false;
            }
            if (dictionary["RCO<sub>3</sub>H"]) {
                if ((string.match(/co3h/g).length - string.match(/o3/g).length) == 0)
                    dictionary["O<sub>3</sub>"] = false;
            }
            if (dictionary["Acetone"]) {
                if ((string.match(/acetone/g).length - string.match(/one/g).length) == 0)
                    dictionary["1 equiv."] = false;
            }
            
            for (var i=0; i<REAGENTS.length; i++) {
                if (dictionary[REAGENTS[i][0]]) {
                    html += REAGENTS[i][0] + ", ";
                }
            }
            
            return "<li class=\"reagent\" class = \"ui-state-default\">"+(html.substr(0, html.length-2))+"<img src=\"arrow.bmp\"/></li>"
        }
      });
      
    var currentReagents = new Array();
      
    var updateReagents;
    
    
    