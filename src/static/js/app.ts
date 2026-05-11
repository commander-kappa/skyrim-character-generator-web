//INFO: DATA Map will be inserted by Server Template

const PROXY = DATA //as Map<string(dataType), Array<Object>
var ATTRIBUTE_MAP = {} as Map<string, string> //Map<attdsibuteId, dataType>

let attributesContainer = document.getElementById('attributes') as HTMLDivElement
let attributesCollection = attributesContainer?.children as HTMLCollectionOf<HTMLElement>


function setSelectOption(attribute_id:string, value:string, name:string): void {
    console.log(attribute_id)
    let customSelect = document.getElementById('select_' + attribute_id) as HTMLDivElement
    let selectElement = customSelect.children.item(0) as HTMLSelectElement
    let selectedElement = customSelect.children.item(1) as HTMLDivElement
    selectedElement.innerHTML = name

    while (selectElement.lastChild) {
        selectElement.removeChild(selectElement.lastChild)
    }
    let optionElement = document.createElement('option') as HTMLOptionElement
    optionElement.value = value
    optionElement.innerHTML = name
    selectElement.appendChild(optionElement)
    selectElement.value = value
}

function getMajorSkillIDs(): Array<Number> {
    let out = [] as Array<Number>
    for (let i = 1; i < 4; i++) {
        let selectElement = document.getElementById('major_skill_' + i) as HTMLSelectElement
        let val = '0' as string
        try  {val = selectElement.value; out.push(parseInt(val))}
        finally {continue}
    }
    return out
}
function blockSKillOptions(ids: Array<Number> = [0]): void {
    for (let i = 1; i < 4; i++) {
        let customSelect = document.getElementById('select_major_skill_' + i) as HTMLDivElement
        let customSelectItems = customSelect.children.item(2)?.children as HTMLCollectionOf<HTMLDivElement>
        console.log(ids)
        for (let item of Array.from(customSelectItems)) {
            let val = 0 as Number
            console.log(item.dataset.id)
            if(item.dataset.id) {val = parseInt(item.dataset.id)}
            if(ids.includes(val)) {item.classList.add('same-as-selected')}
            else {item.classList.remove('same-as-selected')} 
        }
    }   
}

function createCustomOptionElement(name:string, data_id:string): HTMLDivElement {
    let optionElement = document.createElement('div') as HTMLDivElement
    optionElement.innerHTML = name
    optionElement.setAttribute('data-id', data_id)

    optionElement.addEventListener('click', (event: MouseEvent) => {
        console.log("CLICK!")
        
        let thisElement = event.target as HTMLDivElement
        if (thisElement.classList.contains('same-as-selected')) {return}
        let custom_select_items = thisElement.parentElement as HTMLDivElement
        for (let select_item of custom_select_items.children) {
            if (select_item.classList.contains('same-as-selected')) {
                select_item.classList.remove('same-as-selected')
            }
        }
        thisElement.classList.add('same-as-selected')
        
        let thisValue = thisElement.dataset.id as string 
        let thisName = thisElement.innerHTML
        let attribute_id = thisElement.parentElement?.parentElement?.id.replace('select_', '') as string
    
        setSelectOption(attribute_id, thisValue, thisName)

        let selectElement = thisElement.parentNode?.parentNode?.children.item(0) as HTMLSelectElement
        console.log(selectElement.value)

        switch (attribute_id) {
            case 'race':
                loadSelectDataFor('religion')
                
                let mustReloadStart = false as boolean

                let select_start = document.getElementById('start') as HTMLSelectElement
                console.log(select_start.value)
                let old_start_id = parseInt(select_start.value) as number
                console.log('Start ID ' + old_start_id)
                
                if (old_start_id <= 0) {mustReloadStart = true}
                else if (PROXY.get('Start')[old_start_id - 1].race !== null) {mustReloadStart = true}
                
                if (mustReloadStart) {
                    console.log('Must reload Start anyway')   
                    loadSelectDataFor('start')
                }
                else {
                    let customSelect = document.getElementById('select_start') as HTMLDivElement
                    let customSelectOptionContainer = customSelect.children.item(2) as HTMLDivElement
                    let customSelectOptions = customSelectOptionContainer?.children as HTMLCollectionOf<HTMLDivElement>

                    for (let start of PROXY.get('Start')) {
                        if (start.race == null) {continue}
                        else if (start.race == parseInt(data_id)) {
                            customSelectOptionContainer.appendChild(
                                createCustomOptionElement(start.name, start.id)
                            )
                        }
                        else {
                            for (let option of Array.from(customSelectOptions)) {
                                if (option.dataset.id == null) {option.remove()}
                                else if (option.dataset.id == start.id) {option.remove()}
                   
                            }
                        }
                    } 
                }
                break;
            case 'major_skill_1':
                blockSKillOptions(getMajorSkillIDs())
                break;
            case 'major_skill_2':
                blockSKillOptions(getMajorSkillIDs())
                break;
            case 'major_skill_3':
                blockSKillOptions(getMajorSkillIDs())
                break;
            case 'start':
                loadSelectDataFor('specification')
                break;
            }
        
        });        

    return optionElement
}

