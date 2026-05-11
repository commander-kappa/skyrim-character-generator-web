//INFO: DATA Map will be inserted by Server Template
var PROXY = DATA; //as Map<string(dataType), Array<Object>
var ATTRIBUTE_MAP = {}; //Map<attdsibuteId, dataType>
var attributesContainer = document.getElementById('attributes');
var attributesCollection = attributesContainer === null || attributesContainer === void 0 ? void 0 : attributesContainer.children;
function setSelectOption(attribute_id, value, name) {
    console.log(attribute_id);
    var customSelect = document.getElementById('select_' + attribute_id);
    var selectElement = customSelect.children.item(0);
    var selectedElement = customSelect.children.item(1);
    selectedElement.innerHTML = name;
    while (selectElement.lastChild) {
        selectElement.removeChild(selectElement.lastChild);
    }
    var optionElement = document.createElement('option');
    optionElement.value = value;
    optionElement.innerHTML = name;
    selectElement.appendChild(optionElement);
    selectElement.value = value;
}
function getMajorSkillIDs() {
    var out = [];
    for (var i = 1; i < 4; i++) {
        var selectElement = document.getElementById('major_skill_' + i);
        var val = '0';
        try {
            val = selectElement.value;
            out.push(parseInt(val));
        }
        finally {
            continue;
        }
    }
    return out;
}
function blockSKillOptions(ids) {
    var _a;
    if (ids === void 0) { ids = [0]; }
    for (var i = 1; i < 4; i++) {
        var customSelect = document.getElementById('select_major_skill_' + i);
        var customSelectItems = (_a = customSelect.children.item(2)) === null || _a === void 0 ? void 0 : _a.children;
        console.log(ids);
        for (var _i = 0, _b = Array.from(customSelectItems); _i < _b.length; _i++) {
            var item = _b[_i];
            var val = 0;
            console.log(item.dataset.id);
            if (item.dataset.id) {
                val = parseInt(item.dataset.id);
            }
            if (ids.includes(val)) {
                item.classList.add('same-as-selected');
            }
            else {
                item.classList.remove('same-as-selected');
            }
        }
    }
}
function createCustomOptionElement(name, data_id) {
    var optionElement = document.createElement('div');
    optionElement.innerHTML = name;
    optionElement.setAttribute('data-id', data_id);
    optionElement.addEventListener('click', function (event) {
        var _a, _b, _c, _d;
        console.log("CLICK!");
        var thisElement = event.target;
        if (thisElement.classList.contains('same-as-selected')) {
            return;
        }
        var custom_select_items = thisElement.parentElement;
        for (var _i = 0, _e = custom_select_items.children; _i < _e.length; _i++) {
            var select_item = _e[_i];
            if (select_item.classList.contains('same-as-selected')) {
                select_item.classList.remove('same-as-selected');
            }
        }
        thisElement.classList.add('same-as-selected');
        var thisValue = thisElement.dataset.id;
        var thisName = thisElement.innerHTML;
        var attribute_id = (_b = (_a = thisElement.parentElement) === null || _a === void 0 ? void 0 : _a.parentElement) === null || _b === void 0 ? void 0 : _b.id.replace('select_', '');
        setSelectOption(attribute_id, thisValue, thisName);
        var selectElement = (_d = (_c = thisElement.parentNode) === null || _c === void 0 ? void 0 : _c.parentNode) === null || _d === void 0 ? void 0 : _d.children.item(0);
        console.log(selectElement.value);
        switch (attribute_id) {
            case 'race':
                loadSelectDataFor('religion');
                var mustReloadStart = false;
                var select_start = document.getElementById('start');
                console.log(select_start.value);
                var old_start_id = parseInt(select_start.value);
                console.log('Start ID ' + old_start_id);
                if (old_start_id <= 0) {
                    mustReloadStart = true;
                }
                else if (PROXY.get('Start')[old_start_id - 1].race !== null) {
                    mustReloadStart = true;
                }
                if (mustReloadStart) {
                    console.log('Must reload Start anyway');
                    loadSelectDataFor('start');
                }
                else {
                    var customSelect = document.getElementById('select_start');
                    var customSelectOptionContainer = customSelect.children.item(2);
                    var customSelectOptions = customSelectOptionContainer === null || customSelectOptionContainer === void 0 ? void 0 : customSelectOptionContainer.children;
                    for (var _f = 0, _g = PROXY.get('Start'); _f < _g.length; _f++) {
                        var start = _g[_f];
                        if (start.race == null) {
                            continue;
                        }
                        else if (start.race == parseInt(data_id)) {
                            customSelectOptionContainer.appendChild(createCustomOptionElement(start.name, start.id));
                        }
                        else {
                            for (var _h = 0, _j = Array.from(customSelectOptions); _h < _j.length; _h++) {
                                var option = _j[_h];
                                if (option.dataset.id == null) {
                                    option.remove();
                                }
                                else if (option.dataset.id == start.id) {
                                    option.remove();
                                }
                            }
                        }
                    }
                }
                break;
            case 'major_skill_1':
                blockSKillOptions(getMajorSkillIDs());
                break;
            case 'major_skill_2':
                blockSKillOptions(getMajorSkillIDs());
                break;
            case 'major_skill_3':
                blockSKillOptions(getMajorSkillIDs());
                break;
            case 'start':
                loadSelectDataFor('specification');
                break;
        }
    });
    return optionElement;
}
function loadSelectData(id, relevant_data) {
    var _a;
    var dataType = (_a = document.getElementById('attribute_' + id)) === null || _a === void 0 ? void 0 : _a.dataset.type;
    setSelectOption(id, '0', 'Select ' + dataType);
    var selectElement = document.getElementById('select_' + id);
    var custom_select_items = selectElement.children.item(2);
    while (custom_select_items.lastChild) {
        custom_select_items.removeChild(custom_select_items.lastChild);
    }
    if (relevant_data)
        for (var _i = 0, relevant_data_1 = relevant_data; _i < relevant_data_1.length; _i++) {
            var option = relevant_data_1[_i];
            custom_select_items.appendChild(createCustomOptionElement(option.name, option.id));
        }
}
function loadAllSelectData(id) {
    var attributeElement = document.getElementById('attribute_' + id);
    var attributeDataType = attributeElement.dataset.type;
    loadSelectData(id, PROXY.get(attributeDataType));
}
function loadSelectDataFor(id) {
    var data = [];
    var race = document.getElementById('race');
    var race_id = parseInt(race.value);
    switch (id) {
        case 'race':
            loadAllSelectData(id);
            break;
        case 'birthsign':
            loadAllSelectData(id);
            break;
        case 'religion':
            var religions = [];
            for (var _i = 0, _a = PROXY.get('RaceToReligion'); _i < _a.length; _i++) {
                var entry = _a[_i];
                if (entry.race > race_id) {
                    break;
                }
                else if (entry.race == race_id) {
                    religions.push(entry.religion);
                }
            }
            for (var _b = 0, religions_1 = religions; _b < religions_1.length; _b++) {
                var religion_id = religions_1[_b];
                data.push(PROXY.get('Religion')[religion_id - 1]);
            }
            loadSelectData(id, data);
            break;
        case 'major_skill_1':
            loadAllSelectData(id);
            break;
        case 'major_skill_2':
            loadAllSelectData(id);
            break;
        case 'major_skill_3':
            loadAllSelectData(id);
            break;
        case 'personality':
            loadAllSelectData(id);
            break;
        case 'start':
            for (var _c = 0, _d = PROXY.get('Start'); _c < _d.length; _c++) {
                var entry = _d[_c];
                if (entry.race === null || entry.race == race_id) {
                    data.push(entry);
                }
            }
            loadSelectData(id, data);
            break;
        case 'specification':
            var start = document.getElementById('start');
            var start_id = parseInt(start.value);
            var specification = document.getElementById('attribute_specification');
            if (start_id >= 1) {
                if (PROXY.get('Start')[start_id - 1].specification) {
                    console.log('display specification');
                    specification.style.display = 'flex';
                    for (var _e = 0, _f = PROXY.get('Specification'); _e < _f.length; _e++) {
                        var entry = _f[_e];
                        if (entry.start == start_id) {
                            data.push(entry);
                        }
                    }
                }
                else {
                    specification.style.display = 'none';
                }
            }
            else {
                specification.style.display = 'none';
            }
            loadSelectData(id, data);
            break;
    }
}
function initDropdown() {
    loadSelectDataFor('race');
    loadSelectDataFor('birthsign');
    loadSelectDataFor('religion');
    loadSelectDataFor('major_skill_1');
    loadSelectDataFor('major_skill_2');
    loadSelectDataFor('major_skill_3');
    loadSelectDataFor('personality');
    loadSelectDataFor('start');
    loadSelectDataFor('specification');
}
initDropdown();
PROXY.forEach(function (val, key) {
    console.log(key, val);
});
