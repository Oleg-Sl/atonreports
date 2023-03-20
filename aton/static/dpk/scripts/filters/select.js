
// фильтр по компаниям
class FilterSelect {
    constructor(container, requests, path, key) {
        this.container = container;
        this.path = path;
        this.requests = requests;
        this.key = key;

        this.elementSelect = document.querySelector('select');
    }

    init() { }
    
    getRequestParameters() {
        let val = this.elementSelect.value;
        console.log("Choice select options =", val);
        return this.elementSelect.value;
    }
}

export {FilterSelect, };