function loadSelectData(id: string, relevant_data: Array<Object>): void {
    let dataType = document.getElementById('attribute_' + id)?.dataset.type as string
    setSelectOption(id, '0', 'Select ' + dataType)
    let selectElement = document.getElementById('select_' + id) as HTMLSelectElement
    let custom_select_items = selectElement.children.item(2) as HTMLDivElement
    
    while (custom_select_items.lastChild) {
        custom_select_items.removeChild(custom_select_items.lastChild)
    }

    if (relevant_data) for (let option of relevant_data) {
        custom_select_items.appendChild(
            createCustomOptionElement(option.name, option.id)
        )
    }
}
function loadAllSelectData(id: string) {
    let attributeElement = document.getElementById('attribute_' + id) as HTMLDivElement
    let attributeDataType = attributeElement.dataset.type as string
    loadSelectData(id, PROXY.get(attributeDataType))
}

function loadSelectDataFor(id: string) {
    let data = [] as Array<Object>
    let race = document.getElementById('race') as HTMLSelectElement
    let race_id = parseInt(race.value) as number
    
    switch (id) {
        case 'race':
            loadAllSelectData(id)
            break;
        case 'birthsign':
            loadAllSelectData(id)
            break;
        case 'religion':
            let religions = [] as Array<number>
            for (let entry of PROXY.get('RaceToReligion')) {
                if(entry.race > race_id) {break}
                else if(entry.race == race_id) {religions.push(entry.religion)}
            }
            for (let religion_id of religions) {
                data.push(PROXY.get('Religion')[religion_id - 1])
            }
            loadSelectData(id, data)
            break;
        case 'major_skill_1':
            loadAllSelectData(id)
            break;
        case 'major_skill_2':
            loadAllSelectData(id)
            break;
        case 'major_skill_3':
            loadAllSelectData(id)
            break;
        case 'personality':
            loadAllSelectData(id)
            break;
        case 'start':
            for (let entry of PROXY.get('Start')) {
                if(entry.race === null || entry.race == race_id) {
                    data.push(entry)
                }
            }
            loadSelectData(id, data)
            break;
        case 'specification':
            let start = document.getElementById('start') as HTMLSelectElement
            let start_id = parseInt(start.value)
            let specification = document.getElementById('attribute_specification') as HTMLDivElement
            
            if (start_id >= 1) {
                if (PROXY.get('Start')[start_id - 1].specification) {
                    console.log('display specification')
                    specification.style.display = 'flex'
                    for (let entry of PROXY.get('Specification')) {
                        if (entry.start == start_id) {
                        data.push(entry)
                    }
                }
            } else {specification.style.display = 'none'}

        } else {specification.style.display = 'none'}

        loadSelectData(id, data)
        break;
    }
}



function initDropdown() {
    loadSelectDataFor('race')
    loadSelectDataFor('birthsign')
    loadSelectDataFor('religion')
    loadSelectDataFor('major_skill_1')
    loadSelectDataFor('major_skill_2')
    loadSelectDataFor('major_skill_3')
    loadSelectDataFor('personality')
    loadSelectDataFor('start')
    loadSelectDataFor('specification')
}

initDropdown()








PROXY.forEach((val, key) => {
    console.log(key, val)
});
